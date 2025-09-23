from pydantic import BaseModel

class EncryptResponse(BaseModel):
    ciphertext: str
    nonce: str
    tag: str
    filename: str | None = None


class DecryptResponse(BaseModel):
    plaintext: str | None = None
    filename: str | None = None
    content_b64: str | None = None
