
from enum import Enum
from typing import TypedDict


class Status(str, Enum):
    ERROR = "Error"
    WARNING = "Warning"
    PASS = "Passing"

    def __repr__(self):
        if self == Status.ERROR:
            return "Error"
        elif self == Status.WARNING:
            return "Warning"
        elif self == Status.PASS:
            return "Pass"




class Result(TypedDict):
    title: str
    comments: str
    status: Status
