from jasn1.asn1.types import *

class LDAPMessage(SEQUENCE):
    pass

class MessageID(ENUMERATED):
    pass

class BindRequest(SEQUENCE):
	pass

class BindResponse(SEQUENCE):
    pass

class UnbindRequest(SEQUENCE):
	pass

class SearchRequest(SEQUENCE):
	pass

class SearchResultEntry(SEQUENCE):
	pass

class SearchResultDone(SEQUENCE):
	pass

class SearchResultReference(SEQUENCE):
	pass

class ModifyRequest(SEQUENCE):
	pass

class ModifyResponse(SEQUENCE):
	pass

class AddRequest(SEQUENCE):
	pass

class AddResponse(SEQUENCE):
	pass

class DelRequest(SEQUENCE):
	pass

class DelResponse(SEQUENCE):
	pass

class ModifyDNRequest(SEQUENCE):
	pass

class ModifyDNResponse(SEQUENCE):
	pass

class CompareRequest(SEQUENCE):
	pass

class CompareResponse(SEQUENCE):
	pass

class AbandonRequest(SEQUENCE):
	pass

class ExtendedRequest(SEQUENCE):
	pass

class ExtendedResponse(SEQUENCE):
	pass

class LDAP_SUCCESS(ENUMERATED):
    pass

class LDAP_OPERATIONS_ERROR(ENUMERATED):
    pass
