# !pip install spotipy
import json
import argparse
from typing import Dict, List
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from music_crawler.config import *
from util.aws import upload_to_elastic_search, push_to_aws_queue


class InfoCollector:
    def __init__(self):
        self.client = SpotifyClientCredentials(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET
        )
        self.sp = spotipy.Spotify(client_credentials_manager=self.client)

        self.downloadlist = DOWNLOADPLAYLIST
        self.parsed_list = {
            k: self.parse_id(v) for k, v in self.downloadlist.items()
        }

        self.buffer = []

    def search_playlist(self):
        q = ""
        print("test")
        self.sp.search(q, type="playlist")
        return

    def parse_id(self, url: str):
        return url.split("/")[-1]

    def get_playlist_track(self, ply_id: str) -> List[Dict]:
        items = self.sp.playlist(ply_id)

        ply_info = dict()
        ply_info['playlist_id'] = items['id']  # 플리 url에 들어가는 id
        ply_info['playlist_name'] = items['name']  # 플리 이름
        ply_info['playlist_img_hrl'] = items['images'][0]['url'] # 플리 썸네일 이미지
        ply_info['playlist_url'] = items['external_urls']["spotify"]  # 플레이리스트 링크
        ply_info['playlist_description'] = items['description']  # 플레이리스트 전체의 데이터
        ply_info['playlist_snapshot_id'] = items['snapshot_id']  # ? 이건 뭔지 모르겠어요

        if items["tracks"]["total"] > items["tracks"]["limit"]:
            print(f"확인해보면 좋은 케이스 플레이리스트 {ply_id}")

        track_infos: List = items["tracks"]["items"]

        track_list = []
        for t in track_infos:
            track_dict = dict()
            tmp = t["track"]
            for i in range(len(tmp['artists'])):
                track_dict["artist_name"] = tmp['artists'][i]["name"]
                track_dict["artist_id"] = tmp['artists'][i]["id"]  # uri: spotify:artist:

            # song infos
            track_dict["song_name"] = tmp["name"]
            track_dict["song_id"] = tmp["id"]  # uri: spotify:track:
            track_dict["song_duration_ms"] = tmp["duration_ms"]  # 노래 플레이타임

            if t["video_thumbnail"]["url"] is not None:
                track_dict["video_img_url"] = t["video_thumbnail"]["url"]

            track_dict.update(ply_info)

            entry = {  # sqs에 넣기 위한 규칙
                "Id": track_dict["song_id"],
                "MessageBody": json.dumps(track_dict)  # dumps = dump string
            }
            track_list.append(entry)
        return track_list

    def run(self):
        for k, v in self.parsed_list.items():
            self.buffer += self.get_playlist_track(v)
        push_to_aws_queue(self.buffer)
        self.buffer = []  # initialize


if __name__ == "__main__":
    InfoCollector().run()
