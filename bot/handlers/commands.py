# bot/handlers/commands.py
"""
Command handlers for Pinkie Pie bot:
/start, /help, /recipe, /joke, /song, /weather, /subscribe, /unsubscribe

Author: MADAO81
Version: 2.0
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.core.mood_system import MoodSystem
from bot.services.recipe_service import RecipeService
from bot.services.ai_service import get_pinkie_response
from bot.services.weather_service import WeatherService
from bot.utils.time_utils import is_working_hours, get_working_status_message
from bot.core.constants import VERSION
from bot.core.scheduler import add_chat, remove_chat

logger = logging.getLogger(__name__)

mood_system = MoodSystem()
recipe_service = RecipeService()
weather_service = WeatherService()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command."""
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    mood, _ = await mood_system.determine_mood()
    mood_text = mood_system.get_mood_text(mood)
    mood_emoji = mood_system.get_mood_emoji(mood)

    text = (
        f"{mood_emoji} *Hi there! I'm Pinkie Pie!*\n\n"
        f"I'm your cheerful pony friend! I love parties, sweets, and smiles! 😊\n\n"
        f"{mood_text}\n\n"
        f"📋 *Here's what I can do:*\n"
        f"/help — see all commands\n"
        f"/recipe — get a baking recipe 🧁\n"
        f"/joke — hear a joke 😄\n"
        f"/song — listen to a song 🎵\n"
        f"/weather — check the weather 🌤️\n"
        f"/subscribe — get daily recipes 🧁\n"
        f"/unsubscribe — stop daily recipes 😢\n\n"
        f"Just write me something and we'll chat! 💖\n\n"
        f"🤖 *Version:* {VERSION}"
    )

    await update.message.reply_text(text, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /help command."""
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    text = (
        "📖 *Pinkie Pie Commands:*\n\n"
        "/start — start chatting 🎈\n"
        "/help — this help 📖\n"
        "/recipe — random baking recipe 🧁\n"
        "/joke — funny joke 😄\n"
        "/song — song from Pinkie Pie 🎵\n"
        "/weather — weather in any city 🌤️\n"
        "/subscribe — daily recipes 🧁\n"
        "/unsubscribe — stop recipes 😢\n\n"
        "✨ *Features:*\n"
        "• I work daily from 9:00 to 20:00\n"
        "• If it rains — I might get a little sad 🌧️\n"
        "• I comment on messages and photos with 20% probability\n"
        "• I recognize voice messages 🎤\n"
        "• I can tell weather in any city\n"
        "• Always ready to cheer you up!\n\n"
        "💡 *Tip:* Just write me anything and we'll chat!"
    )

    await update.message.reply_text(text, parse_mode="Markdown")


async def recipe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /recipe command."""
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    status_message = await update.message.reply_text("🍳 Looking for a tasty recipe... Wait a moment!")

    recipe = await recipe_service.get_random_recipe()

    if recipe:
        text = (
            f"🧁 *Here's what I found for you!*\n\n"
            f"*{recipe['title']}*\n\n"
            f"📝 *Ingredients:*\n{recipe['ingredients']}\n\n"
            f"👩‍🍳 *Instructions:*\n{recipe['instructions']}\n\n"
            f"Enjoy! 🎂 Don't forget to invite me for tea! ☕"
        )
        await status_message.delete()
        await update.message.reply_text(text, parse_mode="Markdown")
    else:
        await status_message.edit_text(
            "😅 Oh-oh! I can't find a recipe!\n"
            "Try again later! 🍰"
        )


async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /joke command."""
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    status_message = await update.message.reply_text("🤔 Let me remember a good joke...")

    mood, _ = await mood_system.determine_mood()
    mood_desc = "sad" if mood == "sad" else "happy"

    joke = await get_pinkie_response(
        "Tell a short funny joke. No dark humor, just kind and funny jokes. Maximum 2-3 sentences.",
        mood_description=mood_desc
    )

    await status_message.delete()

    if joke:
        await update.message.reply_text(f"😄 {joke}")
    else:
        await update.message.reply_text("😅 Oh no! All the jokes ran away! How about a song instead? 🎵")


async def song_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /song command."""
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    status_message = await update.message.reply_text("🎵 Tuning my voice... La-la-la!")

    mood, _ = await mood_system.determine_mood()
    mood_desc = "sad" if mood == "sad" else "happy"

    song = await get_pinkie_response(
        "Create a short cheerful song of 4-6 lines. Use rhymes and a positive vibe. The song should be about friendship, joy, or sweets.",
        mood_description=mood_desc
    )

    await status_message.delete()

    if song:
        await update.message.reply_text(f"🎵 *Song from Pinkie Pie:*\n\n{song}\n\n🎶 La-la-la! 🎶", parse_mode="Markdown")
    else:
        await update.message.reply_text("😅 Oh no! My voice is gone! I must have sung too much at parties! 🎉")


async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for /weather command.
    Shows weather for specified city or default location.
    """
    if not is_working_hours():
        if update.message.chat.type == "private":
            await update.message.reply_text(get_working_status_message())
        return

    args = context.args
    city = " ".join(args) if args else None

    status_message = await update.message.reply_text("🌤️ Looking out the window... Let me check!")

    try:
        if city:
            weather = await weather_service.get_weather_by_city(city)
            if not weather:
                await status_message.edit_text(
                    f"😅 I can't find city '{city}'!\n"
                    "Check the name or try just /weather for default location 🌤️"
                )
                return
        else:
            weather = await weather_service.get_weather()

        if weather:
            weather_text = weather_service.get_weather_text(weather)

            details = (
                f"\n\n📊 *Details:*\n"
                f"💧 Humidity: {weather.get('humidity', '?')}%\n"
                f"💨 Wind: {weather.get('wind_speed', '?')} m/s\n"
                f"📈 Pressure: {weather.get('pressure', '?')} mmHg"
            )

            full_text = f"🌤️ *Weather*\n\n{weather_text}{details}"

            if not city:
                mood, _ = await mood_system.determine_mood()
                if mood == "sad":
                    full_text += "\n\n😔 The weather is gloomy today... But we'll still find a reason to smile!"
                else:
                    full_text += "\n\n🎈 Great weather for a party! 🎉"

            await status_message.delete()
            await update.message.reply_text(full_text, parse_mode="Markdown")
        else:
            await status_message.edit_text(
                "😅 Oh-oh! I can't get the weather!\n"
                "Check if the OpenWeatherMap API is configured correctly! 🌧️"
            )

    except Exception as e:
        logger.error(f"❌ Error getting weather: {e}")
        await status_message.edit_text(
            "😅 Oops! Something went wrong with the weather request!\n"
            "Try again later! 🌤️"
        )


async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /subscribe command."""
    chat_id = update.message.chat_id
    add_chat(chat_id)
    await update.message.reply_text(
        "🧁 *You've subscribed to daily recipes!*\n\n"
        "Every day at 12:00 I'll send you a tasty baking recipe! 🎂\n\n"
        "To unsubscribe, send /unsubscribe 😢",
        parse_mode="Markdown"
    )


async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /unsubscribe command."""
    chat_id = update.message.chat_id
    remove_chat(chat_id)
    await update.message.reply_text(
        "😢 *You've unsubscribed from daily recipes!*\n\n"
        "If you want to come back — send /subscribe 🧁",
        parse_mode="Markdown"
    )
