import os
from dotenv import load_dotenv

load_dotenv(
    dotenv_path="music_crawler/.spotify_env"
)

# spotify
# SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
# SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_CLIENT_ID = "821c9bdeb2a449918d1210c3ffdcd486"
SPOTIPY_CLIENT_SECRET = "fbba67e6de334f2da2180f1d2a6480d2"


DOWNLOADPLAYLIST = {
    "This is Norah Jones": "https://open.spotify.com/playlist/37i9dQZF1DZ06evO1A8iR2",
    "This is Michael Jackson": "https://open.spotify.com/playlist/37i9dQZF1DXaTIN6XNquoW",
    "Christmas Hits": "https://open.spotify.com/playlist/37i9dQZF1DX0Yxoavh5qJV",
    "Dark & Stormy": "https://open.spotify.com/playlist/37i9dQZF1DX2pSTOxoPbx9?si=bc97091dc6aa4993",
    "Feelin' Good": "https://open.spotify.com/playlist/37i9dQZF1DX9XIFQuFvzM4?si=e4d821d267d94e6e",
    "Mega Hit Max": "https://open.spotify.com/playlist/37i9dQZF1DXbYM3nMM0oPk"
}
