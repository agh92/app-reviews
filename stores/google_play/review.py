import json

import pyquery

from stores.model import Review


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

    @staticmethod
    def from_html(html, app_id):
        div = pyquery.PyQuery(html)
        header = div("div.review-header").eq(0)
        review_info = header("div.review-info").eq(0)
        review_body = div("div.review-body").eq(0)
        # TODO follow permalink and get the full review
        if review_body("div.review-link").eq(0).attr("style") == "display:none":
            review_body.remove("div.review-link")
        return GooglePlayReview(
            app_id=app_id,
            review_id=header.attr("data-reviewid"),
            author=review_info("span.author-name").text(),
            date=review_info("span.review-date").text(),
            perma_link=review_info("a.reviews-permalink").attr("href"),
            stars=review_info("div.tiny-star").attr("aria-label"),
            title=review_body("span.review-title").text(),
            body=review_body.text(),
            raw=str(html),
        )

    @staticmethod
    def from_gp_json(gp_json, app_id, base_url):
        # version gp_json[10]
        return GooglePlayReview(
            app_id=app_id,
            review_id=gp_json[0],
            author=gp_json[1][0],
            date=gp_json[5][0],  # TODO calculate date from both items in array
            perma_link="{}/store/apps/details?id={}&reviewId={}".format(
                base_url, app_id, gp_json[0]
            ),
            stars=gp_json[2],
            title=None,  # there is no title in this data structure
            body=gp_json[4],
            raw=None,  # json.dump(gp_json),
        )
