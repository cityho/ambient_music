import spotipy
import subprocess
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

from spotipy.oauth2 import SpotifyClientCredentials
from music_crawler.config import *

client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
)
sp = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager
)
# client_credentials_manager = SpotifyClientCredentials(client_id='22a6d168710b4ab69d4aeb99b87d313d', client_secret='0be07a9fb54d420fad2259cbebe48318')
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def run():
    subprocess.call(f"$env:SPOTIPY_CLIENT_ID='{SPOTIPY_CLIENT_ID}'")
    subprocess.call(f"$env:SPOTIPY_CLIENT_SECRET={SPOTIPY_CLIENT_SECRET}")

    subprocess.call(
        "spotify_dl -l 'https://open.spotify.com/playlist/37i9dQZF1DX9XIFQuFvzM4' -o 'C:\\Users\\hoho3\\OneDrive\\바탕 화면\\music_file'"
    )

if __name__ == "__main__":
    run()