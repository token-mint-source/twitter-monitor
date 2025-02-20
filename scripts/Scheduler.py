# scripts/scheduler.py
from apscheduler.schedulers.blocking import BlockingScheduler
from tweet_monitor import TweetMonitor
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

def job():
    print("\n--- Running Twitter scan ---")
    monitor = TweetMonitor()
    monitor.fetch_tweets()

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', hours=3)
    print("Scheduler started. Press Ctrl+C to exit.")
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("Scheduler stopped")
