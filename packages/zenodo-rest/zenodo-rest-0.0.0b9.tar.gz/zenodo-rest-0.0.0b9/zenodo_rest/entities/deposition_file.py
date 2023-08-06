from typing import Optional

from pydantic import BaseModel


class DepositionFile(BaseModel):
    id: str
    filename: str
    filesize: str
    checksum: str
    links: Optional[dict] = None
