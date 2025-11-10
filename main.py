import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN, OWNER_CHAT_ID
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import threading
import http.server
import socketserver

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Kolkata"))
scheduler.start()

def send_message(app, text):
    try:
        app.bot.send_message(chat_id=OWNER_CHAT_ID, text=text)
    except Exception as e:
        logger.error(f"Send error: {e}")

def send_daily(app, label):
    msg = f"⚔️ {label.title()} DSA Reminder!"
    send_message(app, msg)
    if label == "evening":
        scheduler.add_job(lambda: hourly_followup(app),
                          CronTrigger(minute=0, timezone=pytz.timezone("Asia/Kolkata")),
                          id="hourly_followup", replace_existing=True)

def hourly_followup(app):
    now = datetime.now(pytz.timezone("Asia/Kolkata"))
    if now.hour >= 23:
        if scheduler.get_job("hourly_followup"):
            scheduler.remove_job("hourly_followup")
        return
    send_message(app, "🔔 Hourly reminder — you still have DSA tasks unsolved!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Your DSA Reminder Bot is active.")

def main():
    if not TELEGRAM_TOKEN or not OWNER_CHAT_ID:
        logger.error("Missing TELEGRAM_TOKEN or OWNER_CHAT_ID")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # 3 daily reminders
    reminder_times = [("07:00", "morning"), ("12:00", "afternoon"), ("17:00", "evening")]
    for t, label in reminder_times:
        hour, minute = map(int, t.split(":"))
        scheduler.add_job(lambda a=app, l=label: send_daily(a, l),
                          CronTrigger(hour=hour, minute=minute,
                                      timezone=pytz.timezone("Asia/Kolkata")),
                          id=f"daily_{label}", replace_existing=True)

    logger.info("Bot running (v21 API)")
    app.run_polling()

def keepalive_server():
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Keepalive server running on port {PORT}")
        httpd.serve_forever()

threading.Thread(target=keepalive_server, daemon=True).start()
if __name__ == "__main__":
    main()
