import string, random


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

        if not characters:
            raise ValueError("You must select at least one character type.")

        return ''.join(random.choice(characters) for _ in range(length))
