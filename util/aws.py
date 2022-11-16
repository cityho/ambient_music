import re
import time
import json
import requests
import pdb
import boto3
import s3fs

from util.config import *


def upload_to_elastic_search(buffer, id_key):
    if len(buffer) == 0:
        return

    data = ""
    for x in buffer:
        idx = {"index": {"_id": x[id_key]}}
        idx = {
            "index": {
                "_id": x[id_key]
            }
        }

        data += json.dumps(idx) + "\n"
        data += json.dumps(x) + "\n"

    headers = {"Content-Type": "application/json"}

    resp = requests.post(
        f"{ELASTICSEARCH_URL}/music_data/_bulk?pretty&refresh",
        headers=headers,
        data=data,
        auth=ELASTICSEARCH_AUTH
    )
    print(resp.status_code)


def push_to_aws_queue(buffer):
    sqs = boto3.resource(
        "sqs",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    queue = sqs.get_queue_by_name(
        QueueName="ambient-music",
        QueueOwnerAWSAccountId=AWS_ACCOUNT_ID
    )

    print("Pushing to AWS SQS")

    temp = {x["Id"]: x for x in buffer}
    buffer = list(temp.values())

    for idx in range(0, len(buffer), 3):  # 일단 그냥 작게 쪼갰어요
        chunk = buffer[idx:idx + 3]
        queue.send_messages(Entries=chunk)


def upload_folder_to_s3(from_local, to_s3):
    # 개별 dir을 업로드 하는 코드
    # ex) s3_path = "bucket_name/dir_path"
    s3_file = s3fs.S3FileSystem(
        key=AWS_ACCESS_KEY, secret=AWS_SECRET_ACCESS_KEY
    )
    s3_file.put(from_local, to_s3, recursive=True)