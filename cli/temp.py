import rx
from rx import operators as ops

import stores
from stores.app_store.app import AppStoreApp
from stores.google_play.app import GooglePlayApp

if __name__ == "__main__":
    stores.VERBOSE = True
    AppStoreApp("840784742", "de").reviews.pipe(
        # GooglePlayApp("com.instagram.android", "de").reviews.pipe(
        ops.map(lambda review: review.to_json()),
    ).subscribe(on_next=lambda value: print(value))
    # rx.range(1, 10).subscribe(lambda val: print(val))
