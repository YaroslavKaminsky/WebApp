import os
from boto.s3.connection import S3Connection

EXCHANGERATE_KEY = S3Connection(os.environ['EXCHANGERATE_KEY'])
TELEGRAMBOT_KEY = S3Connection(os.environ['TELEGRAMBOT_KEY'])
DATABASE_URL = S3Connection(os.environ['DATABASE_URL'])

if __name__ == '__main__':
    print(EXCHANGERATE_KEY)
    print(TELEGRAMBOT_KEY)
    print(DATABASE_URL)
