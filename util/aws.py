import re
import time
import json
import requests
import pdb
import boto3

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



# TODO :SQS 에서 GET 하고 ELASTICSEARCH 연동
#     sqs = boto3.resource("sqs")
#     queue = sqs.get_queue_by_name(QueueName="hoseung2-naver_news")
#
#     while True:  # QUEUEQ가 바닥이 날 때까지
#         print("[{}] Fetching news".format(dt.datetime.now()), end="", flush=True)
#         messages = queue.receive_messages(
#             MessageAttributeNames=["All"],
#             MaxNumberOfMessages=10,
#             WaitTimeSeconds=1  # 큐가 비어 있는 상황에서 다음 메시지 들어올 때 까지의 대기 시간
#         )
#
#         if len(messages) == 0:
#             print("-Queue is empty wait for a while.")
#             time.sleep(60)
#             continue
#
#         for msg in messages:
#             # 큐에서 빼내라는 의미, 이렇게 해야 큐에서 삭제하고 크롤러가 동시에 작업될 수 있다.
#             msg.delete()
#
#         buffer = []
#         # 속도 개선을 위해 두개로 나눕니다.
#         for msg in messages:
#             print(".", end="", flush=True)
#             try:
#                 entry = fetch_news_contents(msg)
#             except:
#                 continue
#
#             if entry is not None:
#                 buffer.append(entry)
#
#         upload_to_elastic_search(buffer)
#         print("!!")
#         time.sleep(3)