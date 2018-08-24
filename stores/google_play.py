import json
import time

import requests
from pyquery import PyQuery as pq

from stores import country_codes, request_delay
from stores.Model.review import GooglePlayReview
from lxml.etree import tostring

_warning_msg = 'Our systems have detected unusual traffic from your computer network'
# this reviews_resource have been exposed by several github projects
_reviews_resource = 'https://play.google.com/store/getreviews'


def reviews(app_id, delay=0, country_code=None, parsing_fn=None):
    if parsing_fn is None:
        parsing_fn = _parse_review

    _review_api_data = {
        'pageNum': 0,
        'id': app_id,
        'reviewSortOrder': 0,
        'hl': 'en',
        'reviewType': 0,
        'xhr': 1
    }
    r = []
    for code in _get(country_code):
        _review_api_data['hl'] = code
        print('Country ', _review_api_data['hl'])
        reviews_str = "1"
        while len(reviews_str):
            response = requests.post(_reviews_resource, data=_review_api_data)
            body = response.text[6:]  # the first 6 characters of the response make the json invalid
            # the body contains a list with in a list -> xml/html format - encode utf8 -> emojies
            try:
                # if the string is empty there are no more reviews to process
                reviews_str = json.loads(body)[0][2].strip().encode('utf-8')
                if len(reviews_str):
                    divs = pq(reviews_str)('div.single-review')
                    rx = [parsing_fn(tostring(div), app_id) for div in divs if len(div)]
                    print('Page ', _review_api_data['pageNum'], ' :', len(rx))
                    r.extend(rx)
                    _review_api_data['pageNum'] += 1
            except json.decoder.JSONDecodeError as e:  # Google Probably blocked us
                if body.find(_warning_msg) != -1:
                    raise GooglePlayExceoption('Ip blocked by Google')
                else:
                    print('Error with code ', code)
                break
            time.sleep(delay)  # don´t let google block us
        _review_api_data['pageNum'] = 0
        time.sleep(delay)
    return r


def _get(country_code):
    if isinstance(country_code, str):
        return [country_code]
    elif isinstance(country_code, list) or isinstance(country_code, set):
        return country_code
    else:  # if len(country_code) == 0 or country_code is None:
        return country_codes.keys()


def _parse_review(xml_string, app_id):
    div = pq(xml_string)
    header = div('div.review-header').eq(0)
    # div.review-header data-reviewid
    review_id = header.attr('data-reviewid')
    review_info = header('div.review-info').eq(0)
    author = review_info('span.author-name').text()
    # div.review-header div.review-info span.review-date text
    date = review_info('span.review-date').text()
    # div.review-header div.review-info a.reviews-permalink href
    perma_link = review_info('a.reviews-permalink').attr('href')
    # div.review-header div.review-info div.tiny-star star-rating-non-editable-container aria-label
    stars = review_info('div.tiny-star').attr('aria-label')
    review_body = div('div.review-body').eq(0)
    # div.review-body with-review-wrapper span.review-title text
    title = review_body('span.review-title').text()
    # div.review-body with-review-wrapper text
    body = review_body.text()
    return GooglePlayReview(app_id=app_id,
                            review_id=review_id,
                            author=author,
                            date=date,
                            perma_link=perma_link,
                            stars=stars,
                            title=title,
                            body=body,
                            raw_review=None)


class GooglePlayExceoption(Exception):
    pass
