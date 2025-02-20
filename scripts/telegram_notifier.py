# scripts/telegram_notifier.py
import os
import requests
from dotenv import load_dotenv

load_dotenv('../config/.env')

class TelegramNotifier:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.base_url = f"https://api.telegram.org/bot{self.token}"
    
    def send_alert(self, message):
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=payload)
            return response.ok
        except Exception as e:
            print(f"Telegram error: {str(e)}")
            return False
