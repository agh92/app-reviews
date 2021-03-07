from stores.model.review import Review


class GooglePlayReview(Review):
    def __init__(
        self,
        app_id,
        review_id,
        author,
        date,
        stars,
        title,
        body,
        perma_link,
        raw,
    ):
        super().__init__(app_id, review_id, author, date, stars, title, body, raw)
        self.perma_link = perma_link
