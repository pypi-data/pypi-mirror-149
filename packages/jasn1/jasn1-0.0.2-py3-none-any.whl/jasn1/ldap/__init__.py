import sys

from jasn1.bidict import *
from jasn1.asn1 import *
from .types import *

class LDAP(ASN1):

    LDAPMessage = LDAPMessage

    MessageID = MessageID
    class protocolOp(MAP):
        __MAP__ = BiDict({
            0: BindRequest,
            1: BindResponse,
            2: UnbindRequest,
            3: SearchRequest,
            4: SearchResultEntry,
            5: SearchResultDone,
            6: SearchResultReference,
            7: ModifyRequest,
            8: ModifyResponse,
            9: AddRequest,
            10: AddResponse,
            11: DelRequest,
            12: DelResponse,
            13: ModifyDNRequest,
            14: ModifyDNResponse,
            15: CompareRequest,
            16: CompareResponse,
            17: AbandonRequest,
            18: ExtendedRequest,
            19: ExtendedResponse,
        })

    LDAP_SUCCESS = LDAP_SUCCESS
    LDAP_OPERATIONS_ERROR = LDAP_OPERATIONS_ERROR

    @classmethod
    def parse_tag_type(cls, node: tuple, tag_class: str, tag_constructed: bool, tag: int):
        if node == ():
            return cls.LDAPMessage
        elif node == (0,):
            return cls.MessageID
        elif node == (1,):
            if cls.protocolOp.get(tag) is None:
                raise NotImplementedError("LDAP tag type {tag} has no mapping".format(tag=tag))
            return cls.protocolOp.get(tag)
        elif len(node) == 2 and node[0] == 1 and tag_class == ASN1.Classes.CONTEXT_SPECIFIC and tag == 0:
            return ASN1.Types.SEQUENCE
        else:
            return cls.__base__.parse_tag_type(cls, tag_class, tag_constructed, node, tag)

    @classmethod
    def parse_value(cls, node: tuple, tag_class: str, tag_constructed: bool, tag_type: str, value_length: int, value_tag: bytes):
        if node == (1, 0) and tag_type == ASN1.Types.ENUMERATED:
            if int.from_bytes(value_tag, byteorder=sys.byteorder) == 0:
                return cls.LDAP_SUCCESS.__name__
            elif int.from_bytes(value_tag, byteorder=sys.byteorder) == 1:
                return cls.LDAP_OPERATIONS_ERROR.__name__
        else:
            return tag_type.parse_value(cls, node, tag_class, tag_constructed, value_length, value_tag)
