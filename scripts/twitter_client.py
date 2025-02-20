# scripts/twitter_client.py
import os
import tweepy
from dotenv import load_dotenv

load_dotenv('../config/.env')

class TwitterClient:
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=os.getenv('BEARER_TOKEN'),
            wait_on_rate_limit=True
        )
    
    def get_client(self):
        return self.client
