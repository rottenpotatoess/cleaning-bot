import os
import logging
import asyncio
from datetime import datetime
import pytz
import pandas as pd
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_GROUP_ID = os.environ["TELEGRAM_GROUP_ID"]
EXCEL_FILE = os.environ.get("EXCEL_FILE", "Coffee_Cleaning_Schedule_2026.xlsx")
CAMBODIA_TZ = pytz.timezone("Asia/Phnom_Penh")


def load_schedule() -> pd.DataFrame:
    df = pd.read_excel(EXCEL_FILE)
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"], format="mixed")
    return df


def get_todays_shift(df: pd.DataFrame) -> dict | None:
    today = datetime.now(CAMBODIA_TZ).date()
    for _, row in df.iterrows():
        shift_date = row["Date"].date()
        if shift_date == today:
            return {
                "date": shift_date,
                "team": str(row["Team"]).strip(),
                "members": str(row["Assigned Members"]).strip(),
            }
    return None


def build_message(shift: dict) -> str:
    date_str = shift["date"].strftime("%A, %B %d, %Y")
    members_list = [m.strip() for m in shift["members"].split(",")]
    members_formatted = "\n".join(f"  • {m}" for m in members_list)

    return (
        f"☕ *Coffee Area Cleaning Reminder*\n\n"
        f"📅 *Date:* {date_str}\n"
        f"👥 *Team:* {shift['team']}\n\n"
        f"🧹 *Assigned Members:*\n{members_formatted}\n\n"
        f"⏰ Please remember to clean the coffee area today\\. Thank you\\! 🙏"
    )


async def send_reminder():
    logger.info("Checking schedule for today...")
    try:
        df = load_schedule()
        shift = get_todays_shift(df)

        if shift is None:
            logger.info("No cleaning shift scheduled for today.")
            return

        logger.info(f"Found shift: {shift}")
        message = build_message(shift)

        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(
            chat_id=TELEGRAM_GROUP_ID,
            text=message,
            parse_mode="MarkdownV2",
        )
        logger.info(f"Reminder sent successfully to group {TELEGRAM_GROUP_ID}")

    except TelegramError as e:
        logger.error(f"Telegram error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)


async def main():
    scheduler = AsyncIOScheduler(timezone=CAMBODIA_TZ)

    # Schedule daily at 4:30 PM Cambodia time
    scheduler.add_job(
        send_reminder,
        trigger="cron",
        hour=16,
        minute=30,
        id="daily_reminder",
        name="Coffee Cleaning Reminder",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("Bot started. Scheduler running — daily reminder at 4:30 PM (Cambodia time).")

    # Keep the process alive
    try:
        while True:
            await asyncio.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
