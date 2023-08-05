from pydantic import BaseModel


class BucketFile(BaseModel):
    key: str  # filename
    mimetype: str
    checksum: str
    version_id: str
    size: int
    created: str
    updated: str
    links: dict
    is_head: bool
    delete_marker: bool
