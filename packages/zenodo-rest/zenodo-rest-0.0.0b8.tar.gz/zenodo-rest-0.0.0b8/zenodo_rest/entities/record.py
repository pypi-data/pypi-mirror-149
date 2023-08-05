from dataclasses import dataclass
from typing import Optional

from zenodo_rest.entities.zenodo_file import ZenodoFile


@dataclass
class Record:
    created: str
    doi: str
    files: list[ZenodoFile]
    links: dict
    id: int
    metadata: dict
    owners: list[int]
    revision: int
    stats: dict
    updated: str
    conceptdoi: Optional[str] = None
    conceptrecid: Optional[str] = None
