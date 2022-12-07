"""
Based on code by jp KIM!
- PRERPOCESSED VERSION
"""

import json
import time
import warnings
from datetime import datetime
from typing import List

import librosa
import librosa.display
import nltk
# !pip install PyAudio
# !pip install librosa
# !pip install Wave
import numpy as np
import pandas as pd
import requests
from matplotlib import pyplot as plt
from wordcloud import WordCloud

from util.aws import QUEUE, update_to_elastic_search
from util.config import *

# For onset_detect---------------------
# 온셋 추출 위한 라이브러리 추가 설치

warnings.filterwarnings("ignore")
# from music_crawler.cmd import download_music  # 음악 파일을 로컬에 저장 후 불러와서 온셋 데이터 추출 작업 위해 cmd 폴더 안 music_download.py를 import

# -------------------------------------


class LyricsSentiment():
    def __init__(self):
        pass

    def process_sentiment(self, msg=None, song_id="", full=True):
        if msg:
            body = json.loads(msg.body)
            song_id = body['song_id']
        elif song_id:
            pass
        song_id = "0S5EEpFAHcT7cm5XOASc29"
        resp = requests.get(
            f"{ELASTICSEARCH_URL}/music_data/_doc/{song_id}",
            headers={"Content-Type": "application/json"},
            auth=ELASTICSEARCH_AUTH
        )
        # if resp.status_code != 200:
        #     self.no_lyrics.append(song_id)

        entry = resp.json()["_source"]
        artist_name = entry["artist_name"]
        song_name = entry["song_name"]
        playlist_name = entry["playlist_name"]
        wav_name = f"{artist_name} - {song_name}"
        folder_name = f"C:\\Users\\hoho3\\OneDrive\\바탕 화면\\ambient_music\\sound_analyzer\\ambient-music\\{playlist_name}\\"

        signal, sr = librosa.load(f"{folder_name}{wav_name}.wav")
        onset_env = librosa.onset.onset_strength(y=signal, sr=sr, hop_length=512, aggregate=np.median)
        peaks = librosa.util.peak_pick(onset_env, pre_max=3, post_max=3, pre_avg=3, post_avg=5, delta=3, wait=10)
        times = librosa.times_like(onset_env, sr=sr, hop_length=512)
        peak_time = list(times[peaks])  # peak_time이 최종 온셋 추출 데이터임 (list 형태)

        entry.update(
            {"onset_detect": peak_time})
        try:
            del entry["text_sentiments_emotion"]["lyrics"]
        except KeyError:
            pass
        print(entry)
        update_to_elastic_search([entry], "song_id")
        time.sleep(1)
        return

    def run_by_els(self):
        data = json.dumps({"size": 400, "query": {"match_all": {}}})
        resp = requests.get(
            f"{ELASTICSEARCH_URL}/music_data/_search",
            headers={"Content-Type": "application/json"},
            auth=ELASTICSEARCH_AUTH,
            data=data
        )
        songs = resp.json()["hits"]["hits"]

        for s in songs:
            print(".", end="", flush=True)
            # try:
            entry = self.process_sentiment(song_id=s["_id"])
            # except:
            #     import traceback
            #     # print(traceback.format_exc())
            #     print("No data on:", s["_id"])
            #     continue

            # update_to_elastic_search([entry], "song_id")

if __name__ == "__main__":
    # LyricsSentiment(args).run()
    LyricsSentiment().run_by_els()