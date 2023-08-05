from pydantic import BaseModel


class Doi(BaseModel):
    doi: str
    recid: str
