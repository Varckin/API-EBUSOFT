from pydantic import BaseModel


class URLEncodeRequest(BaseModel):
    text: str
    safe: str = ""  # characters that do NOT need to be encoded (by default, everything is encoded)


class URLEncodeResponse(BaseModel):
    encoded: str


class URLDecodeRequest(BaseModel):
    text: str


class URLDecodeResponse(BaseModel):
    decoded: str
