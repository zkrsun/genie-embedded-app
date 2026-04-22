from typing import List, Optional
from pydantic import BaseModel


class SpaceOut(BaseModel):
    name: str
    code: str
    url: str
    description: Optional[str] = None


class DomainOut(BaseModel):
    name: str
    code: str
    spaces: List[SpaceOut]
    description: Optional[str] = None


class BuOut(BaseModel):
    name: str
    code: str
    domains: List[DomainOut]
    description: Optional[str] = None
