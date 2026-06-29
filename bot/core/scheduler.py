# bot/core/scheduler.py
"""
Scheduler for daily recipe sending.

Author: MADAO81
Version: 2.0
"""

import logging
import sqlite3
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.config import Config
from bot.services.recipe_service import RecipeService

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()
recipe_service = RecipeService()

DB_PATH = Config.DATA_DIR / "recipes.db"


def _get_connection():
    """Returns database connection."""
    return sqlite3.connect(DB_PATH)


def _init_db():
    """Creates subscriptions table if it doesn't exist."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            chat_id INTEGER PRIMARY KEY,
            subscribed_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def add_chat(chat_id: int):
    """Adds chat to daily recipe distribution."""
    _init_db()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO subscriptions (chat_id) VALUES (?)", (chat_id,))
    conn.commit()
    conn.close()
    logger.info(f"📋 Chat {chat_id} added for recipe distribution")


def remove_chat(chat_id: int):
    """Removes chat from recipe distribution."""
    _init_db()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subscriptions WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()
    logger.info(f"📋 Chat {chat_id} removed from recipe distribution")


def get_active_chats():
    """Returns list of active chats from database."""
    _init_db()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM subscriptions")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]


async def send_daily_recipe(app):
    """Sends daily recipe to all active chats."""
    active_chats = get_active_chats()

    if not active_chats:
        logger.info("📭 No active chats for recipe distribution")
        return

    logger.info(f"📅 Sending daily recipe to {len(active_chats)} chats...")

    try:
        recipe = await recipe_service.get_random_recipe()

        if not recipe:
            logger.warning("⚠️ Failed to get recipe")
            return

        message = (
            f"🧁 *Here's what I baked for you today!*\n\n"
            f"*{recipe['title']}*\n\n"
            f"📝 *Ingredients:*\n{recipe['ingredients']}\n\n"
            f"👩‍🍳 *Instructions:*\n{recipe['instructions']}\n\n"
            f"Enjoy! 🎂 Don't forget to invite me for tea! ☕"
        )

        for chat_id in active_chats:
            try:
                await app.bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode="Markdown"
                )
                logger.info(f"✅ Recipe sent to chat {chat_id}")
            except Exception as e:
                logger.error(f"❌ Error sending to chat {chat_id}: {e}")
                if "bot was blocked" in str(e) or "chat not found" in str(e):
                    remove_chat(chat_id)

    except Exception as e:
        logger.error(f"❌ Error sending recipe: {e}")


def start_scheduler(app):
    """Starts the scheduler."""
    try:
        _init_db()
        hour, minute = map(int, Config.RECIPE_SEND_TIME.split(':'))

        scheduler.add_job(
            send_daily_recipe,
            CronTrigger(hour=hour, minute=minute),
            args=[app],
            id='daily_recipe',
            replace_existing=True
        )

        scheduler.start()
        logger.info(f"✅ Scheduler started. Daily recipe at {Config.RECIPE_SEND_TIME}")

    except Exception as e:
        logger.error(f"❌ Error starting scheduler: {e}")


def stop_scheduler():
    """Stops the scheduler."""
    try:
        scheduler.shutdown()
        logger.info("⏹️ Scheduler stopped")
    except Exception as e:
        logger.error(f"❌ Error stopping scheduler: {e}")
