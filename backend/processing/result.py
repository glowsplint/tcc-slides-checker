
from enum import Enum
from typing import TypedDict


class Status(Enum):
    ERROR = 2
    WARNING = 1
    PASS = 0

    def __repr__(self):
        if self == Status.ERROR:
            return "Error"
        elif self == Status.WARNING:
            return "Warning"
        elif self == Status.PASS:
            return "Pass"

    def __lt__(self, other) -> bool:
        return self.value < other.value



class Result(TypedDict):
    title: str
    comments: str
    status: Status
