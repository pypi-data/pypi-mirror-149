class SNMP:

    SNMPv1_TRAP = "SNMPv1_TRAP"
    SNMP_INFORM = "SNMP_INFORM"
    SNMPv2_TRAP = "SNMPv2_TRAP"

    TYPE_MAP = {
        4: SNMPv1_TRAP,
        6: SNMP_INFORM,
        7: SNMPv2_TRAP,
    }

    def parse_tag_type(self, node: tuple, tag: int):
        if node == (2,):
            if self.TYPE_MAP.get(tag) is None:
                raise NotImplementedError("SNMP tag type {tag} has no mapping".format(tag=tag))
            return self.TYPE_MAP[tag]
        else:
            return None
SNMP.INVERSE_TYPE_MAP = {SNMP.TYPE_MAP[x]: x for x in SNMP.TYPE_MAP}
