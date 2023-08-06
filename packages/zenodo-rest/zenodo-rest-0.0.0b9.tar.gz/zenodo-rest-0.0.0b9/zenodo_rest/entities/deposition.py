import os
from typing import Optional, TypeVar


import requests
from pydantic import BaseModel

from zenodo_rest.entities.deposition_file import DepositionFile
from zenodo_rest.entities.metadata import Metadata
from zenodo_rest import exceptions

T = TypeVar("Deposition")

class Deposition(BaseModel):
    created: str
    doi: Optional[str]
    doi_url: Optional[str]
    files: Optional[list[DepositionFile]]
    id: str
    links: dict
    metadata: Metadata
    modified: str
    owner: int
    record_id: int
    record_url: Optional[str]
    state: str
    submitted: bool
    title: str

    @staticmethod
    def retrieve(
        deposition_id: str, token: Optional[str] = None, base_url: Optional[str] = None
    ) -> T:
        if token is None:
            token = os.getenv("ZENODO_TOKEN")
        if base_url is None:
            base_url = os.getenv("ZENODO_URL")
        header = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

        response = requests.get(
            f"{base_url}/api/deposit/depositions/{deposition_id}",
            headers=header,
        )

        response.raise_for_status()
        return Deposition.parse_obj(response.json())

    def refresh(self, token: str = None) -> Optional[T]:
        return Deposition.retrieve(self.id, token)

    def get_latest(self, token: str = None) -> Optional[T]:

        deposition: Deposition = self.refresh(token)
        latest_url = deposition.links.get("latest", None)
        if latest_url is None:
            return deposition.refresh()
        latest_id = latest_url.rsplit("/", 1)[1]
        return Deposition.retrieve(latest_id)

    def get_latest_draft(self, token: str = None) -> Optional[T]:
        deposition: Deposition = self.refresh(token)
        latest_draft_url = deposition.links.get("latest_draft", None)
        if latest_draft_url is None:
            raise exceptions.NoDraftFound(deposition.id)

        if token is None:
            token = os.getenv("ZENODO_TOKEN")

        header = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        response = requests.get(
            latest_draft_url,
            headers=header,
        )
        response.raise_for_status()
        return Deposition.parse_obj(response.json())

    def get_bucket(self) -> str:
        return self.links.get("bucket")

    def delete_file(self, file_id: str, token: str = None, base_url: str = None) -> int:
        if token is None:
            token = os.getenv("ZENODO_TOKEN")
        if base_url is None:
            base_url = os.getenv("ZENODO_URL")
        header = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

        response = requests.delete(
            f"{base_url}/api/deposit/depositions/{self.id}/files/{file_id}",
            headers=header,
        )

        response.raise_for_status()
        return response.status_code

    def delete_files(self, token: str = None, base_url: str = None) -> list[int]:
        return [self.delete_file(file.id, token, base_url) for file in self.files]
