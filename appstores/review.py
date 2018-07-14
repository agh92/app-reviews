import json


class Review:
    def __init__(self, app_id, review_id, author, date, perma_link, stars, title, body):
        self.app_id = app_id
        self.id = review_id
        self.author = author
        self.date = date
        self.perma_link = perma_link
        self.stars = stars
        self.title = title
        self.body = body

    def to_json(self):
        return json.dumps({
            'app_id': self.app_id,
            'review_id': self.id,
            'author': self.author,
            'date': self.date,
            'perma_link': self.perma_link,
            'stars': self.stars,
            'title': self.title,
            'body': self.body
        })
