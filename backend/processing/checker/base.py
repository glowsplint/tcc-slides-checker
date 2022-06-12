import abc

from backend.processing.result import Result


class BaseChecker(abc.ABC):
    @abc.abstractmethod
    def run_single(self) -> list[Result]:
        pass
