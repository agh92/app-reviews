import json


class Review:
    def __init__(self, app_id, review_id, author, date, stars, title, body):
        self.id = review_id
        self.date = date
        self.title = title
        self.body = body
        self.app_id = app_id
        self.stars = stars
        self.author = author

    def to_json(self):
        return json.dumps(self.__dict__)


class GooglePlayReview(Review):

    def __init__(self, app_id, review_id, author, date, stars, title, body, perma_link):
        super().__init__(app_id, review_id, author, date, stars, title, body)
        self.perma_link = perma_link


class AppStoreReview(Review):

    def __init__(self, app_id, review_id, author, date, stars, title, body, version):
        super().__init__(app_id, review_id, author, date, stars, title, body)
        self.version = version
