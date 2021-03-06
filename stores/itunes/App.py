import rx

from stores.itunes.functions import _parse_reviews, raw_reviews


class App:
    def __init__(self, app_id: str, country_code: str):
        self.app_id = app_id
        self.country_code = country_code
        # TODO define pipe
        self.reviews = rx.create(self._fetch_reviews)

    def _fetch_reviews(self, observer, scheduler):
        for raw_review in raw_reviews(self.app_id, self.country_code):
            observer.on_next(_parse_reviews(raw_review[1], self.app_id))
        observer.on_completed()
