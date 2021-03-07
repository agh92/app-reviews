from lxml.etree import tostring

from stores.Model.review import AppStoreReview

# {"im": "http://itunes.apple.com/rss", None: "http://www.w3.org/2005/Atom"}
XMLNS = "{http://www.w3.org/2005/Atom}"
XMLNS_IM = "{http://itunes.apple.com/rss}"


# TODO use feedparser instead of parsing here
def parse_review(entry, app_id: str):
    # TODO remove the that this call adds /n/t
    raw = str(tostring(entry))
    review_id = entry.find(XMLNS + "id").xpath("string()")
    updated = entry.find(XMLNS + "updated").xpath("string()")
    title = entry.find(XMLNS + "title").xpath("string()")
    body = _get_text_content(entry)
    rating = entry.find(XMLNS_IM + "rating")
    if rating is not None:
        rating = rating.xpath("string()")
    version = entry.find(XMLNS_IM + "version")
    if version is not None:
        version = version.xpath("string()")
    author_name = entry.find(XMLNS + "author/" + XMLNS + "name")
    if author_name is not None:
        author_name = author_name.xpath("string()")
    return AppStoreReview(
        app_id, review_id, author_name, updated, rating, title, body, version, raw
    )


def _get_text_content(entry):
    body = ""
    for content in entry.iter(XMLNS + "content"):
        if content.get("type") == "text":
            body = content.xpath("string()")
            break
    return body
