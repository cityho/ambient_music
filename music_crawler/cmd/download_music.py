import argparse
import subprocess

from music_crawler.config import *

"""
DEPRECATED CODE
- 다운로드시 샘플로 보기 위해 두었습니다.
"""


# CMD NOT WORKING, ENV 커맨드가 안먹히는데 일단 뒀어요
# 다운로

def run(args):
    subprocess.call(f"$env:SPOTIPY_CLIENT_ID='{SPOTIPY_CLIENT_ID}'")
    subprocess.call(f"$env:SPOTIPY_CLIENT_SECRET={SPOTIPY_CLIENT_SECRET}")

    subprocess.call(
        f"spotify_dl -l 'https://open.spotify.com/playlist/{args.ply_id}' -o {args.path}'"
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description='Pass artist id --ply_id, --path',
    )
    parser.add_argument('--ply_id', default="")
    parser.add_argument('--path', default="")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args)
