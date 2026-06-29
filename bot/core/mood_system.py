# bot/core/mood_system.py
"""
Mood system for Pinkie Pie bot.

Author: MADAO81
Version: 2.0
"""

import random
from typing import Tuple, Optional, Dict
from bot.services.weather_service import WeatherService
from bot.config import Config


class MoodSystem:
    """Manages Pinkie Pie's mood based on weather."""

    def __init__(self):
        self.weather_service = WeatherService()
        self.sad_probability = Config.SAD_PROBABILITY
        self.current_mood = "happy"
        self.current_weather = None

    async def determine_mood(self) -> Tuple[str, Optional[Dict]]:
        """Determines mood based on current weather."""
        weather = await self.weather_service.get_weather()
        self.current_weather = weather

        if not weather:
            self.current_mood = "happy"
            return "happy", None

        if self.weather_service.is_bad_weather(weather):
            if random.random() < self.sad_probability:
                self.current_mood = "sad"
                return "sad", weather

        self.current_mood = "happy"
        return "happy", weather

    def get_mood_text(self, mood: str) -> str:
        """Returns text description of mood."""
        if mood == "sad":
            return "😔 Pinkamena Diane Pie is a little sad today... But she's still happy to see you!"
        return "🎈 Pinkie Pie is in a great mood! The party continues!"

    def get_mood_emoji(self, mood: str) -> str:
        """Returns emoji for current mood."""
        if mood == "sad":
            return "🌧️"
        return "🎈"

    def should_comment(self) -> bool:
        """Determines whether to comment (20% probability)."""
        return random.random() < 0.2

    def get_current_mood(self) -> str:
        """Returns current mood."""
        return self.current_mood

    def get_current_weather(self) -> Optional[Dict]:
        """Returns current weather data."""
        return self.current_weather
