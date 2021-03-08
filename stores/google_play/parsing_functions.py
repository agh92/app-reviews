import requests

_warning_msg = "Our systems have detected unusual traffic from your computer network"
# this reviews_resource have been exposed by several github projects
_base_url = "https://play.google.com"
_reviews_resource = (
    _base_url
    + "/_/PlayStoreUi/data/batchexecute?rpcids=qnKhOb&f.sid=-697906427155521722&bl"
    "=boq_playuiserver_20190903.08_p0&hl={}&gl={}&authuser&soc-app=121&soc-platform=1&soc-device=1&_reqid=1065213"
)
_req_body = (
    "f.req=%5B%5B%5B%22UsvDTd%22%2C%22%5Bnull%2Cnull%2C%5B2%2C{}%2C%5B{"
    "}%2Cnull%2Cnull%5D%2Cnull%2C%5B%5D%5D%2C%5B%5C%22{}%5C%22%2C7%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D "
)
_most_recent = 2
# _review_api_data = {
#    "appId": app_id,
#    "token": "%token%",
#    "sort": 2,
#    "requestType": "initial",
#    "num": 150,
#    "paginate": False,
#    "nextPaginationToken": None,
# }


def raw_reviews(app_id, country_code, delay=0):
    # TODO implement pagination
    response = requests.post(
        _reviews_resource.format("en", "us"),
        data=_req_body.format(_most_recent, 150, app_id),
        headers={"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"},
        allow_redirects=True,
    )
    return response.text
