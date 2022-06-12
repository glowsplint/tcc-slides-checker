import abc

from backend.processing.result import FileResults, Result


class BaseChecker(abc.ABC):
    @abc.abstractmethod
    def run(self) -> list[FileResults]:
        pass

    @abc.abstractmethod
    def run_single(self) -> list[Result]:
        pass
