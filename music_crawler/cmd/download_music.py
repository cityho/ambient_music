import os
import glob
import argparse
import subprocess
import spotify_dl
from moviepy.audio.io.AudioFileClip import AudioFileClip

from music_crawler.config import *
from util.aws import upload_folder_to_s3

"""
노래 일괄 다운로드 및 변환, 업로드
"""


def run(args):
    env = {
        "SPOTIPY_CLIENT_ID": SPOTIPY_CLIENT_ID,
        "SPOTIPY_CLIENT_SECRET": SPOTIPY_CLIENT_SECRET
    }

    path = args.path.replace("\\", "\\\\")
    for k, v in DOWNLOADPLAYLIST.items():
        subprocess.call(  # 패키지 특성상 로컬에 받아서 변환 후 업로드
            f"spotify_dl -l '{v}' -o '{path}'", shell=True, env=env
        )

    sub_folders = [x[0] for x in os.walk(args.path) if x[0] != args.path]
    if args.wav:
        for sub in sub_folders:
            os.chdir(sub)
            for f in glob.glob("*.webm"):
                clip = AudioFileClip(f)
                clip.write_audiofile(f.replace(".webm", ".wav"))

                os.remove(f"{sub}\\{f}")

    if args.to_s3:
        for sub in sub_folders:
            upload_folder_to_s3(from_local=sub, to_s3="ambient-music")


def parse_args():
    parser = argparse.ArgumentParser(
        description='Pass artist id --wav, --path',
    )
    parser.add_argument(
        '--path', default=f"C:\\music_file"
    )
    parser.add_argument(
        '--wav', default=True, action="store_true"
    )
    parser.add_argument(
        '--to_s3', default=False, action="store_true"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args)
