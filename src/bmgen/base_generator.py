from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    @abstractmethod
    def add(self, line):
        raise NotImplementedError()

    @abstractmethod
    def generate(self):
        raise NotImplementedError()
