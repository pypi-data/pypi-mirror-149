from typing import Optional

from pydantic import BaseModel


class Subject(BaseModel):
    term: str
    identifier: str
    scheme: Optional[str]
