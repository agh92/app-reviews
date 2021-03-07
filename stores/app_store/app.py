from typing import Optional

import feedparser
import rx
from rx import operators as ops, Observable
from rx.core import Observer
from rx.disposable import Disposable
from rx.scheduler.scheduler import Scheduler

from stores.model.app import App
from stores.app_store.review import AppStoreReview

# an other possible source:
# http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStoreServices.woa/wa/wsLookup?id=343200656&country=us
# ${opts.country} ${opts.page} ${id}  sortby={}/${opts.sort}
# use xml because it has two more fields than the json: updated and html - json also available
_rss = "https://itunes.apple.com/{}/rss/customerreviews/page={}/id={}/sortBy=mostRecent/xml"


class AppStoreApp(App):
    def __init__(self, app_id: str, country_code: str):
        self._app_id = app_id
        self._country_code = country_code
        self._reviews = rx.create(self._fetch)

    @property
    def app_id(self) -> str:
        return self._app_id

    @property
    def country_code(self) -> str:
        return self._country_code

    @property
    def reviews(self) -> Observable:
        return self._reviews

    def _fetch(self, observer: Observer, scheduler: Optional[Scheduler]) -> Disposable:
        # TODO just use 1 and then switchMap or similar to use the feed links
        return (
            rx.range(1, 100)
            .pipe(
                ops.map(lambda page: _rss.format(self.country_code, page, self.app_id)),
                ops.map(feedparser.parse),
                ops.take_while(lambda feed: len(feed.entries) > 0),
                ops.map(lambda feed: feed.entries),
                ops.flat_map(lambda entries: entries),
                ops.map(
                    lambda entry: AppStoreReview.from_feed_entry(entry, self.app_id)
                ),
            )
            .subscribe(observer)
        )
