import abc

from backend.processing.result import Result


class BaseChecker(abc.ABC):
    @abc.abstractmethod
    def run(self) -> list[Result]:
        pass

    def sort_results(self):
        pass
