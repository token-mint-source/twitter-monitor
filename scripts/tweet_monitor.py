# scripts/tweet_monitor.py
from datetime import datetime, timedelta
import pandas as pd
from config import settings
from .twitter_client import TwitterClient
import logging
import os

logging.basicConfig(filename='../logs/monitor.log', level=logging.INFO)

class TweetMonitor:
    def __init__(self):
        self.client = TwitterClient().get_client()
        self.keywords = settings.KEYWORDS
        self.time_window = timedelta(hours=settings.TIME_WINDOW_HOURS)
        
    def _build_query(self):
        return f"{self.keywords} {settings.EXCLUDE} {settings.LANG}"
    
    def fetch_tweets(self):
        try:
            query = self._build_query()
            start_time = (datetime.utcnow() - self.time_window).strftime('%Y-%m-%dT%H:%M:%SZ')
            
            response = self.client.search_recent_tweets(
                query=query,
                start_time=start_time,
                max_results=settings.MAX_RESULTS,
                tweet_fields=['created_at', 'text', 'author_id']
            )
            
            if response.data:
                self._save_tweets(response.data)
                logging.info(f"Found {len(response.data)} new tweets")
                
            return response.data
            
        except Exception as e:
            logging.error(f"Error fetching tweets: {str(e)}")
            return []
    
    def _save_tweets(self, tweets):
        os.makedirs('../data/tweets', exist_ok=True)
        df = pd.DataFrame([{
            'id': tweet.id,
            'author': tweet.author_id,
            'text': tweet.text.replace('\n', ' '),
            'timestamp': tweet.created_at
        } for tweet in tweets])
        
        filename = f"../data/tweets/{datetime.utcnow().strftime('%Y%m%d_%H%M')}.csv"
        df.to_csv(filename, index=False)
