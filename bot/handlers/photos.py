# bot/handlers/photos.py
"""
Photo handler for Pinkie Pie bot.

Author: MADAO81
Version: 2.0
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.core.mood_system import MoodSystem
from bot.services.ai_service import analyze_image
from bot.services.weather_service import WeatherService
from bot.utils.time_utils import is_working_hours
from bot.core.context_manager import ContextManager

logger = logging.getLogger(__name__)

mood_system = MoodSystem()
weather_service = WeatherService()
context_manager = ContextManager()


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles photos."""
    if not is_working_hours():
        return

    if not mood_system.should_comment():
        return

    status_message = await update.message.reply_text("🖼️ Looking at the picture... Let me think!")

    try:
        user_id = update.effective_user.id
        user_message = update.message.caption or "Nice picture!"

        photo_file = await update.message.photo[-1].get_file()
        image_data = await photo_file.download_as_bytearray()
        
        logger.info(f"📸 Photo received, size: {len(image_data)} bytes")

        mood, weather = await mood_system.determine_mood()
        mood_desc = "sad" if mood == "sad" else "happy"

        response = await analyze_image(
            image_data=bytes(image_data),
            user_message=user_message,
            mood_description=mood_desc
        )

        if not response:
            response = "🖼️ Oh, what a beautiful picture! My eyes are dazzled by such magnificence! 😄"

        weather_keywords = ["weather", "rain", "sun", "cold", "warm", "temperature"]
        if user_message and any(keyword in user_message.lower() for keyword in weather_keywords):
            weather_text = weather_service.get_weather_text(weather)
            response += f"\n\n{weather_text}"

        await status_message.delete()

        if update.message.chat.type == "private":
            await update.message.reply_text(f"🖼️ {response}")
        else:
            await update.message.reply_text(
                f"🖼️ {response}",
                reply_to_message_id=update.message.message_id
            )

        context_manager.save_context(user_id, f"[Photo] {user_message}", response)
        logger.info("✅ Photo processed successfully")

    except Exception as e:
        logger.error(f"❌ Error processing photo: {e}")
        await status_message.edit_text(
            "🖼️ Oh, what a beautiful picture! "
            "I'm a little blind from such magnificence! 😄"
        )
