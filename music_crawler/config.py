import os
from dotenv import load_dotenv

load_dotenv(
    dotenv_path=".spotify_env"
)

# spotify
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

DOWNLOADPLAYLIST = {
    "This is Norah Jones": "https://open.spotify.com/playlist/37i9dQZF1DZ06evO1A8iR2",
    "This is Michael Jackson": "https://open.spotify.com/playlist/37i9dQZF1DXaTIN6XNquoW",
    "Christmas Hits": "https://open.spotify.com/playlist/37i9dQZF1DX0Yxoavh5qJV",
    "Dark & Stormy": "https://open.spotify.com/playlist/37i9dQZF1DX2pSTOxoPbx9?si=bc97091dc6aa4993",
    "Feelin' Good": "https://open.spotify.com/playlist/37i9dQZF1DX9XIFQuFvzM4?si=e4d821d267d94e6e",
    "Mega Hit Max": "https://open.spotify.com/playlist/37i9dQZF1DXbYM3nMM0oPk"
}
