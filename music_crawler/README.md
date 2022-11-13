# Music Crawler
- ambient music이 play 및 학습하기 위한 음원과 가사 데이터를 수집합니다.

## collect_track_info.py 사용법
- 수집하고 싶은 플레이리스트의 id를 `music_crawler/config.py`에 추가합니다.
- 이후 `collect_track_info.py`를 실행하면, 플레이리스트들과 수록곡의 정보가 sqs에 저장됩니다.

## cmd
- `music_crawler/cmd/convert_webm_wav.py --folder_path {path}` : 해당 경로 내의 webm 파일을 wav로 변환합니다.
- `music_crawler/cmd/download_music.py --ply_id {id} --path {path}` : [현재 작동x] 다운로드할 플레이리스트와 저장 경로를 지정합니다. 샘플코드로 남겨두었습니다.

