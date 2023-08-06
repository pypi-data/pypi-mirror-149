from dataclasses import dataclass


@dataclass
class ZenodoFile:
    bucket: str
    checksum: str
    key: str
    links: dict
    size: int
    type: str
