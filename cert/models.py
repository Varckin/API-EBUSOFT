from typing import List, Optional
from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    domain: str = Field(..., description="Domain to search for (e.g., example.com)")
    exact: bool = Field(False, description="Exact match without wildcard")
    include_expired: bool = Field(True, description="Include expired certificates")


class CrtShRawItem(BaseModel):
    issuer_ca_id: Optional[int] = None
    issuer_name: Optional[str] = None
    common_name: Optional[str] = None
    name_value: Optional[str] = None
    id: Optional[int] = None
    entry_timestamp: Optional[str] = None
    not_before: Optional[str] = None
    not_after: Optional[str] = None
    serial_number: Optional[str] = None


class CrtShItem(BaseModel):
    id: int
    common_name: Optional[str] = None
    names: List[str] = []
    issuer_name: Optional[str] = None
    entry_timestamp: Optional[str] = None
    not_before: Optional[str] = None
    not_after: Optional[str] = None
    serial_number: Optional[str] = None
