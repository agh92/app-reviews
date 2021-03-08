from typing import Optional

import rx
from rx.core.typing import Disposable, Observable, Observer, Scheduler
from rx import operators as ops

from stores.google_play.parsing_functions import raw_reviews, _parse_reviews
from stores.model import App


class GooglePlayApp(App):
    def __init__(self, app_id: str, country_code: str):
        self._app_id = app_id
        self._country_code = country_code

    @property
    def app_id(self) -> str:
        return self._app_id

    @property
    def country_code(self) -> str:
        return self._country_code

    @property
    def reviews(self) -> Observable:
        pass
