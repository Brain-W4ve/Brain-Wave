from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def process(self, file_data):
        ...