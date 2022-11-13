import os 
from dotenv import load_dotenv

load_dotenv()

ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')
ELASTICSEARCH_ID = os.getenv('ELASTICSEARCH_ID')
ELASTICSEARCH_PW = os.getenv('ELASTICSEARCH_PW')
ELASTICSEARCH_AUTH = (ELASTICSEARCH_ID, ELASTICSEARCH_PW)

#aws format
AWS_ACCESS_KEY = os.getenv('aws_access_key_id')
AWS_SECRET_ACCESS_KEY = os.getenv('aws_secret_access_key')
AWS_ACCOUNT_ID = str(os.getenv('aws_account_id'))