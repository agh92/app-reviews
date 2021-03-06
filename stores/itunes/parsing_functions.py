from lxml.etree import tostring

from stores.Model.review import AppStoreReview


def _text_body(entry, std_namespace="http://www.w3.org/2005/Atom"):
    body = ""
    # content < type="text"> text
    for content in entry.iter("{" + std_namespace + "}content"):
        if content.get("type") == "text":
            body = content.xpath("string()")
            break
    return body


def _parse_review(
    entry,
    std_namespace="http://www.w3.org/2005/Atom",
    im_namespace="http://itunes.apple.com/rss",
):
    # tostring will return bytes and we cant json serelize bytes so call str
    raw = str(tostring(entry))
    review_id = entry.find("{" + std_namespace + "}id").xpath("string()")
    updated = entry.find("{" + std_namespace + "}updated").xpath("string()")
    # title <title> text
    title = entry.find("{" + std_namespace + "}title").xpath("string()")
    body = _text_body(entry)
    # rating <im:rating> text
    rating = entry.find("{" + im_namespace + "}rating")
    if rating is not None:
        rating = rating.xpath("string()")
    # version <im:version> text
    version = entry.find("{" + im_namespace + "}version")
    if version is not None:
        version = version.xpath("string()")
    author_name = entry.find(
        "{" + std_namespace + "}author/" + "{" + std_namespace + "}name"
    )  # author_name <author><name> text
    if author_name is not None:
        author_name = author_name.xpath("string()")
    return AppStoreReview(
        None, review_id, author_name, updated, rating, title, body, version, raw
    )
