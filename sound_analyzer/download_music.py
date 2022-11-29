import s3fs

from util.config import *

fs = s3fs.S3FileSystem(key=AWS_ACCESS_KEY, secret=AWS_SECRET_ACCESS_KEY)
bucket = "s3://ambient-music/"

bucket_folders = fs.ls(bucket)
for f in bucket_folders:
    files = fs.ls(f)
    for file in files:
        fs.download(file, file)

