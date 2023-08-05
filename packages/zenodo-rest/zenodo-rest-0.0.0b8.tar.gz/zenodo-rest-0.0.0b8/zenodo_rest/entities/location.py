from typing import Optional

from pydantic import BaseModel


class Location(BaseModel):
    lat: float
    lon: float
    place: str
    description: Optional[str] = None
