from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Creator(BaseModel):
    name: str = "Placeholder"
    affiliation: Optional[str] = None
    orcid: Optional[str] = None
    gnd: Optional[str] = None


class ContributorType(Enum):
    contact_person = "ContactPerson"
    data_collector = "DataCollector"
    data_curator = "DataCurator"
    data_manager = "DataManager"
    distributor = "Distributor"
    editor = "Editor"
    funder = "Funder"
    hosting_institution = "HostingInstitution"
    producer = "Producer"
    project_leader = "ProjectLeader"
    project_manager = "ProjectManager"
    registration_agency = "RegistrationAgency"
    registration_authority = "RegistrationAuthority"
    related_person = "RelatedPerson"
    researcher = "Researcher"
    research_group = "ResearchGroup"
    rights_holder = "RightsHolder"
    supervisor = "Supervisor"
    sponsor = "Sponsor"
    work_package_leader = "WorkPackageLeader"
    other = "Other"


class Contributor(Creator):
    type: ContributorType
