# bot/utils/time_utils.py
"""
Time utilities for Pinkie Pie bot.

Author: MADAO81
Version: 2.0
"""

from datetime import datetime
from bot.config import Config


def is_working_hours() -> bool:
    """Checks if bot is currently in working hours."""
    now = datetime.now()
    current_hour = now.hour
    return Config.WORK_START_HOUR <= current_hour < Config.WORK_END_HOUR


def get_working_status_message() -> str:
    """Returns message about working status."""
    if is_working_hours():
        return None

    return (
        "🌸 Hi! I'm resting right now, my working hours are "
        f"{Config.WORK_START_HOUR}:00 to {Config.WORK_END_HOUR}:00.\n\n"
        "Come back tomorrow — I'd love to chat! "
        "In the meantime, you can check out recipes on food.ru 🧁\n\n"
        "Good night! 🌙"
    )


def get_current_time() -> str:
    """Returns current time in HH:MM format."""
    now = datetime.now()
    return now.strftime("%H:%M")


def get_current_date() -> str:
    """Returns current date in DD.MM.YYYY format."""
    now = datetime.now()
    return now.strftime("%d.%m.%Y")


def get_weekday() -> str:
    """Returns current weekday name in English."""
    weekdays = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    now = datetime.now()
    return weekdays.get(now.weekday(), "Unknown")
