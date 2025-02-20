# scripts/tweet_monitor.py
import os
import logging
from datetime import datetime, timedelta
import pandas as pd
import tweepy
from dotenv import load_dotenv
from .twitter_client import TwitterClient
from .telegram_notifier import TelegramNotifier

# Load environment variables
load_dotenv('../config/.env')

# Configure logging
logging.basicConfig(
    filename='../logs/monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TweetMonitor:
    def __init__(self):
        self.client = TwitterClient().get_client()
        self.notifier = TelegramNotifier()
        self.keywords = os.getenv('TWITTER_KEYWORDS', '(accept bitcoin OR (send address OR send wallet) OR addy)')
        self.time_window = int(os.getenv('TIME_WINDOW_HOURS', 3))
        self.max_results = int(os.getenv('MAX_RESULTS', 100))

    def _build_query(self):
        return f"{self.keywords} -is:retweet -is:reply lang:en"

    def _format_message(self, tweet):
        return f"""🚨 **New Crypto Post Detected** 🚨
        
📝 *Text*: {tweet.text[:200] + '...' if len(tweet.text) > 200 else tweet.text}
🕒 *Posted*: {tweet.created_at.strftime('%Y-%m-%d %H:%M UTC')}
🔗 *Twitter URL*: https://twitter.com/user/status/{tweet.id}

⚠️ *Potential scam alert*! Be cautious with wallet addresses."""

    def fetch_tweets(self):
        try:
            query = self._build_query()
            start_time = (datetime.utcnow() - timedelta(hours=self.time_window)).strftime('%Y-%m-%dT%H:%M:%SZ')
            
            logging.info(f"Searching tweets with query: {query}")
            
            response = self.client.search_recent_tweets(
                query=query,
                start_time=start_time,
                max_results=self.max_results,
                tweet_fields=['created_at', 'text', 'author_id']
            )

            if not response.data:
                logging.info("No new tweets found in this interval.")
                return []

            tweets = response.data
            self._save_tweets(tweets)
            self._send_alerts(tweets)
            
            return tweets

        except tweepy.TweepyException as e:
            logging.error(f"Twitter API error: {str(e)}
