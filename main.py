import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from config import TELEGRAM_TOKEN, OWNER_CHAT_ID
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Kolkata"))
scheduler.start()

def send_message(bot, text):
    try:
        bot.send_message(chat_id=OWNER_CHAT_ID, text=text)
    except Exception as e:
        logger.error(f"Failed to send message: {e}")

def send_daily(bot, label):
    text = f"⚔️ {label.title()} DSA Reminder!"
    send_message(bot, text)
    if label == "evening":
        scheduler.add_job(lambda: hourly_followup(bot), CronTrigger(minute=0, timezone=pytz.timezone("Asia/Kolkata")), id="hourly_followup", replace_existing=True)

def hourly_followup(bot):
    now = datetime.now(pytz.timezone("Asia/Kolkata"))
    if now.hour >= 23:
        job = scheduler.get_job("hourly_followup")
        if job:
            scheduler.remove_job("hourly_followup")
        return
    send_message(bot, "🔔 Hourly reminder — you still have DSA tasks unsolved!")

async def start(update, context):
    await update.message.reply_text("Hello! Your DSA Reminder Bot is active.")

def main():
    if not TELEGRAM_TOKEN or not OWNER_CHAT_ID:
        print("Missing TELEGRAM_TOKEN or OWNER_CHAT_ID")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    bot = app.bot

    reminder_times = [("07:00", "morning"), ("12:00", "afternoon"), ("17:00", "evening")]
    for t, label in reminder_times:
        hour, minute = map(int, t.split(":"))
        scheduler.add_job(lambda b=bot, l=label: send_daily(b, l), CronTrigger(hour=hour, minute=minute, timezone=pytz.timezone("Asia/Kolkata")), id=f"daily_{label}", replace_existing=True)

    logger.info("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
