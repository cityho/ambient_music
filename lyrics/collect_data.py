import argparse
import operator
from collections import defaultdict
from typing import Dict, List

from lyricsgenius import Genius
from lyrics.config import *
import requests


# TODO: concurrent 적용(비동기처리 필요)
# TODO: 엘라스틱서치 업로드


class GeniusDataOpenSearch:
    def __init__(self, args):
        self.args = args
        self.start = args.start_artist_id
        self.end = args.end_artist_id
        self.token_by = args.token_by
        self.genius = Genius(ACCESS_TOKEN[self.token_by])

        # 에러 발생시 계속 돌아갈 대체 토큰
        self.possible_token = [k for k in ACCESS_TOKEN.keys() if k != self.token_by]
        self.data_to_update = []

    def run(self):
        try:
            self.process(self.start, self.end)
        except:
            print("호승아~ 오류 났당")

    # 이거 나중에 쪼개서 루프돌리려구요 토큰별로, start end는 임시입니다.
    def process(self, start_id, end_id):
        # loop 도는 기준: (가수 전체-가수를 인기순으로 정렬-N노래및가사)
        artists = []
        for i in range(start_id, end_id+1):
            try:
                artists.append(
                    self.get_artist_info(i)
                )
            except requests.exceptions.HTTPError:
                # 보니까 흠... 없는 가수가 많은 것 같아요 404 체감상 40%? 앞부분은 안유명해서 그럴수도?
                print(f"NO DATA ID(404): {i}")

        artists.sort(
            key=operator.itemgetter('followers_count'), reverse=True
        )  # 페북 follower가 많은 순서대로 정렬
        for art in artists:
            if art['followers_count'] < 300:  # 테스트를 위한 숫자 설정
                break  # 너무 안유명하면 그냥 수집 x

            self.data_to_update.append(
                list(
                    self.get_artist_alb_songs(art)
                )
            )

    def get_artist_info(self, artist_id: int) -> Dict:
        artist_dict = defaultdict(str)
        artist = self.genius.artist(artist_id)
        artist_dict["artist_id"] = artist_id
        artist_dict["name"] = artist["artist"]['description_annotation']['fragment']  # 이건 그냥 혹시 몰라서 저장함
        artist_dict["followers_count"] = artist["artist"]["followers_count"]
        artist_dict['image_url'] = artist["artist"]['image_url']

        return artist_dict

    def get_artist_alb_songs(self, artist_info: defaultdict) -> List:
        artist_songs = self.genius.artist_songs(
            artist_info["artist_id"], per_page=1, page=1, sort='popularity'  # 개발용으로 숫자 설정
        )  # pagenation이 귀찮아서 perpage 수를 늘리는 쪽으로... 최대limit 있음(아마100)

        for song in artist_songs["songs"]:
            if song['lyrics_state'] != 'complete':
                print(f"other case detected!!!!  {song['lyrics_state']}")
                continue
            if song['language'] != 'en':
                continue

            s = self.genius.search_song(
                song_id=song["id"]
            ).to_dict()

            res = dict()
            res["song_id"] = song["id"]
            res['artist_names'] = song['artist_names']          # 'artist_names': 'DJ Khaled (Ft. Chance the Rapper, Justin Bieber, Lil Wayne & Quavo)',
            res['full_title'] = song['full_title']              # 'full_title': "I'm the One by\xa0DJ\xa0Khaled (Ft.\xa0Chance\xa0the Rapper, Justin\xa0Bieber, Lil\xa0Wayne & Quavo)",
            res['header_image_thumbnail_url'] = song['header_image_thumbnail_url']
            res['lyrics'] = s['lyrics'].split("\n")
            res.update(artist_info)

            yield res


def parse_args():
    parser = argparse.ArgumentParser(
        description='Pass artist id --start_artist_id, --end_artist_id',
    )
    parser.add_argument('--start_artist_id', default=1)
    parser.add_argument('--end_artist_id', default=30)
    parser.add_argument('--token_by', default="hoseung")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    GeniusDataOpenSearch(args).run(1, 10)
