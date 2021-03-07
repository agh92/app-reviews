import json
import time

import requests
from pyquery import PyQuery as pq
from lxml.etree import tostring

import stores
from stores import country_codes
from stores.Model.review import GooglePlayReview

_warning_msg = "Our systems have detected unusual traffic from your computer network"
# this reviews_resource have been exposed by several github projects
_reviews_resource = "https://play.google.com/store/getreviews"


def _default_request_data(app_id):
    return {
        "pageNum": 0,
        "id": app_id,
        "reviewSortOrder": 0,
        "hl": "en",
        "reviewType": 0,
        "xhr": 1,
    }


def raw_reviews(app_id, delay=0, country_code=None):
    if stores.VERBOSE:
        print("Id: ", app_id)
    r = []
    _review_api_data = _default_request_data(app_id)
    for code in _country_codes(country_code):
        _review_api_data["hl"] = code
        _review_api_data["pageNum"] = 0
        reviews_str = "1"
        if stores.VERBOSE:
            print("Country ", _review_api_data["hl"])
        while len(reviews_str):
            response = requests.post(_reviews_resource, data=_review_api_data)
            # the first 6 characters of the response make the json invalid
            body = response.text[6:]
            # the body contains a list with in a list -> xml/html format - encode utf8 -> emojies
            try:
                # if the string is empty there are no more reviews to process
                reviews_str = (
                    json.loads(body, encoding=response.encoding)[0][2]
                    .strip()
                    .encode(response.encoding)
                )
                _review_api_data["pageNum"] += 1
                if stores.VERBOSE:
                    print(
                        "Page: ",
                        _review_api_data["pageNum"],
                        " len ",
                        str(len(reviews_str)),
                    )
                tpl = (response.text, response.content)
                if len(reviews_str) and tpl not in r:
                    r.append(tpl)
            except:
                if body.find(_warning_msg) != -1:
                    raise GooglePlayException("Ip blocked by Google")
                raise
            time.sleep(delay)
    return r


def reviews(app_id, delay=0, country_code=None, parsing_fn=None):
    if parsing_fn is None:
        parsing_fn = _parse_reviews
    r = []
    for raw_review in raw_reviews(app_id, delay, country_code):
        r.extend(parsing_fn(raw_review[0], app_id))
    return r


def _country_codes(country_code):
    if isinstance(country_code, str):
        return [country_code]
    elif isinstance(country_code, list) or isinstance(country_code, set):
        return country_code
    else:  # if len(country_code) == 0 or country_code is None:
        return country_codes.keys()


def _parse_reviews(raw_review, app_id):
    # the first 6 characters of the response make the json invalid
    body = raw_review[6:]
    reviews_str = json.loads(body, encoding="utf-8")[0][2].strip().encode("utf-8")
    divs = pq(reviews_str)("div.single-review")
    return [_parse_review(tostring(div), app_id) for div in divs if len(div)]


def _parse_review(xml_string, app_id):
    div = pq(xml_string)
    header = div("div.review-header").eq(0)
    # div.review-header data-reviewid
    review_id = header.attr("data-reviewid")
    review_info = header("div.review-info").eq(0)
    author = review_info("span.author-name").text()
    # div.review-header div.review-info span.review-date text
    date = review_info("span.review-date").text()
    # div.review-header div.review-info a.reviews-permalink href
    perma_link = review_info("a.reviews-permalink").attr("href")
    # div.review-header div.review-info div.tiny-star star-rating-non-editable-container aria-label
    stars = review_info("div.tiny-star").attr("aria-label")
    review_body = div("div.review-body").eq(0)
    # div.review-body with-review-wrapper span.review-title text
    title = review_body("span.review-title").text()
    # div.review-body with-review-wrapper text
    if review_body("div.review-link").eq(0).attr("style") == "display:none":
        review_body.remove("div.review-link")
    elif stores.VERBOSE:
        print("WARNING: NO IMPLEMENTATION")
        # TODO follow permalink and get the full review
    body = review_body.text()
    return GooglePlayReview(
        app_id=app_id,
        review_id=review_id,
        author=author,
        date=date,
        perma_link=perma_link,
        stars=stars,
        title=title,
        body=body,
        raw=str(xml_string),
    )


class GooglePlayException(Exception):
    pass
