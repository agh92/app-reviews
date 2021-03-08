import json
from typing import Optional

import rx
from rx.core.typing import Disposable, Observable, Observer, Scheduler
from rx import operators as ops

from stores.google_play.parsing_functions import raw_reviews
from stores.google_play.review import GooglePlayReview
from stores.model import App

base_url = "https://play.google.com"


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
        return rx.create(self._fetch)

    def _fetch(self, observer: Observer, scheduler: Optional[Scheduler]) -> Disposable:
        return (
            rx.of(raw_reviews(self.app_id, self.country_code, 0.1))
            .pipe(
                # the first 6 characters of the response make the json invalid
                ops.map(lambda text: text[5:]),
                ops.map(lambda fixed_text: json.loads(fixed_text)),
                ops.map(lambda top_object: top_object[0][2]),
                ops.map(lambda raw_data: json.loads(raw_data)),
                # TODO there is no need for this when the content is html
                ops.map(lambda json_array: json_array[0]),
                ops.flat_map(lambda rev: rev),
                ops.map(
                    lambda gp_json: GooglePlayReview.from_gp_json(
                        gp_json, self.app_id, base_url
                    )
                ),
            )
            .subscribe(observer)
        )
