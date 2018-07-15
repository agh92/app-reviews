

'http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStoreServices.woa/wa/wsLookup?id=343200656&country=us'
import requests

#${opts.country} ${opts.page} ${id}  sortby={}/${opts.sort}
_resource = 'https://itunes.apple.com/{}/rss/customerreviews/page={}/id={}/json'

def reviews(app_id, country):
    url = _resource.format('de', '1', app_id) #, 'mostRecent'
    print(url)
    return requests.post(url)

