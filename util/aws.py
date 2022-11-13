import re
import time
import json
import requests

from util.config import *

import pdb


def upload_to_elastic_search(buffer, id_key):

    if len(buffer) == 0:
        return
    
    data = ""
    for x in buffer:
        idx = {"index": {"_id": x[id_key]}}
        idx = {
            "index": {
                "_id": x["song_id"]
            }
        }

        data += json.dumps(idx)+"\n"
        data += json.dumps(x)+"\n"

    headers = {"Content-Type": "application/json"}

    resp = requests.post(
        f"{ELASTICSEARCH_URL}/lyrics/_bulk?pretty&refresh",
        headers=headers,
        data=data,
        auth=ELASTICSEARCH_AUTH
    )
    print(resp.status_code)
