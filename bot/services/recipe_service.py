# bot/services/recipe_service.py
"""
Recipe service using SQLite database.
If DB is unavailable — uses fallback recipes.

Author: MADAO81
Version: 2.0
"""

import logging
import sqlite3
import random
from typing import Optional, Dict, List
from pathlib import Path
from bot.config import Config

logger = logging.getLogger(__name__)

DB_PATH = Config.DATA_DIR / "recipes.db"


class RecipeService:
    """
    Recipe service using SQLite database.
    """

    def __init__(self):
        self.db_path = DB_PATH
        self._init_db()

    def _init_db(self):
        """Checks if database exists."""
        if not self.db_path.exists():
            logger.warning(f"⚠️ Recipe database not found: {self.db_path}")
            logger.warning("⚠️ Will use fallback recipes")

    def _get_connection(self):
        """Returns database connection."""
        return sqlite3.connect(self.db_path)

    async def get_random_recipe(self) -> Optional[Dict]:
        """
        Returns a random recipe from DB.
        If DB is unavailable — uses fallback.
        """
        recipe = await self._get_recipe_from_db()
        if recipe:
            return recipe

        logger.info("📖 Using fallback recipe")
        return self._get_fallback_recipe()

    async def _get_recipe_from_db(self) -> Optional[Dict]:
        """
        Returns random recipe from database.
        """
        try:
            if not self.db_path.exists():
                return None

            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT title, ingredients, instructions, category
                FROM recipes
                ORDER BY RANDOM()
                LIMIT 1
            """)

            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    "title": row[0],
                    "ingredients": row[1],
                    "instructions": row[2],
                    "category": row[3]
                }
            return None

        except Exception as e:
            logger.error(f"❌ Error getting recipe from DB: {e}")
            return None

    def _get_fallback_recipe(self) -> Dict:
        """Returns a random fallback recipe."""
        recipes = [
            {
                "title": "🍰 Classic Sponge Cake",
                "ingredients": "• Eggs — 4 pcs\n• Sugar — 150 g\n• Flour — 150 g\n• Vanilla sugar — 1 tsp",
                "instructions": "1. Beat eggs with sugar until fluffy.\n2. Add flour and vanilla sugar, gently fold in.\n3. Bake at 180°C for 30-35 minutes."
            },
            {
                "title": "🧁 Chocolate Muffins",
                "ingredients": "• Flour — 200 g\n• Sugar — 150 g\n• Cocoa — 40 g\n• Eggs — 2 pcs\n• Milk — 200 ml\n• Oil — 80 ml",
                "instructions": "1. Mix dry ingredients.\n2. Add eggs, milk, and oil.\n3. Mix until smooth.\n4. Bake at 180°C for 20-25 minutes."
            },
            {
                "title": "🥞 Pancakes with Milk",
                "ingredients": "• Flour — 250 g\n• Milk — 500 ml\n• Eggs — 2 pcs\n• Sugar — 2 tbsp\n• Salt — 0.5 tsp",
                "instructions": "1. Beat eggs with sugar and salt.\n2. Add milk and flour, mix until smooth.\n3. Add oil, let rest for 15 minutes.\n4. Fry on both sides."
            },
            {
                "title": "🍪 Oatmeal Cookies",
                "ingredients": "• Butter — 100 g\n• Sugar — 100 g\n• Egg — 1 pc\n• Oat flakes — 150 g\n• Flour — 100 g",
                "instructions": "1. Cream butter with sugar.\n2. Add egg, mix.\n3. Add flakes and flour.\n4. Bake at 180°C for 15-20 minutes."
            },
            {
                "title": "🍰 Classic Honey Cake",
                "ingredients": "• Honey — 100 g\n• Sugar — 150 g\n• Eggs — 2 pcs\n• Flour — 300 g\n• Baking soda — 1 tsp\n• Sour cream — 400 g for cream",
                "instructions": "1. Heat honey, sugar, and eggs in a water bath.\n2. Add flour and soda, knead the dough.\n3. Divide into layers, bake at 180°C for 5-7 minutes.\n4. Layer with sour cream and sugar cream."
            }
        ]
        return random.choice(recipes)

    async def search_recipes(self, query: str) -> List[Dict]:
        """Search recipes by query."""
        results = []
        try:
            if not self.db_path.exists():
                return results

            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT title, ingredients, instructions, category
                FROM recipes
                WHERE title LIKE ? OR ingredients LIKE ?
                LIMIT 10
            """, (f'%{query}%', f'%{query}%'))

            for row in cursor.fetchall():
                results.append({
                    "title": row[0],
                    "ingredients": row[1],
                    "instructions": row[2],
                    "category": row[3]
                })
            conn.close()

        except Exception as e:
            logger.error(f"❌ Error searching: {e}")

        return results
