from appstores import google_play as gp
import json


# define your own app_ids.txt
with open('app_ids.txt') as ids_file:
    for app_id in ids_file.readlines():
        reviews = gp.reviews(app_id)
        jsons = [review.to_json() for review in reviews]
        print ('Got ', len(jsons), ' reviews')
        with open(app_id.replace('.', '_') + '.json', 'w') as f:
            f.write('[' + ',\n'.join(jsons) + ']')
