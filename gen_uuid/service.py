import uuid


class UUID:
    def create_uuid4(self) -> str:
        return str(uuid.uuid4())
    
    def create_uuid3(self, text: str) -> str:
        return str(uuid.uuid3(uuid.NAMESPACE_OID, text))
    
    def create_uuid5(self, text: str) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_OID, text))
