"""
Based on code by HYUNJI KIM!
- PRERPOCESSED VERSION
"""
import argparse
import json
import logging
import time
from datetime import datetime
from typing import List

import matplotlib.pyplot as plt
import nltk
import pandas as pd
import requests
from transformers import pipeline
from wordcloud import WordCloud

from util.aws import upload_to_elastic_search, QUEUE, update_to_elastic_search
from util.config import *


class LyricsSentiment():
    def __init__(self, args):
        self.mode = args.sentiment_mode

        if self.mode == "emotion":
            logging.info("가사 분석이 감정을 기준으로 분류됩니다.")
            self.classifier = pipeline(
                "sentiment-analysis", model="michellejieli/emotion_text_classifier"
            )
        else:
            logging.info("가사 분석이 positive, negative를 기준으로 분류됩니다.")
            self.classifier = pipeline('sentiment-analysis')
        self.word_cloud = args.word_cloud

        self.no_lyrics = []

    def _make_word_cloud(self, lyrics: List[str]):
        # TODO: 이거 이미지 넣는 코드에서 수정이 조금 필요할 것 같아요~
        stopwords = nltk.corpus.stopwords.words('english')
        new_stopwords = [
            'verse', 'bridge', 'guitar', 'solo', 'instrumental', 'intro',
            'im', 'get', 'youre', 'youve', 'gotta', "we've", "gon'", "I'll", "can't",
            "yo", "yeah", 'ayy', 'ooh', 'oh', 'ya', 'doo', 'doo doo'
        ]
        stopwords.extend(new_stopwords)
        wordcloud = WordCloud(
            stopwords=stopwords, background_color='White', width=800, height=600
        ).generate(' '.join(lyrics))

        plt.figure(figsize=(12, 8))
        plt.axis("off")
        plt.imshow(wordcloud)
        plt.show()

    def _calculate_sentiment(self, lyrics, full):
        c1 = pd.DataFrame(self.classifier(lyrics))  # ex1 : 문장
        if full:
            lyrics = [lyrics]
        df = pd.DataFrame(lyrics, columns=['lyrics']).join(c1)
        df_dict = {f"text_sentiments_{self.mode}": df.to_dict("list")}
        return df_dict

    def _prerocess_lyrics(self, lyrics: str, full) -> List[str]:
        lyrics = lyrics.split("\n")

        new_stopwords = [
            'verse', 'bridge', 'guitar', 'solo', 'instrumental', 'intro',
            'im', 'get', 'youre', 'youve', 'gotta', "we've", "gon'", "I'll", "can't",
            "yo", "yeah", 'ayy', 'ooh', 'oh', 'ya', 'doo', 'doo doo'
        ]

        lyrics = [
            ly for ly in lyrics if not (ly.startswith("[") and ly.endswith("]"))
        ]
        for w in new_stopwords:
            lyrics = [ly.replace(w, "") for ly in lyrics]

        if full:
            return " ".join(lyrics)
        else:
            return lyrics

    def process_sentiment(self, msg, full=True):
        body = json.loads(msg.body)
        song_id = body['song_id']
        song_id = "0S5EEpFAHcT7cm5XOASc29"  # 마이클잭슨 테스트
        resp = requests.get(
            f"{ELASTICSEARCH_URL}/music_data/_doc/{song_id}",
            headers={"Content-Type": "application/json"},
            auth=ELASTICSEARCH_AUTH
        )
        if resp.status_code != 200:
            print("*" * 50)
            print(body)
            self.no_lyrics.append(body)
            print("*" * 50)

        entry = resp.json()["_source"]
        lyrics = self._prerocess_lyrics(entry["lyrics"], full)

        if self.word_cloud:
            self._make_word_cloud(lyrics)
        entry.update(
            self._calculate_sentiment(lyrics, full)
        )
        return entry

    def run(self):
        count = 0
        while True:  # QUEUEQ가 바닥이 날 때까지
            print("[{}] Fetching song info".format(datetime.now()), end="", flush=True)
            messages = QUEUE.receive_messages(
                MessageAttributeNames=["All"],
                MaxNumberOfMessages=10,
                WaitTimeSeconds=1
            )

            if len(messages) == 0:
                print("-Queue is empty wait for a while.")
                count += 1
                if count == 5:
                    print("DONE!!")
                    print("DONE!!")
                    print("DONE!!")
                    break
                time.sleep(60)
                continue

            for msg in messages:
                msg.delete()

            buffer = []
            for msg in messages:
                print(".", end="", flush=True)
                try:
                    entry = self.process_sentiment(msg)
                except:
                    continue
                update_to_elastic_search([entry], "song_id")
                print(entry["song_id"])
                print("!!")
                time.sleep(3)

            # upload_to_elastic_search(buffer, "song_id")
            print("!!")

        with open("../../music_crawler/deprecated/no_lyrics.json", "w", encoding="utf-8") as f:
            json.dump(self.no_lyrics, f, indent="\t")


def parse_args():
    parser = argparse.ArgumentParser(
        description='Pass --sentiment_mode, avaliable: emotion, pos_neg'
    )
    parser.add_argument(
        '--sentiment_mode', default="emotion"
    )
    parser.add_argument(
        '--word_cloud', default=False, action="store_true"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    LyricsSentiment(args).run()
