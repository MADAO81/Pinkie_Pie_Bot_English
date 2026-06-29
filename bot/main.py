# bot/main.py
"""
Main module for Pinkie Pie bot.

Author: MADAO81
Version: 2.0
"""

import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from bot.config import Config
from bot.handlers.commands import (
    start,
    help_command,
    recipe_command,
    joke_command,
    song_command,
    weather_command,
    subscribe_command,
    unsubscribe_command
)
from bot.handlers.admin import (
    add_recipe_command,
    list_recipes_command,
    del_recipe_command,
    list_chats_command
)
from bot.handlers.messages import handle_message
from bot.handlers.photos import handle_photo
from bot.handlers.voice import handle_voice
from bot.core.scheduler import start_scheduler, add_chat
from bot.core.constants import VERSION

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Entry point for the application."""
    logger.info(f"🎈 Starting Pinkie Pie bot (v{VERSION})...")
    logger.info(f"👤 Author: MADAO81")

    if not Config.TELEGRAM_TOKEN:
        logger.error("❌ TELEGRAM_TOKEN not found in .env!")
        return

    if not Config.OPENAI_API_KEY:
        logger.error("❌ OPENAI_API_KEY not found in .env!")
        return

    app = Application.builder().token(Config.TELEGRAM_TOKEN).build()

    # === AUTO-LOAD CHATS FROM .env ===
    default_chats = os.getenv("DEFAULT_CHATS", "")
    if default_chats:
        for chat_id in default_chats.split(","):
            try:
                chat_id = int(chat_id.strip())
                add_chat(chat_id)
                logger.info(f"✅ Automatically added chat: {chat_id}")
            except Exception as e:
                logger.error(f"❌ Error adding chat {chat_id}: {e}")

    # ===== 1. REGISTER ALL COMMANDS =====
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("recipe", recipe_command))
    app.add_handler(CommandHandler("joke", joke_command))
    app.add_handler(CommandHandler("song", song_command))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(CommandHandler("subscribe", subscribe_command))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe_command))

    app.add_handler(CommandHandler("addrecipe", add_recipe_command))
    app.add_handler(CommandHandler("listrecipes", list_recipes_command))
    app.add_handler(CommandHandler("delrecipe", del_recipe_command))
    app.add_handler(CommandHandler("listchats", list_chats_command))

    # ===== 2. REGISTER MESSAGE HANDLERS =====
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.AUDIO, handle_voice))

    start_scheduler(app)

    logger.info("✅ Bot successfully started and ready!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()