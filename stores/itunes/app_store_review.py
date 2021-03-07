from feedparser import FeedParserDict

from stores.Model.review import Review


class AppStoreReview(Review):
    def __init__(
        self, app_id, review_id, author, date, stars, title, body, version, raw
    ):
        super().__init__(app_id, review_id, author, date, stars, title, body, raw)
        self.version = version

    @staticmethod
    def from_feed_entry(entry: FeedParserDict, app_id: str):
        # see https://feedparser.readthedocs.io/en/latest/common-atom-elements.html for more detail
        # TODO is it posible to get the xml entry and use it as raw
        # language is also available here but is not really the language of the review is the country code
        # href also available but its of no help because it redirects to the AppStore
        return AppStoreReview(
            app_id=app_id,
            review_id=entry.id,
            author=entry.author,
            date=entry.updated,
            stars=entry.im_rating,
            title=entry.title,
            version=entry.im_version,
            body=entry.summary,
            raw=next(
                filter(lambda content: content.type == "text/html", entry.content)
            ).value,
        )
