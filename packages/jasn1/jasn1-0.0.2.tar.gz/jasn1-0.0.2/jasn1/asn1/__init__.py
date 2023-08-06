from jasn1.bidict import *
from .types import *

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

class MAP:

    @classmethod
    def get(cls, key):
        return cls.__MAP__.get(key)

    @classmethod
    def rget(cls, value):
        return cls.__MAP__.rget(value)

class ASN1:

    class Classes:
        UNIVERSAL = "UNIVERSAL"
        APPLICATION = "APPLICATION"
        PRIVATE = "PRIVATE"
        CONTEXT_SPECIFIC = "CONTEXT_SPECIFIC"

    class Types(MAP):

        END_OF_CONTENT = END_OF_CONTENT
        OCTET_STRING = OCTET_STRING
        BOOLEAN = BOOLEAN
        INTEGER = INTEGER
        BIT_STRING = BIT_STRING
        OCTET_STRING = OCTET_STRING
        NULL = NULL
        OBJECT_IDENTIFIER = OBJECT_IDENTIFIER
        ObjectDescriptor = ObjectDescriptor
        ENUMERATED = ENUMERATED
        EMBEDDED_PDV = EMBEDDED_PDV
        UTF8String = UTF8String
        SEQUENCE = SEQUENCE
        SET = SET
        NumericString = NumericString
        PrintableString = PrintableString
        T61String = T61String
        VideotexString = VideotexString
        IA5String = IA5String
        UTCTime = UTCTime

        __MAP__ = BiDict({
            0: END_OF_CONTENT,
            1: BOOLEAN,
            2: INTEGER,
            3: BIT_STRING,
            4: OCTET_STRING,
            5: NULL,
            6: OBJECT_IDENTIFIER,
            7: ObjectDescriptor,
            10: ENUMERATED,
            11: EMBEDDED_PDV,
            12: UTF8String,
            16: SEQUENCE,
            17: SET,
            18: NumericString,
            19: PrintableString,
            20: T61String,
            21: VideotexString,
            22: IA5String,
            23: UTCTime,
        })

    def parse_tag_type(cls, node: tuple, tag_class: str, tag_constructed: bool, tag: int):
        if cls.Types.get(tag) is None:
            raise NotImplementedError("Type '{tag_type}' has not been implemented in class '{cls}'".format(tag_type=str(tag), cls=cls))
        return cls.Types.get(tag)

    @staticmethod
    def zero_length_value(tag_class: str, tag_constructed: bool, tag_type: str, num_length_octets: int = 0, value_length: int = 0):
        return {
            "tag": {
                "class": tag_class,
                "constructed": tag_constructed,
                "type": tag_type.__name__,
            },
            "num_length_octets": num_length_octets,
            "value_length": value_length,
            "value": None,
        }

    @classmethod
    def decode(cls, data: bytes, node: tuple = (), simplify=False):
        if len(data) == 0:
            return None

        tag = data[0]

        bit_8 = tag & (1 << (8 - 1))
        bit_7 = tag & (1 << (7 - 1))
        bit_6 = tag & (1 << (6 - 1))

        if not bit_8 and not bit_7:
            tag_class = cls.Classes.UNIVERSAL
        elif not bit_8 and bit_7:
            tag_class = cls.Classes.APPLICATION
        elif bit_8 and not bit_7:
            tag_class = cls.Classes.CONTEXT_SPECIFIC
        elif bit_8 and bit_7:
            tag_class = cls.Classes.PRIVATE

        tag_constructed = bool(bit_6)

        tag_type = cls.parse_tag_type(node, tag_class, tag_constructed, tag % 32)
        if len(data) == 1:
            return cls.zero_length_value(tag_class, tag_constructed, tag_type)

        num_length_octets = 1
        value_length = data[1]
        if len(data) == 2:
            return cls.zero_length_value(tag_class, tag_constructed, tag_type, num_length_octets, value_length)

        if value_length > 127:
            num_length_octets = value_length - 128

            value_starting_octet = 2 + num_length_octets
            value_length = 0
            for octet in data[2:value_starting_octet]:
                value_length *= 256
                value_length += octet

        else:
            value_starting_octet = 2

        if value_length < 1:
            return cls.zero_length_value(tag_class, tag_constructed, tag_type, num_length_octets, 0)

        value_tag = data[value_starting_octet:(value_starting_octet + value_length)]

        value = cls.parse_value(node, tag_class, tag_constructed, tag_type, value_length, value_tag)
        output = {
            "tag": {
                "class": tag_class,
                "constructed": tag_constructed,
                "type": tag_type.__name__,
            },
            "num_length_octets": num_length_octets,
            "value_length": value_length,
            "value": value,
        }

        if node == () and simplify == True:
            output = simplify_json_data(output)
        return output
