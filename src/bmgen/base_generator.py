from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    def __init__(self):
        self.context = []

    @abstractmethod
    def add(self, line):
        raise NotImplementedError()

    @abstractmethod
    def generate(self):
        raise NotImplementedError()

    @abstractmethod
    def ast(self):
        raise NotImplementedError()
