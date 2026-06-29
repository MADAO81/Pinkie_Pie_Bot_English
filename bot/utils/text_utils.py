# bot/utils/text_utils.py
"""
Text utilities for Pinkie Pie bot.

Author: MADAO81
Version: 2.0
"""

import re
import random
from typing import List, Optional
from bot.core.constants import EMOJIS


def get_random_emoji(mood: str = "happy") -> str:
    """Returns a random emoji for the mood."""
    emoji_list = EMOJIS.get(mood, EMOJIS["neutral"])
    return random.choice(emoji_list)


def add_emojis_to_text(text: str, mood: str = "happy", count: int = 2) -> str:
    """Adds emojis to text."""
    emojis = [get_random_emoji(mood) for _ in range(count)]
    return f"{' '.join(emojis)} {text}"


def clean_text(text: str) -> str:
    """Cleans text from extra characters."""
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


def truncate_text(text: str, max_length: int = 1000, suffix: str = "...") -> str:
    """Truncates text to specified length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_user_message(message: str, username: Optional[str] = None) -> str:
    """Formats user message."""
    if username:
        return f"{username}: {message}"
    return message


def format_bot_response(response: str, with_emojis: bool = True) -> str:
    """Formats bot response."""
    if not with_emojis:
        return response

    if not any(char in response for char in ["🎈", "🎉", "⭐", "💖", "😊", "🌸"]):
        response += f" {get_random_emoji('happy')}"

    return response


def extract_hashtags(text: str) -> List[str]:
    """Extracts hashtags from text."""
    hashtags = re.findall(r'#\w+', text)
    return hashtags


def remove_mentions(text: str) -> str:
    """Removes mentions (@username) from text."""
    return re.sub(r'@\w+', '', text)


def is_question(text: str) -> bool:
    """Checks if text is a question."""
    question_words = ["what", "where", "when", "why", "how", "who", "which"]
    return (
        text.endswith("?") or
        any(word in text.lower() for word in question_words)
    )


def get_greeting() -> str:
    """Returns a greeting based on time of day."""
    from datetime import datetime
    hour = datetime.now().hour

    if 6 <= hour < 12:
        return "Good morning!"
    elif 12 <= hour < 18:
        return "Good afternoon!"
    elif 18 <= hour < 23:
        return "Good evening!"
    else:
        return "Good night!"
