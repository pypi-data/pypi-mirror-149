from abc import ABC, abstractmethod

class Type(ABC):

    @staticmethod
    @abstractmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        raise NotImplementedError

class END_OF_CONTENT(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        return None

class BOOLEAN(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        return bool(value_tag)

class INTEGER(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        sum = 0
        if value_tag[0] & (1 << (8 - 1)):
            negative = True
            sum += value_tag[0] - 128
        else:
            sum += value_tag[0]
            negative = False

        for value_octet in value_tag[1:]:
            sum *= 256
            sum += value_octet

        if negative:
            value = sum - (2 ** ((8 * len(value_tag)) - 1))
        else:
            value = sum

        return value

class BIT_STRING(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):

        if not tag_constructed:
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


        else:
            value = parent_cls.decode(value_tag, node, simplify=False)
        return value

class OCTET_STRING(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        return value_tag.decode('ISO-8859-1')

class NULL(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        return None

class OBJECT_IDENTIFIER(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        object_ids = []
        if value_length == 1:
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
        return value

class ObjectDescriptor(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        raise NotImplementedError

class EXTERNAL(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        raise NotImplementedError

class REAL(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        raise NotImplementedError

class ENUMERATED(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        sum = 0
        if value_tag[0] & (1 << (8 - 1)):
            negative = True
            sum += value_tag[0] - 128
        else:
            sum += value_tag[0]
            negative = False

        for value_octet in value_tag[1:]:
            sum *= 256
            sum += value_octet

        if negative:
            value = sum - (2 ** ((8 * len(value_tag)) - 1))
        else:
            value = sum

        return value

class EMBEDDED_PDV(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        #raise NotImplementedError
        return value_tag.decode('utf-8')
class UTF8String(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        return value_tag.decode('utf-8')

class SEQUENCE(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        value = []
        inner_index = 0
        position = 0
        while position < value_length:
            if position >= len(value_tag):
                break
            element = parent_cls.decode(value_tag[position:], node=(*node, inner_index), simplify=False)
            position += element["value_length"] + element["num_length_octets"] + 1
            value.append(element)
            inner_index += 1
        return value

class SET(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        value = []
        inner_index = 0
        position = 0
        while position < value_length:
            if position >= len(value_tag):
                break
            element = parent_cls.decode(value_tag[position:], node=(*node, inner_index), simplify=False)
            position += element["value_length"] + element["num_length_octets"] + 1
            value.append(element)
            inner_index += 1
        return value

class NumericString(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        return value_tag.decode('utf-8')

class PrintableString(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        return value_tag.decode('utf-8')

class T61String(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        return value_tag.decode('utf-8')

class VideotexString(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        return value_tag.decode('utf-8')

class IA5String(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        return value_tag.decode('utf-8')

class UTCTime(Type):

    @staticmethod
    def parse_value(parent_cls, node: tuple, tag_class: str, tag_constructed: bool, value_length: int, value_tag: bytes):
        return value_tag.decode('utf-8')
