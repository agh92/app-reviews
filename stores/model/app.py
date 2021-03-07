from abc import ABC, abstractmethod

from rx import Observable


class App(ABC):
    @property
    @abstractmethod
    def app_id(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def country_code(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def reviews(self) -> Observable:
        return NotImplemented
