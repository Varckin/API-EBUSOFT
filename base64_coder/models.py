from pydantic import BaseModel


class StringRequest(BaseModel):
    data: str
    action: str  # 'encode' or 'decode'

class StringResponse(BaseModel):
    result: str
