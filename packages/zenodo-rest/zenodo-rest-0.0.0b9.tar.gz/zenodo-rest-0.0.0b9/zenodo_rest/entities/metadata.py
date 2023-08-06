from datetime import date
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel

from zenodo_rest.entities.community import Community
from zenodo_rest.entities.creator import Contributor, Creator
from zenodo_rest.entities.date_interval import DateInterval
from zenodo_rest.entities.doi import Doi
from zenodo_rest.entities.grant import Grant
from zenodo_rest.entities.location import Location
from zenodo_rest.entities.subject import Subject


class UploadType(str, Enum):
    publication = "publication"
    poster = "poster"
    presentation = "presentation"
    dataset = "dataset"
    image = "image"
    video_audio = "video"
    software = "software"
    lesson = "lesson"
    physical_object = "physicalobject"
    other = "other"


class PublicationType(str, Enum):
    annotation_collection = "annotationcollection"
    book = "book"
    section = "section"
    conference_paper = "conferencepaper"
    data_management_plan = "datamanagementplan"
    article = "article"
    patent = "patent"
    preprint = "preprint"
    deliverable = "deliverable"
    milestone = "milestone"
    proposal = "proposal"
    report = "report"
    software_documentation = "softwaredocumentation"
    taxonomic_treatment = "taxonomictreatment"
    technical_note = "technicalnote"
    thesis = "thesis"
    working_paper = "workingpaper"
    other = "other"


class ImageType(str, Enum):
    figure = "figure"
    plot = "plot"
    drawing = "drawing"
    diagram = "diagram"
    photo = "photo"
    other = "other"


class AccessRight(str, Enum):
    open = "open"
    embargoed = "embargoed"
    restricted = "restricted"
    closed = "closed"


class Metadata(BaseModel):
    upload_type: UploadType = UploadType.other
    publication_type: Optional[PublicationType] = None
    image_type: Optional[ImageType] = None
    publication_date: str = date.today().isoformat()
    title: str = "Placeholder"
    creators: list[Creator] = [Creator()]
    description: str = "Placeholder"
    access_right: AccessRight = AccessRight.open
    license: Optional[str] = None
    embargo_date: Optional[date] = None
    access_conditions: Optional[str] = None
    doi: Optional[str] = None
    prereserve_doi: Optional[Union[Doi, bool]] = None
    keywords: Optional[list[str]] = None
    notes: Optional[str] = None
    related_identifiers: Optional[list[object]] = None
    contributors: Optional[list[Contributor]] = None
    references: Optional[list[str]] = None
    communities: Optional[list[Community]] = None
    grants: Optional[list[Grant]] = None
    journal_title: Optional[str] = None
    journal_volume: Optional[str] = None
    journal_issue: Optional[str] = None
    journal_pages: Optional[str] = None
    conference_title: Optional[str] = None
    conference_acronym: Optional[str] = None
    conference_dates: Optional[str] = None
    conference_place: Optional[str] = None
    conference_url: Optional[str] = None
    conference_session: Optional[str] = None
    conference_session_part: Optional[str] = None
    imprint_publisher: Optional[str] = None
    imprint_isbn: Optional[str] = None
    imprint_place: Optional[str] = None
    partof_title: Optional[str] = None
    partof_pages: Optional[str] = None
    thesis_supervisors: Optional[list[Creator]] = None
    thesis_university: Optional[str] = None
    subjects: Optional[list[Subject]] = None
    version: Optional[str] = None
    language: Optional[str] = None
    locations: Optional[list[Location]] = None
    dates: Optional[list[DateInterval]] = None
    method: Optional[str] = None
