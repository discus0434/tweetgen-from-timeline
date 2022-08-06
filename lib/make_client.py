import os

import tweepy
from dotenv import load_dotenv

load_dotenv()

def make_client() -> tweepy.Client:

    client = tweepy.Client(
        consumer_key=os.getenv("API_KEY"),
        consumer_secret=os.getenv("API_SECRET_KEY"),
        bearer_token=os.getenv("BEARER_TOKEN"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
    )

    return client
