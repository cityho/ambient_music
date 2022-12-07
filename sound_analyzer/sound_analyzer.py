"""
Based on code by jp KIM!
- PRERPOCESSED VERSION
"""

import json
import time
import warnings

import librosa
import librosa.display
# !pip install PyAudio
# !pip install librosa
# !pip install Wave
import numpy as np
import requests

from util.aws import update_to_elastic_search
from util.config import *

warnings.filterwarnings("ignore")


class LyricsSentiment():
    def __init__(self):
        pass

    def process_sentiment(self, msg=None, song_id="", full=True):
        if msg:
            body = json.loads(msg.body)
            song_id = body['song_id']
        elif song_id:
            pass
        resp = requests.get(
            f"{ELASTICSEARCH_URL}/music_data/_doc/{song_id}",
            headers={"Content-Type": "application/json"},
            auth=ELASTICSEARCH_AUTH
        )

        entry = resp.json()["_source"]
        artist_name = entry["artist_name"]
        song_name = entry["song_name"]
        playlist_name = entry["playlist_name"]
        wav_name = f"{artist_name} - {song_name}"
        folder_name = f"C:\\Users\\hoho3\\OneDrive\\바탕 화면\\ambient_music\\sound_analyzer\\ambient-music\\{playlist_name}\\"

        try:
            signal, sr = librosa.load(f"{folder_name}{wav_name}.wav")
            onset_env = librosa.onset.onset_strength(y=signal, sr=sr, hop_length=512, aggregate=np.median)
            peaks = librosa.util.peak_pick(onset_env, pre_max=3, post_max=3, pre_avg=3, post_avg=5, delta=3, wait=10)
            times = librosa.times_like(onset_env, sr=sr, hop_length=512)
            peak_time = list(times[peaks])  # peak_time이 최종 온셋 추출 데이터임 (list 형태)
        except:
            print(song_id, f"{folder_name}{wav_name}.wav")
            return

        entry.update(
            {"onset_detect": peak_time})
        try:
            del entry["text_sentiments_emotion"]["lyrics"]
        except KeyError:
            pass
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
    print("t???")
    # LyricsSentiment(args).run()
    LyricsSentiment().run_by_els()