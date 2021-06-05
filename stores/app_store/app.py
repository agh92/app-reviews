from typing import Optional

import feedparser
import rx
from feedparser import FeedParserDict
from rx import operators as ops
from rx.core.typing import Disposable, Observer, Scheduler, Observable
from rx.subject import Subject, BehaviorSubject

from stores.model import App
from stores.app_store.review import AppStoreReview

# an other possible source:
# http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStoreServices.woa/wa/wsLookup?id=343200656&country=us
# ${opts.country} ${opts.page} ${id}  sortby={}/${opts.sort}
# use xml because it has two more fields than the json: updated and html - json also available
_rss = "https://itunes.apple.com/{}/rss/customerreviews/page={}/id={}/sortBy=mostRecent/xml"


def pagination(current_page: str, links: FeedParserDict, paging_subject: Subject):
    next_page: str = next(link.href for link in links if link.rel == "next")
    if current_page == next_page:
        paging_subject.on_completed()
    else:
        paging_subject.on_next(next_page)


class AppStoreApp(App):
    def __init__(self, app_id: str, country_code: str):
        self._app_id = app_id
        self._country_code = country_code

    @property
    def app_id(self) -> str:
        return self._app_id

    @property
    def country_code(self) -> str:
        return self._country_code

    @property
    def reviews(self) -> Observable:
        return rx.create(self._fetch)

    def _fetch(self, observer: Observer, scheduler: Optional[Scheduler]) -> Disposable:
        # start with the first url the nex ones will be extracted from the feed
        paging_subject: Subject = BehaviorSubject(
            _rss.format(self.country_code, "1", self.app_id)
        )
        return paging_subject.pipe(
            ops.map(lambda url: (url, feedparser.parse(url))),
            ops.do_action(
                lambda data: pagination(data[0], data[1].feed.links, paging_subject)
            ),
            ops.do_action(lambda feed: print(len(feed.entries))),
            ops.map(lambda feed: feed.entries),
            ops.flat_map(lambda entries: entries),
            ops.map(lambda entry: AppStoreReview.from_feed_entry(entry, self.app_id)),
        ).subscribe(observer)
