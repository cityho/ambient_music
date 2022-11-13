import argparse
import subprocess
import glob
import os

import moviepy.editor as moviepy


def run(args: argparse.Namespace):
    file_path = args.folder_path
    os.chdir(file_path)
    for f in glob.glob("*.webm"):
        clip = moviepy.AudioFileClip(f)
        clip.write_audiofile(f.replace(".webm", ".wav"))

        os.remove(f"{file_path}\\{f}")


def parse_args():
    parser = argparse.ArgumentParser(
        description='Pass --folder_path path should be absolute path'
    )
    parser.add_argument(
        '--folder_path',
        default=r"C:\Users\hoho3\OneDrive\바탕 화면\music_file\Feelin' Good"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args)