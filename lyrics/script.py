import subprocess


for i in range(200000, 300000, 50):
    subprocess.call(
        f'python collect_data.py --start_artist_id {i} --end_artist_id {i+100} --token_by hoseung'

    )
