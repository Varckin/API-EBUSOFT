from fastapi import HTTPException
import random, nanoid, string


def generate_shortid(length: int, alphabet: str | None = None) -> str:
    """Simple ShortID implementation with optional custom alphabet"""
    if alphabet is None:
        alphabet = string.ascii_letters + string.digits + "_-"
    return "".join(random.choices(alphabet, k=length))

def generate_identifier(type_: str, length: int, alphabet: str | None = None) -> str:
    """
    Generate an identifier based on type:
    - 'shortid' -> ShortID
    - 'nanoid' -> NanoID
    """
    if type_ == "shortid":
        return generate_shortid(length, alphabet)
    elif type_ == "nanoid":
        return nanoid.generate(alphabet=alphabet, size=length) if alphabet else nanoid.generate(size=length)
    else:
        # This block is nearly unreachable but kept for safety
        raise HTTPException(status_code=400, detail="Invalid identifier type")
