from enum import Enum
from typing import Optional

from pydantic import BaseModel


class DateIntervalType(Enum):
    collected = "Collected"
    valid = "Valid"
    withdrawn = "Withdrawn"


class DateInterval(BaseModel):
    # at least start or end must be defined
    start: Optional[str] = None
    end: Optional[str] = None
    type: DateIntervalType
    description: Optional[str] = None
