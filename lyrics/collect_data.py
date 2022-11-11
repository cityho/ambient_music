import argparse
import operator
from collections import defaultdict
from typing import Dict, List
import time
from lyricsgenius import Genius
from lyrics.config import *
import requests
import traceback

from util.opensearch import upload_to_elastic_search


class GeniusDataOpenSearch:
    def __init__(self, args):
        self.args = args
        self.start = int(args.start_artist_id)
        self.end = int(args.end_artist_id)
        self.token_by = args.token_by
        self.genius = Genius(ACCESS_TOKEN[self.token_by], timeout=15)

        # 에러 발생시 계속 돌아갈 대체 토큰
        self.possible_token = [k for k in ACCESS_TOKEN.keys() if k != self.token_by]

        self.data_to_update = []
        self.current_artist = 0

    def run(self):
        try:
            self.process(self.start, self.end)
        except Exception as e:
            upload_to_elastic_search(
                self.data_to_update
            )
            self.data_to_update = []
            print(traceback.format_exc())
            print(self.current_artist)

    # 이거 나중에 쪼개서 루프돌리려구요 토큰별로, start end는 임시입니다.
    def process(self, start_id, end_id):
        print(start_id, end_id)
        # loop 도는 기준: (가수 전체-가수를 인기순으로 정렬-N노래및가사)
        artists = []
        for i in range(start_id, end_id+1):
            try:
                artists.append(
                    self.get_artist_info(i)
                )
                time.sleep(2)
            except requests.exceptions.HTTPError:
                # 보니까 흠... 없는 가수가 많은 것 같아요 404 체감상 40%? 앞부분은 안유명해서 그럴수도?
                print(f"NO DATA ID(404): {i}")

        artists.sort(
            key=operator.itemgetter('followers_count'), reverse=True
        )  # 페북 follower가 많은 순서대로 정렬
        count = 0 
        for art in artists:
            # if art['followers_count'] < 10000:  # 테스트를 위한 숫자 설정
            #     continue  # 너무 안유명하면 그냥 수집 x

            self.data_to_update += self.get_artist_alb_songs(art)
            count += 1
            if count % 100 == 0:
                upload_to_elastic_search(
                    self.data_to_update
                )
                self.data_to_update = []
        upload_to_elastic_search(
            self.data_to_update
        )
        self.data_to_update = []

    def get_artist_info(self, artist_id: int) -> Dict:
        artist_dict = defaultdict(str)
        artist = self.genius.artist(artist_id)
        artist_dict["artist_id"] = artist_id
        artist_dict["name"] = artist["artist"]['description_annotation']['fragment']  # 이건 그냥 혹시 몰라서 저장함
        artist_dict["followers_count"] = artist["artist"]["followers_count"]
        artist_dict['image_url'] = artist["artist"]['image_url']

        return artist_dict

    def get_artist_alb_songs(self, artist_info: defaultdict) -> List:
        try:
            artist_songs = self.genius.artist_songs(
                artist_info["artist_id"], per_page=20, page=1, sort='popularity'  # 개발용으로 숫자 설정
            )  # pagenation이 귀찮아서 perpage 수를 늘리는 쪽으로... 최대limit 있음(아마100)
        except requests.exceptions.Timeout:
            return []
        res_list = []
        for song in artist_songs["songs"]:
            if song['lyrics_state'] != 'complete':
                print(f"other case detected!!!!  {song['lyrics_state']}")
                continue
            if song['language'] != 'en':
                continue

            try:
                s = self.genius.search_song(
                    song_id=song["id"], get_full_info=False
                ).to_dict()
                time.sleep(2)
            except requests.exceptions.Timeout:
                continue
            except AttributeError:
                continue

            res = dict()
            res["song_id"] = song["id"]
            res['artist_names'] = song['artist_names']          # 'artist_names': 'DJ Khaled (Ft. Chance the Rapper, Justin Bieber, Lil Wayne & Quavo)',
            res['full_title'] = song['full_title']              # 'full_title': "I'm the One by\xa0DJ\xa0Khaled (Ft.\xa0Chance\xa0the Rapper, Justin\xa0Bieber, Lil\xa0Wayne & Quavo)",
            res['header_image_thumbnail_url'] = song['header_image_thumbnail_url']
            res['lyrics'] = s['lyrics'].split("\n")
            res.update(artist_info)

            res_list.append(res)
        return res_list


def parse_args():
    parser = argparse.ArgumentParser(
        description='Pass artist id --start_artist_id, --end_artist_id',
    )
    parser.add_argument('--start_artist_id', default=1)
    parser.add_argument('--end_artist_id', default=500000)
    parser.add_argument('--token_by', default="jp")
    return parser.parse_args()

# python .\lyrics\collect_data.py --start_artist_id 10 --end_artist_id 5000 --token_by jp
# python .\lyrics\collect_data.py --start_artist_id 5000 --end_artist_id 10000 --token_by hoseung
# python .\lyrics\collect_data.py --start_artist_id 10000 --end_artist_id 15000 --token_by dy

if __name__ == "__main__":
    args = parse_args()
    GeniusDataOpenSearch(args).run()
