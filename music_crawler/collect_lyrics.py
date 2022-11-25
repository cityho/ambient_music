import re
import boto3
import time
from datetime import datetime
import json
import requests
from typing import Dict, List
from bs4 import BeautifulSoup

from music_crawler.config import *
from util.aws import upload_to_elastic_search, push_to_aws_queue

sqs = boto3.resource("sqs")
queue = sqs.get_queue_by_name(QueueName="ambient-music")


def scrape_lyrics(msg):
    item = json.loads(msg.body)

    artistname = item["artist_name"].replace(' ', '-')
    songname = item["song_name"].replace(' ', '-')

    url = f'https://genius.com/{artistname}-{songname}-lyrics'
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')

    regex = re.compile('.*Lyrics__Container-sc.*')  # "lyrics"(구버전), "Lyrics__Container-sc-1ynbvzw-6 YYrds" ...
    containers: List = html.find_all("div", {"class": regex})
    assert len(containers) == 1, Exception("가사가 여러개로 탐지되는 경우")

    lyrics = containers[0].get_text(separator="\n")
    try:
        if len(lyrics) == 0:
            print("here")
    except:
        print("here")


    item["lyrics"] = lyrics
    return item

def run():
    while True:  # QUEUEQ가 바닥이 날 때까지
        print("[{}] Fetching song info".format(datetime.now()), end="", flush=True)
        messages = queue.receive_messages(
            MessageAttributeNames=["All"],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=1  # 큐가 비어 있는 상황에서 다음 메시지 들어올 때 까지의 대기 시간
        )

        if len(messages) == 0:
            print("-Queue is empty wait for a while.")
            time.sleep(60)
            continue

        for msg in messages:
            # 큐에서 빼내라는 의미, 이렇게 해야 큐에서 삭제하고 크롤러가 동시에 작업될 수 있다.
            msg.delete()

        buffer = []
        # 속도 개선을 위해 두개로 나눕니다.
        for msg in messages:
            print(".", end="", flush=True)
            try:
                entry = scrape_lyrics(msg)
            except:
                continue

            if entry is not None:
                buffer.append(entry)

        upload_to_elastic_search(buffer, "song_id")
        print("!!")
        time.sleep(3)


if __name__ == "__main__":
    run()
