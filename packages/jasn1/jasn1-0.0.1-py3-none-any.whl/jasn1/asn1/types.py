class ASN1Types:

    OCTET_STRING = "OCTET STRING"
    BOOLEAN = "BOOLEAN"
    INTEGER = "INTEGER"
    BIT_STRING = "BIT_STRING"
    OCTET_STRING = "OCTET_STRING"
    NULL = "NULL"
    OBJECT_IDENTIFIER = "OBJECT_IDENTIFIER"
    ObjectDescriptor = "ObjectDescriptor"
    ENUMERATED = "ENUMERATED"
    EMBEDDED_PDV = "EMBEDDED_PDV"
    UTF8_STRING = "UTF8_STRING"
    SEQUENCE = "SEQUENCE"
    SET = "SET"
    PrintableString = "PrintableString"
    T61String = "T61String"
    IA5String = "IA5String"
    UTCTime = "UTCTime"

    TYPE_MAP = {
        0: OCTET_STRING,
        1: BOOLEAN,
        2: INTEGER,
        3: BIT_STRING,
        4: OCTET_STRING,
        5: NULL,
        6: OBJECT_IDENTIFIER,
        7: ObjectDescriptor,
        10: ENUMERATED,
        11: EMBEDDED_PDV,
        12: UTF8_STRING,
        16: SEQUENCE,
        17: SET,
        19: PrintableString,
        20: T61String,
        22: IA5String,
        23: UTCTime,
    }
ASN1Types.INVERSE_TYPE_MAP = {ASN1Types.TYPE_MAP[x]: x for x in ASN1Types.TYPE_MAP}
