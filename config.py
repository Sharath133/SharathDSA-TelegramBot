import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_CHAT_ID = int(os.getenv("OWNER_CHAT_ID")) if os.getenv("OWNER_CHAT_ID") else None
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")
DAILY_REMINDER_TIMES = os.getenv("DAILY_REMINDER_TIMES", "07:00,12:00,17:00").split(",")
