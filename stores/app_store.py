import requests
from lxml import etree

from . import country_codes
from .Model.review import AppStoreReview

# an other posible source:
# - http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStoreServices.woa/wa/wsLookup?id=343200656&country=us
# ${opts.country} ${opts.page} ${id}  sortby={}/${opts.sort}
# use xml because it has two more fields than the json updated and html - json also availible
_resource = 'https://itunes.apple.com/{}/rss/customerreviews/page={}/id={}/xml'


def reviews(app_id, country_code=None):
    """
    :param country_code:
    :param app_id: app id from itunes connect
    :param country:
    :return:
    """
    r = []
    codes = country_codes.keys() if country_code is None else [country_code]
    for code in codes:
        received = 1
        page = 1
        print('Reviews for ', code)
        while received > 0:
            url = _resource.format(code, page, app_id)  # , 'mostRecent'
            rx = _reviews(url)
            print('Page ', page, ' :', len(rx))
            r.extend(rx)
            received = len(rx)
            page += 1
    return r


def _reviews(url):
    content = requests.post(url).content
    tree = etree.fromstring(content)
    std_namespace = tree.nsmap[None]
    im_namespace = tree.nsmap['im']
    r = []
    # skip the first entry because its the itunes description and not a review
    first = True
    iter_child = tree.iter('{' + std_namespace + '}entry')
    itunes_entry = tree.find('{' + std_namespace + '}entry')
    if itunes_entry is not None:
        app_id = itunes_entry.find('{' + std_namespace + '}id').get('{'+im_namespace+'}id')
    for child in iter_child:
        if first:
            #TODO firstone ist showing up
            next(iter_child)
            first = False
        parsed_review = _parse_review(child)
        parsed_review.app_id = app_id
        r.append(parsed_review)

    return r


def _parse_review(entry, std_namespace='http://www.w3.org/2005/Atom', im_namespace='http://itunes.apple.com/rss'):
    review_id = entry.find('{' + std_namespace + '}id').xpath("string()")
    updated = entry.find('{' + std_namespace + '}updated').xpath("string()")
    #TODO get version for date?
    title = entry.find('{' + std_namespace + '}title').xpath("string()")  # title <title> text
    body = None
    for content in entry.iter('{' + std_namespace + '}content'):  # content < type="text"> text
        if content.get("type") == 'text':
            body = content.xpath("string()")
            break
        elif content.get("type") == 'html':
            #TODO
            pass
    rating = entry.find('{' + im_namespace + '}rating')  # rating <im:rating> text
    if rating is not None:
        rating = rating.xpath("string()")
    version = entry.find('{' + im_namespace + '}version')  # version <im:version> text
    if version is not None:
        version = version.xpath("string()")
    #TODO optimise just one find until name tag
    author = entry.find('{' + std_namespace + '}author')  # author_name <author><name> text
    author_name = None
    if author is not None:
        author_name = author.find('{' + std_namespace + '}name')
        if author_name is not None:
            author_name = author_name.xpath("string()")
    return AppStoreReview(None, review_id, author_name, updated, rating, title, body, version)