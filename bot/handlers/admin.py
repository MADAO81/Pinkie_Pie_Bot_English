# bot/handlers/admin.py
"""
Admin commands for Pinkie Pie bot.
Adding recipes via Telegram.

Author: MADAO81
Version: 2.0
"""

import logging
import sqlite3
from telegram import Update
from telegram.ext import ContextTypes
from bot.config import Config
from bot.utils.time_utils import is_working_hours

logger = logging.getLogger(__name__)

ADMIN_ID = int(Config.ADMIN_ID) if hasattr(Config, 'ADMIN_ID') and Config.ADMIN_ID else None
DB_PATH = Config.DATA_DIR / "recipes.db"


async def add_recipe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command /addrecipe — add a new recipe.
    Available only to the administrator.
    Format: /addrecipe Title | Ingredients | Instructions | Category
    """
    if ADMIN_ID is None:
        await update.message.reply_text(
            "❌ Admin not configured!\n"
            "Add ADMIN_ID=your_id to .env file"
        )
        return

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You don't have permission to use this command!")
        return

    if not is_working_hours():
        await update.message.reply_text("⏰ Bot works only from 9:00 to 20:00")
        return

    args = context.args
    if not args:
        await update.message.reply_text(
            "📝 *How to add a recipe:*\n\n"
            "`/addrecipe Title | Ingredients | Instructions | Category`\n\n"
            "📌 *Example:*\n"
            "`/addrecipe Chocolate Cake | Flour 200g, Sugar 150g, Cocoa 50g, Eggs 3pcs | Mix dry ingredients, add eggs, bake 40 minutes at 180°C | cakes`\n\n"
            "📂 *Categories:* cakes, pastries, cookies, muffins, pies, desserts, other",
            parse_mode="Markdown"
        )
        return

    full_text = " ".join(args)
    parts = full_text.split("|")

    if len(parts) < 3:
        await update.message.reply_text(
            "❌ Invalid format! Use `|` as separator.\n"
            "Example: `/addrecipe Title | Ingredients | Instructions | Category`",
            parse_mode="Markdown"
        )
        return

    title = parts[0].strip()
    ingredients = parts[1].strip()
    instructions = parts[2].strip()
    category = parts[3].strip() if len(parts) > 3 else "other"

    if not title or not ingredients or not instructions:
        await update.message.reply_text(
            "❌ All fields must be filled!\n"
            "Format: `/addrecipe Title | Ingredients | Instructions | Category`",
            parse_mode="Markdown"
        )
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO recipes (title, ingredients, instructions, category, source)
            VALUES (?, ?, ?, ?, ?)
        """, (title, ingredients, instructions, category, 'admin'))

        conn.commit()
        conn.close()

        await update.message.reply_text(
            f"✅ *Recipe added successfully!*\n\n"
            f"📌 *Title:* {title}\n"
            f"📂 *Category:* {category}\n"
            f"📝 *Ingredients:* {ingredients[:100]}{'...' if len(ingredients) > 100 else ''}\n"
            f"👩‍🍳 *Instructions:* {instructions[:100]}{'...' if len(instructions) > 100 else ''}\n\n"
            f"Now the recipe is available via /recipe! 🎂",
            parse_mode="Markdown"
        )

        logger.info(f"✅ Admin added recipe: {title}")

    except Exception as e:
        logger.error(f"❌ Error adding recipe: {e}")
        await update.message.reply_text(f"❌ Error adding recipe: {e}")


async def list_recipes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command /listrecipes — show last 20 recipes (admin only).
    """
    if ADMIN_ID is None:
        await update.message.reply_text("❌ Admin not configured!")
        return

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You don't have permission!")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, category FROM recipes ORDER BY id DESC LIMIT 20")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            await update.message.reply_text("📭 No recipes in the database.")
            return

        text = "📋 *Last 20 recipes:*\n\n"
        for row in rows:
            text += f"`{row[0]}`. {row[1]} — *{row[2]}*\n"

        await update.message.reply_text(text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"❌ Error getting recipe list: {e}")
        await update.message.reply_text(f"❌ Error: {e}")


async def del_recipe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command /delrecipe [id] — delete recipe by ID (admin only).
    """
    if ADMIN_ID is None:
        await update.message.reply_text("❌ Admin not configured!")
        return

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You don't have permission!")
        return

    args = context.args
    if not args:
        await update.message.reply_text(
            "📝 *How to delete a recipe:*\n\n"
            "`/delrecipe ID`\n\n"
            "To find the ID, use /listrecipes",
            parse_mode="Markdown"
        )
        return

    try:
        recipe_id = int(args[0])
    except ValueError:
        await update.message.reply_text("❌ ID must be a number!")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT title FROM recipes WHERE id = ?", (recipe_id,))
        row = cursor.fetchone()

        if not row:
            await update.message.reply_text(f"❌ Recipe with ID {recipe_id} not found!")
            conn.close()
            return

        title = row[0]

        cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()
        conn.close()

        await update.message.reply_text(
            f"✅ *Recipe deleted!*\n\n"
            f"📌 *Title:* {title}\n"
            f"🆔 *ID:* {recipe_id}",
            parse_mode="Markdown"
        )

        logger.info(f"✅ Admin deleted recipe: {title} (ID: {recipe_id})")

    except Exception as e:
        logger.error(f"❌ Error deleting recipe: {e}")
        await update.message.reply_text(f"❌ Error: {e}")


async def list_chats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command /listchats — show all subscribed chats (admin only).
    """
    if ADMIN_ID is None:
        await update.message.reply_text("❌ Admin not configured!")
        return

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You don't have permission!")
        return

    from bot.core.scheduler import get_active_chats
    chats = get_active_chats()

    if not chats:
        await update.message.reply_text("📭 No active subscriptions.")
        return

    text = "📋 *List of subscribed chats:*\n\n"
    for chat_id in chats:
        try:
            chat = await context.bot.get_chat(chat_id)
            chat_name = chat.title or chat.first_name or str(chat_id)
            text += f"• `{chat_id}` — {chat_name}\n"
        except Exception:
            text += f"• `{chat_id}` — (unknown)\n"

    await update.message.reply_text(text, parse_mode="Markdown")
