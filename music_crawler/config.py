import os
from dotenv import load_dotenv

load_dotenv(
    dotenv_path=".spotify_env"
)

# spotify
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

DOWNLOADPLAYLIST = {
    "Happy & Energetic" : "https://open.spotify.com/playlist/7JybuGacYxxo3yV4vsRxRg?si=0cf9921c68d84289", # HJ 추가
    "Sadness & Calm" : "https://open.spotify.com/playlist/7yVvSMAjQfBwrEEGiur0Ki?si=d24d37a7e9264173", # HJ 추가
    "Christmas" : "https://open.spotify.com/playlist/7JybuGacYxxo3yV4vsRxRg?si=0cf9921c68d84289", # HJ 추가
    "Disney" : "https://open.spotify.com/playlist/6nrnG5dhXGepVAflmyA1Qu", # HJ 추가
    "This is Norah Jones": "https://open.spotify.com/playlist/37i9dQZF1DZ06evO1A8iR2",
    "This is Michael Jackson": "https://open.spotify.com/playlist/37i9dQZF1DXaTIN6XNquoW",
    "Christmas Hits": "https://open.spotify.com/playlist/37i9dQZF1DX0Yxoavh5qJV",
    "Dark & Stormy": "https://open.spotify.com/playlist/37i9dQZF1DX2pSTOxoPbx9?si=bc97091dc6aa4993",
    "Feelin' Good": "https://open.spotify.com/playlist/37i9dQZF1DX9XIFQuFvzM4?si=e4d821d267d94e6e",
    "Mega Hit Max": "https://open.spotify.com/playlist/37i9dQZF1DXbYM3nMM0oPk"
} # 추가 희망시: 스포티파이 계정에서 링크를 만들고 그 링크와 플레이리스트 명을 여기 추가해주세요!
