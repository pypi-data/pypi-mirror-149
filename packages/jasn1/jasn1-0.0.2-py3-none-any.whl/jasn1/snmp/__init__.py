import sys

from jasn1.bidict import *
from jasn1.asn1 import *
from .types import *

class SNMP(ASN1):

    V1_TRAP = V1_TRAP
    INFORM = INFORM
    V2_TRAP = V2_TRAP

    class Types(MAP):
        __MAP__ = BiDict({
            4: V1_TRAP,
            6: INFORM,
            7: V2_TRAP,
        })

    @classmethod
    def parse_tag_type(cls, node: tuple, tag_class: str, tag_constructed: bool, tag: int):
        if node == (2,):
            if cls.Types.get(tag) is None:
                raise NotImplementedError("SNMP tag type {tag} has no mapping".format(tag=tag))
            return cls.Types.get(tag)
        else:
            return cls.__base__.parse_tag_type(cls, tag_class, tag_constructed, node, tag)

    @classmethod
    def parse_value(cls, node: tuple, tag_class: str, tag_constructed: bool, tag_type: str, value_length: int, value_tag: bytes):
        return tag_type.parse_value(cls, node, tag_class, tag_constructed, value_length, value_tag)
