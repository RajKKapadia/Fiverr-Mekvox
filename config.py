import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
ADMIN_ID = os.getenv('ADMIN_ID')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_ASSOCIATE_TAG = os.getenv('AWS_ASSOCIATE_TAG')
