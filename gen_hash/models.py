from pydantic import BaseModel
from typing import List, Optional


class HashRequest(BaseModel):
    text: str
    algorithms: Optional[List[str]] = None  # If None, use default_algorithms
