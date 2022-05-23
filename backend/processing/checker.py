import abc


class Checker(abc.ABC):
    @abc.abstractmethod
    def run(self):
        pass
