import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description='Pass artist id --start_artist_id, --end_artist_id',
    )
    parser.add_argument('--start_artist_id', default=1)
    parser.add_argument('--end_artist_id', default=500000)
    parser.add_argument('--token_by', default="jp")
    return parser.parse_args()