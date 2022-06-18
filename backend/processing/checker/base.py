import abc

from backend.processing.result import FileResults, Result


class BaseChecker(abc.ABC):
    @abc.abstractmethod
    def run(self) -> list[Result]:
        pass


class BaseMultiChecker(abc.ABC):
    @abc.abstractmethod
    def run(self) -> list[FileResults]:
        pass
