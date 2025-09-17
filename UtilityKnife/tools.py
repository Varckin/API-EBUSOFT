import uuid, string, random


class UUID:
    def create_uuid4(self) -> str:
        return str(uuid.uuid4())
    
    def create_uuid3(self, text: str) -> str:
        return str(uuid.uuid3(uuid.NAMESPACE_OID, text))
    
    def create_uuid5(self, text: str) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_OID, text))


class GeneratorPass:
    def gen_pass(self, length: int, use_lower:bool,
                 use_upper: bool, use_digits: bool,
                 use_special: bool) -> str:
        characters: str = ''

        if use_lower:
            characters += string.ascii_lowercase
        if use_upper:
            characters += string.ascii_uppercase
        if use_digits:
            characters += string.digits
        if use_special:
            characters += string.punctuation

        return ''.join(random.choice(characters) for _ in range(length))
