from pydantic import BaseModel, Field
from os import getenv


class AnonimMail(BaseModel):
    anonmail_base_url: str = Field(
        default=getenv('ANONMAIL_BASE'),
        description="Base URL for the Anonymous Mail API"
    )
    timeout: int = Field(
        default=10,
        description="Request timeout in seconds"
    )


CONFIG = AnonimMail()
