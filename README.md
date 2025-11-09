# SharathDSA-TelegramBot

This bot sends DSA problem reminders on Telegram three times a day (07:00, 12:00, 17:00 IST).
If you haven't solved your problems by 17:00, it will remind you every hour until midnight.

## Setup

1. Clone or unzip this repository.
2. Create a `.env` file or set environment variables:
   ```
   TELEGRAM_TOKEN=your_bot_token
   OWNER_CHAT_ID=your_chat_id
   TIMEZONE=Asia/Kolkata
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

Deployed version recommended on Render / Railway for 24x7 uptime.
