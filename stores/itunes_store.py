import time

import requests
from lxml import etree
from lxml.etree import tostring

from . import country_codes, VERBOSE
from .Model.review import AppStoreReview

# an other posible source:
# - http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStoreServices.woa/wa/wsLookup?id=343200656&country=us
# ${opts.country} ${opts.page} ${id}  sortby={}/${opts.sort}
# use xml because it has two more fields than the json updated and html - json also availible
_resource = 'https://itunes.apple.com/{}/rss/customerreviews/page={}/id={}/xml'


def raw_reviews(app_id, country_code=None):
    if VERBOSE:
        print('Id: ', app_id)
    r = []
    for code in _country_codes(country_code):
        received = 1
        page = 1
        if VERBOSE:
            print('Country ', code)
        while received > 0:
            url = _resource.format(code, page, app_id)  # , 'mostRecent'
            resp = requests.post(url)
            tree = etree.fromstring(resp.content)
            received = len(list(tree.iter('{' + tree.nsmap[None] + '}entry')))
            if VERBOSE:
                print('Page ', page, ' len ', str(received))
            page += 1
            if received > 0:
                # TODO check that content is not in the list so we dont add duplicates in the list
                r.append((resp.text, resp.content))
    return r


def reviews(app_id, country_code=None, parsing_fn=None):
    if parsing_fn is None:
        parsing_fn = _parse_reviews
    r = []
    for raw_review in raw_reviews(app_id, country_code):
        r.extend(parsing_fn(raw_review[1]))
    return r


def _country_codes(country_code):
    if isinstance(country_code, str):
        return [country_code]
    elif isinstance(country_code, list) or isinstance(country_code, set):
        return country_code
    else:  # if len(country_code) == 0 or country_code is None:
        return country_codes.keys()


def _parse_reviews(content):
    tree = etree.fromstring(content)
    std_namespace = tree.nsmap[None]
    im_namespace = tree.nsmap['im']
    r = []
    # skip the first entry because its the itunes description and not a review
    iter_child = tree.iter('{' + std_namespace + '}entry')
    itunes_entry = tree.find('{' + std_namespace + '}entry')
    if itunes_entry is not None:  # the first entry is itunes information not review
        app_id = itunes_entry.find('{' + std_namespace + '}id').get('{' + im_namespace + '}id')
    else:
        app_id = None
    for child in iter_child:
        parsed_review = _parse_review(child)
        parsed_review.app_id = app_id
        r.append(parsed_review)
    return r


def _parse_review(entry, std_namespace='http://www.w3.org/2005/Atom', im_namespace='http://itunes.apple.com/rss'):
    raw = tostring(entry)
    review_id = entry.find('{' + std_namespace + '}id').xpath("string()")
    updated = entry.find('{' + std_namespace + '}updated').xpath("string()")
    title = entry.find('{' + std_namespace + '}title').xpath("string()")  # title <title> text
    body = None
    html = None
    for content in entry.iter('{' + std_namespace + '}content'):  # content < type="text"> text
        if content.get("type") == 'text':
            body = content.xpath("string()")
        if content.get("type") == 'html':
            html = content.xpath("string()")
    rating = entry.find('{' + im_namespace + '}rating')  # rating <im:rating> text
    if rating is not None:
        rating = rating.xpath("string()")
    version = entry.find('{' + im_namespace + '}version')  # version <im:version> text
    if version is not None:
        version = version.xpath("string()")
    # TODO optimise just one find until name tag
    author = entry.find('{' + std_namespace + '}author')  # author_name <author><name> text
    author_name = None
    if author is not None:
        author_name = author.find('{' + std_namespace + '}name')
        if author_name is not None:
            author_name = author_name.xpath("string()")
    return AppStoreReview(None, review_id, author_name, updated, rating, title, body, version, raw, html)
