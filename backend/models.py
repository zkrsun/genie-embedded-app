from typing import Optional

from pydantic import BaseModel


class SpaceOut(BaseModel):
    name: str
    code: str
    url: str
    description: Optional[str] = None
    icon_code: Optional[str] = None
    access_count: int = 0
