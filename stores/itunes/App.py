import requests
import rx
from lxml import etree
from rx import operators as ops

from stores.itunes.parsing_functions import parse_review, XMLNS

# an other possible source:
# http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStoreServices.woa/wa/wsLookup?id=343200656&country=us
# ${opts.country} ${opts.page} ${id}  sortby={}/${opts.sort}
# use xml because it has two more fields than the json: updated and html - json also available
_resource = "https://itunes.apple.com/{}/rss/customerreviews/page={}/id={}/sortBy=mostRecent/xml"


class App:
    def __init__(self, app_id: str, country_code: str):
        self.app_id = app_id
        self.country_code = country_code
        self.reviews = rx.create(self._fetch_reviews).pipe(
            ops.flat_map(lambda xml_tree: xml_tree),
            ops.filter(
                lambda xml_review: any(
                    content.get("type") == "text"
                    for content in xml_review.iter(XMLNS + "content")
                )
            ),
            ops.map(lambda xml_review: parse_review(xml_review, self.app_id)),
        )

    def _fetch_reviews(self, observer, scheduler):
        received = 1
        page = 1
        while received > 0:
            revs = self._get_page(page)
            observer.on_next(revs)
            received = len(revs)
            page += 1
            if received > 0:
                break
        observer.on_completed()

    def _get_page(self, page: int) -> []:
        url = _resource.format(self.country_code, page, self.app_id)
        resp = requests.post(url)
        tree = etree.fromstring(resp.content)
        # skip the first entry because its the itunes description and not a review
        return list(tree.iter(XMLNS + "entry"))
