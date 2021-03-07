from typing import Optional

import requests
import rx
from lxml import etree
from rx import operators as ops
from rx.core import Observer
from rx.disposable import Disposable
from rx.scheduler.scheduler import Scheduler

from stores.itunes.parsing_functions import parse_review, XMLNS

# an other possible source:
# http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStoreServices.woa/wa/wsLookup?id=343200656&country=us
# ${opts.country} ${opts.page} ${id}  sortby={}/${opts.sort}
# use xml because it has two more fields than the json: updated and html - json also available
_rss = "https://itunes.apple.com/{}/rss/customerreviews/page={}/id={}/sortBy=mostRecent/xml"


class App:
    def __init__(self, app_id: str, country_code: str):
        self.app_id = app_id
        self.country_code = country_code
        self.reviews = rx.create(self._fetch)

    def _fetch(self, observer: Observer, scheduler: Optional[Scheduler]) -> Disposable:
        # TODO max pages are 50 - confirm
        return (
            rx.range(1, 100)
            .pipe(
                ops.map(lambda page: _rss.format(self.country_code, page, self.app_id)),
                ops.map(lambda url: requests.post(url)),
                ops.map(lambda response: etree.fromstring(response.content)),
                ops.map(lambda xml_tree: list(xml_tree.iter(XMLNS + "entry"))),
                ops.take_while(lambda xml_reviews: len(xml_reviews) > 0),
                ops.flat_map(lambda xml_tree: xml_tree),
                ops.filter(
                    lambda xml_review: any(
                        content.get("type") == "text"
                        for content in xml_review.iter(XMLNS + "content")
                    )
                ),
                ops.map(lambda xml_review: parse_review(xml_review, self.app_id)),
            )
            .subscribe(observer)
        )
