import json
import time

import requests
from pyquery import PyQuery as pq

from stores import country_codes, google_play_delay
from stores.Model.review import GooglePlayReview
from lxml.etree import tostring

# this reviews_resource have been exposed by several github projects
_reviews_resource = 'https://play.google.com/store/getreviews'

_review_api_data = {
    'pageNum': 0,
    'id': None,
    'reviewSortOrder': 0,
    'hl': 'en',
    'reviewType': 0,
    'xhr': 1
}


def reviews(app_id, country_code=None):
    _review_api_data['id'] = app_id
    r = []
    codes = country_codes.keys() if country_code is None else [country_code]
    for code in codes:
        _review_api_data['hl'] = code
        do = True
        while do:
            print('Request reviews for page ', _review_api_data['pageNum'])
            response = requests.post(_reviews_resource, data=_review_api_data)
            body = response.text[6:]  # the first 6 characters of the response make the json invalid
            # print(body)
            # encode utf8 for possible emojies
            reviews_str = json.loads(body)[0][2].strip().encode(
                'utf-8')  # the body contains a list with in a list -> xml/html format
            if len(reviews_str):
                d = pq(reviews_str)
                divs = d('div.single-review')
                r.extend([_parse_review(pq(tostring(div)), app_id) for div in divs if len(div)])
                _review_api_data['pageNum'] += 1
            else:  # if the string is empty there are no more reviews to process
                do = False
            time.sleep(google_play_delay[0])  # don´t let google block us
        _review_api_data['pageNum'] = 0
        time.sleep(google_play_delay[1])
    return r


def _parse_review(div, app_id):
    header = div('div.review-header').eq(0)
    review_id = header.attr('data-reviewid')  # div.review-header data-reviewid
    review_info = header('div.review-info').eq(0)
    author = review_info('span.author-name').text()
    date = review_info('span.review-date').text()  # div.review-header div.review-info span.review-date text
    perma_link = review_info('a.reviews-permalink').attr(
        'href')  # div.review-header div.review-info a.reviews-permalink href
    stars = review_info('div.tiny-star').attr(
        'aria-label')  # div.review-header div.review-info div.tiny-star star-rating-non-editable-container aria-label
    review_body = div('div.review-body').eq(0)
    title = review_body('span.review-title').text()  # div.review-body with-review-wrapper span.review-title text
    body = review_body.text()  # div.review-body with-review-wrapper text
    return GooglePlayReview(app_id=app_id,
                            review_id=review_id,
                            author=author,
                            date=date,
                            perma_link=perma_link,
                            stars=stars,
                            title=title,
                            body=body)