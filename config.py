import os

EXCHANGERATE_KEY = os.environ.get('EXCHANGERATE_KEY', None)
TELEGRAMBOT_KEY = os.environ.get('TELEGRAMBOT_KEY', None)
DATABASE_URL = os.environ.get('DATABASE_URL', None)

if __name__ == '__main__':
    print(EXCHANGERATE_KEY)
    print(TELEGRAMBOT_KEY)
    print(DATABASE_URL)
