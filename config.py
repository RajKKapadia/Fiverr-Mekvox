import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
ADMIN_ID = os.getenv('ADMIN_ID')
AMAZON_CREATORS_CREDENTIAL_ID = os.getenv('AMAZON_CREATORS_CREDENTIAL_ID')
AMAZON_CREATORS_CREDENTIAL_SECRET = os.getenv('AMAZON_CREATORS_CREDENTIAL_SECRET')
AMAZON_ASSOCIATE_TAG = os.getenv('AMAZON_ASSOCIATE_TAG')
