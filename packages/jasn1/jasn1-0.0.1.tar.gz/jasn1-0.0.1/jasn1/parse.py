from .asn1 import *
from .snmp import *
from .ldap import *

def simplify_json_data(json_data):
    simplified_data = {}
    if type(json_data["value"]) == list:
        simplified_data[json_data["tag"]["type"]] = []
        for value in json_data["value"]:
            simplified_data[json_data["tag"]["type"]].append(simplify_json_data(value))
    elif type(json_data["value"]) == dict:
        if json_data["value"].get("text") is not None:
            simplified_data[json_data["tag"]["type"]] = json_data["value"]["text"]
        else:
            simplified_data[json_data["tag"]["type"]] = json_data["value"]
    else:
        simplified_data[json_data["tag"]["type"]] = json_data["value"]
    return simplified_data

def decode_asn1(asn1: bytes, node: tuple = (), protocol=None, simplify=True):
    tag = asn1[0]

    bit_8 = tag & (1 << (8 - 1))
    bit_7 = tag & (1 << (7 - 1))
    bit_6 = tag & (1 << (6 - 1))

    if not bit_8 and not bit_7:
        tag_class = ASN1.classes.UNIVERSAL
    elif not bit_8 and bit_7:
        tag_class = ASN1.classes.APPLICATION
    elif bit_8 and not bit_7:
        tag_class = ASN1.classes.CONTEXT_SPECIFIC
    elif bit_8 and bit_7:
        tag_class = ASN1.classes.PRIVATE

    tag_constructed = bool(bit_6)

    tag_type = None
    if protocol == 'snmp':
        tag_type = SNMP.parse_tag_type(tag)
    elif protocol == 'ldap':
        tag_type = LDAP.parse_tag_type(tag)

    if tag_type is None:
        #if TYPE_MAP.get(tag) is None:
        #    raise NotImplementedError("Tag type {tag} has no mapping".format(tag=tag))
        tag_type = ASN1.TYPE_MAP.get(tag)

    if tag_type is None:
        tag_type = str(tag_type_int)

    if len(asn1) < 2:
        return {
            "tag": {
                "class": class_tag,
                "constructed": constructed_tag,
                "type": tag_type,
                "of": None,
            },
            "num_length_octets": 0,
            "length": 0,
            "value": None,
        }
    num_length_octets = 1
    length = asn1[1]

    if length > 127:
        num_length_octets = length - 128

        value_starting_octet = 2 + num_length_octets
        length = 0
        for octet in asn1[2:value_starting_octet]:
            length *= 256
            length += octet
            #length_octets.append(bin(octet)[2:].zfill(8))
        #length = int("".join(length_octets), 2)

    else:
        value_starting_octet = 2

    if length > 1:
        value_tag = b[value_starting_octet:(value_starting_octet + length)]
    elif length == 1:
        value_tag = b[2]
    elif length < 1:
        return {
            "tag": {
                "class": class_tag,
                "constructed": constructed_tag,
                "type": tag_type,
                "of": None,
            },
            "num_length_octets": num_length_octets,
            "length": length,
            "value": None,
        }

    if tag_type == ASN1.BOOLEAN:
        value = value_tag
        #print(value)

    if tag_type == ASN1.NULL:
        value = None

    elif tag_type in [ASN1.INTEGER, ASN1.ENUMERATED]:
        if length == 1:
            if value_tag & (1 << (8 - 1)):
                negative = True
                value = value_tag - 128
            else:
                negative = False
                value = value_tag

        else:
            sum = 0
            if value_tag[0] & (1 << (8 - 1)):
                negative = True
                value = value_tag[0] - 128
            else:
                negative = False

            for value_octect in value_tag[1:]:
                sum *= 256
                sum += value_octect

            if negative:
                value = sum - (2 ** ((8 * len(byte_values)) - 1))
            else:
                value = sum

        if protocol == 'ldap':
            value = LDAP.parse_value(value)

    elif tag_type == "BIT STRING":
        if not constructed_tag:
            if length == 1:
                value = bin(value_tag)[2:].zfill(8)
            else:
                bit_strings = []
                unused_bits = value_tag[0]
                bit_strings.append(bin(unused_bits)[2:].zfill(8))
                value = {
                    "unused": unused_bits,
                    "raw_bitstring": "".join(bit_strings),
                    "no_length_bitstring": "".join(bit_strings[1:]),
                }

            if type(value_tag) == int:
                value = bin(value_tag)[2:].zfill(8)
            else:
                bit_strings = []
                unused_bits = value_tag[0]
                bit_strings.append(bin(unused_bits)[2:].zfill(8))

                for bit_string_byte in value_tag[1:]:
                    bit_strings.append(bin(bit_string_byte)[2:].zfill(8))
                value = {
                    "unused": unused_bits,
                    "raw_bitstring": "".join(bit_strings),
                    "no_length_bitstring": "".join(bit_strings[1:]),
                }
                value["stripped_bitstring"] = ("".join(bit_strings[1:]))[(len("".join(bit_strings[1:])) - unused_bits)]

                #try:
                #    value["stripped_bitstring"] = ("".join(bit_strings[1:]))[(len("".join(bit_strings[1:])) - unused_bits)]
                #except IndexError as e:
                #    value["stripped_bitstring"] = None

        else:
            value = decode_asn1(value_tag)

    elif tag_type == "OCTET STRING":
        value = str(value)
        """
        byte_strings = []
        for bit_string_byte in value_tag:
            byte_strings.append(bin(bit_string_byte)[2:].zfill(8))
        bit_string = "".join(byte_strings)
        hex_string = hex(int(bit_string, 2))[2:]
        if len(hex_string) % 2 == 0:
            try:
                text = bytes.fromhex(hex_string).decode('ascii')
            except ValueError as e:
                text = None
        else:
            text = None
            text = str(hex_string)[2:]

        value = {
            "bits": bit_string,
            "hex": hex_string,
            "text": text,
        }
        """

    elif tag_type == "OBJECT IDENTIFIER":
        object_ids = []
        if length == 1:
            object_ids.append(value_tag // 40)
            object_ids.append(value_tag % 40)
        else:
            object_ids.append(value_tag[0] // 40)
            object_ids.append(value_tag[0] % 40)

            current_value = 0
            for octet in value_tag[1:]:

                current_value *= 128
                if octet & (1 << (8 - 1)):
                    current_value += (octet - 128)
                else:
                    current_value += octet

                    object_ids.append(current_value)
                    current_values.clear()

        value = ".".join([str(x) for x in object_ids])

    elif tag_type == "UTF8 STRING":
        value = "".join([x.decode('utf-8') for x in value_tag])

    elif tag_type in [
        "SEQUENCE",
        "SET",
        "EMBEDDED PDV",
        "ObjectDescriptor",
        *SNMP.TYPE_MAP.values(),
        *LDAP.TYPE_MAP.values(),
    ]:
        value = []
        inner_index = 0
        position = 0
        while position < length:
            if position >= len(value_tag):
                break
            element = decode_asn1(value_tag[position:], node=(*node, inner_index), protocol=protocol, simplify=False)
            position += element["length"] + element["num_length_octets"] + 1
            value.append(element)
            inner_index += 1

    else:
        return {
            "tag": {
                "class": class_tag,
                "constructed": constructed_tag,
                "type": tag_type,
                "of": None,
            },
            "num_length_octets": num_length_octets,
            "length": length,
            "value": value,
        }

    data = {
        "tag": {
            "class": class_tag,
            "constructed": constructed_tag,
            "type": tag_type,
            "of": None,
        },
        "num_length_octets": num_length_octets,
        "length": length,
        "value": value,
    }
    if node == () and simplify == True:
        data = simplify_json_data(data)
    return data
