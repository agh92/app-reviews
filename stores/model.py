import json
from abc import ABC, abstractmethod

from rx.core.typing import Observable


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


class Review:
    def __init__(self, app_id, review_id, author, date, stars, title, body, raw):
        self.id = review_id
        self.date = date
        self.title = title
        self.body = body
        self.app_id = app_id
        self.stars = stars
        self.author = author
        self.raw = raw

    # NICE TO HAVE implement __eq__ and __hash__ to drop duplicates form countries that return the same reviews
    # def __eq__(self, other):
    #    return self.__dict__ == other.__dict__

    def to_json(self):
        return json.dumps(
            {k: v for k, v in self.__dict__.items() if not isinstance(v, bytes)}
        )
