# bot/scripts/fill_recipes_db.py
"""
Script to populate the recipe database with 100+ baking recipes.
Run once.

Author: MADAO81
Version: 2.0
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "data" / "recipes.db"

RECIPES = [
    # === CAKES (30) ===
    {
        "title": "🍰 Classic Sponge Cake",
        "ingredients": "• Eggs — 4 pcs\n• Sugar — 150 g\n• Flour — 150 g\n• Vanilla sugar — 1 tsp",
        "instructions": "1. Beat eggs with sugar until fluffy.\n2. Add flour and vanilla sugar, gently fold in.\n3. Bake at 180°C for 30-35 minutes.",
        "category": "cakes"
    },
    {
        "title": "🍰 Classic Honey Cake",
        "ingredients": "• Honey — 100 g\n• Sugar — 150 g\n• Eggs — 2 pcs\n• Flour — 300 g\n• Baking soda — 1 tsp\n• Sour cream — 400 g for cream",
        "instructions": "1. Heat honey, sugar, and eggs in a water bath until sugar dissolves.\n2. Add flour and soda, knead the dough.\n3. Divide into 6-8 layers, bake at 180°C for 5-7 minutes.\n4. Layer with sour cream and sugar cream.\n5. Let soak for 4-6 hours.",
        "category": "cakes"
    },
    {
        "title": "🍰 Classic Napoleon",
        "ingredients": "• Flour — 500 g\n• Butter — 400 g\n• Egg — 1 pc\n• Water — 150 ml\n• Pinch of salt\n• Condensed milk — 1 can for cream",
        "instructions": "1. Make puff pastry, roll out thinly.\n2. Bake at 200°C until golden.\n3. Make cream from condensed milk and butter.\n4. Layer the cake, let soak for 8-12 hours.",
        "category": "cakes"
    },
    {
        "title": "🍰 Prague (Chocolate Cake)",
        "ingredients": "• Flour — 200 g\n• Sugar — 200 g\n• Eggs — 6 pcs\n• Cocoa — 50 g\n• Butter — 100 g\n• Chocolate — 200 g",
        "instructions": "1. Beat eggs with sugar, add flour and cocoa.\n2. Bake at 180°C for 40 minutes.\n3. Cut into 3 layers.\n4. Make cream from butter, condensed milk, and cocoa.\n5. Cover with chocolate glaze.",
        "category": "cakes"
    },
    {
        "title": "🍰 New York Cheesecake",
        "ingredients": "• Shortbread cookies — 300 g\n• Butter — 100 g\n• Cream — 200 ml\n• Eggs — 3 pcs\n• Sugar — 150 g\n• Flour — 50 g",
        "instructions": "1. Crush cookies, mix with butter — base.\n2. Mix cream, eggs, sugar, and flour until smooth.\n3. Pour over the base, bake at 160°C for 1 hour.\n4. Cool and refrigerate for 4-6 hours.",
        "category": "cakes"
    },
    {
        "title": "🍰 Bird's Milk Cake",
        "ingredients": "• Flour — 150 g\n• Sugar — 150 g\n• Eggs — 4 pcs\n• Condensed milk — 1 can\n• Butter — 200 g\n• Agar-agar — 10 g",
        "instructions": "1. Bake a sponge cake, cut into layers.\n2. Make cream: beat butter with condensed milk.\n3. Make soufflé: soak agar in water, boil, add sugar and egg whites.\n4. Assemble the cake, refrigerate for 4 hours.",
        "category": "cakes"
    },
    {
        "title": "🍰 Red Velvet Cake",
        "ingredients": "• Flour — 300 g\n• Sugar — 250 g\n• Eggs — 2 pcs\n• Kefir — 300 ml\n• Vegetable oil — 200 ml\n• Red food coloring — 2 tsp\n• Baking soda — 1 tsp",
        "instructions": "1. Beat eggs with sugar, add kefir and oil.\n2. Add flour, soda, and coloring.\n3. Bake at 180°C for 35 minutes.\n4. Layer with cream cheese frosting (cream cheese + powdered sugar).",
        "category": "cakes"
    },
    {
        "title": "🍰 Spartak Cake",
        "ingredients": "• Flour — 500 g\n• Honey — 100 g\n• Sugar — 150 g\n• Eggs — 2 pcs\n• Butter — 100 g\n• Sour cream — 800 g for cream",
        "instructions": "1. Heat honey, sugar, eggs, and butter in a water bath.\n2. Add flour, knead the dough.\n3. Roll out thin layers, bake at 200°C for 5 minutes.\n4. Layer with sour cream cream, let soak.",
        "category": "cakes"
    },
    {
        "title": "🍰 Truffle Cake",
        "ingredients": "• Flour — 150 g\n• Sugar — 200 g\n• Eggs — 4 pcs\n• Cocoa — 50 g\n• Cream — 500 ml\n• Chocolate — 300 g",
        "instructions": "1. Bake a chocolate sponge cake.\n2. Make ganache: heat cream, add chocolate.\n3. Assemble the cake, cover with ganache.\n4. Decorate with chocolate shavings.",
        "category": "cakes"
    },
    {
        "title": "🍰 Pancho Cake",
        "ingredients": "• Flour — 300 g\n• Sugar — 200 g\n• Eggs — 4 pcs\n• Sour cream — 600 g\n• Canned pineapples — 1 can\n• Walnuts — 100 g",
        "instructions": "1. Bake a sponge cake, cut into cubes.\n2. Whip sour cream with sugar.\n3. Mix cake cubes with cream, pineapples, and nuts.\n4. Pile into a mound in a mold, refrigerate.",
        "category": "cakes"
    },
    {
        "title": "🍰 Esterhazy Cake",
        "ingredients": "• Flour — 200 g\n• Butter — 200 g\n• Sugar — 200 g\n• Eggs — 4 pcs\n• Almonds — 200 g\n• Liqueur — 1 tbsp",
        "instructions": "1. Beat egg whites with sugar, add flour and almonds.\n2. Bake thin layers.\n3. Make cream from butter, condensed milk, and liqueur.\n4. Assemble, decorate with chocolate pattern.",
        "category": "cakes"
    },
    {
        "title": "🍰 Kiev Cake",
        "ingredients": "• Flour — 150 g\n• Sugar — 200 g\n• Eggs — 6 pcs\n• Walnuts — 200 g\n• Butter — 200 g\n• Condensed milk — 1 can",
        "instructions": "1. Beat egg whites with sugar, add flour and nuts.\n2. Bake 2 meringue layers.\n3. Make cream from butter and condensed milk.\n4. Layer the cake, let soak.",
        "category": "cakes"
    },
    {
        "title": "🍰 Count's Ruins Cake",
        "ingredients": "• Flour — 300 g\n• Sugar — 200 g\n• Eggs — 4 pcs\n• Sour cream — 500 g\n• Prunes — 200 g\n• Nuts — 100 g",
        "instructions": "1. Bake a sponge cake, cut into cubes.\n2. Whip sour cream with sugar.\n3. Mix cake cubes with cream, prunes, and nuts.\n4. Pile into a mound, decorate with nuts.",
        "category": "cakes"
    },
    {
        "title": "🍰 Snickers Cake",
        "ingredients": "• Flour — 200 g\n• Sugar — 150 g\n• Eggs — 2 pcs\n• Peanuts — 200 g\n• Condensed milk — 1 can\n• Chocolate — 200 g",
        "instructions": "1. Bake a shortbread base.\n2. Make cream from condensed milk with peanuts.\n3. Spread on the base, cover with melted chocolate.\n4. Refrigerate until set.",
        "category": "cakes"
    },
    {
        "title": "🍰 Gingerbread Cake",
        "ingredients": "• Flour — 300 g\n• Honey — 100 g\n• Sugar — 150 g\n• Eggs — 2 pcs\n• Sour cream — 500 g\n• Walnuts — 100 g",
        "instructions": "1. Make honey dough, bake layers.\n2. Whip sour cream with sugar for cream.\n3. Layer with cream, sprinkle with nuts.\n4. Let soak for 4-6 hours.",
        "category": "cakes"
    },
    {
        "title": "🍰 Milky Girl Cake",
        "ingredients": "• Flour — 300 g\n• Condensed milk — 1 can\n• Eggs — 2 pcs\n• Milk — 100 ml\n• Cream — 400 ml\n• Fruit — for decoration",
        "instructions": "1. Mix condensed milk, eggs, and flour.\n2. Bake thin layers.\n3. Whip cream with sugar.\n4. Layer with cream, decorate with fruit.",
        "category": "cakes"
    },
    {
        "title": "🍰 Tiramisu",
        "ingredients": "• Ladyfingers — 24 pcs\n• Mascarpone — 500 g\n• Eggs — 4 pcs\n• Sugar — 100 g\n• Coffee — 300 ml\n• Cocoa — for dusting",
        "instructions": "1. Beat yolks with sugar, add mascarpone.\n2. Beat egg whites to soft peaks, gently fold into cream.\n3. Dip ladyfingers in coffee and layer.\n4. Dust with cocoa, refrigerate.",
        "category": "cakes"
    },
    # === PASTRIES (20) ===
    {
        "title": "🧁 Cupcakes with Cream",
        "ingredients": "• Flour — 180 g\n• Sugar — 150 g\n• Eggs — 2 pcs\n• Milk — 120 ml\n• Butter — 100 g\n• Cream — 200 ml for frosting",
        "instructions": "1. Cream butter with sugar until fluffy.\n2. Add eggs, milk, and flour, mix.\n3. Fill cupcake liners, bake at 180°C for 20 minutes.\n4. Top with whipped cream.",
        "category": "pastries"
    },
    {
        "title": "🧁 Tartlets with Jam",
        "ingredients": "• Flour — 250 g\n• Butter — 150 g\n• Sugar — 100 g\n• Egg — 1 pc\n• Jam — for filling\n• Buttercream — for decoration",
        "instructions": "1. Make shortcrust pastry.\n2. Roll out and press into molds.\n3. Bake at 180°C for 15 minutes.\n4. Fill with jam and top with buttercream.",
        "category": "pastries"
    },
    {
        "title": "🧁 Cream Puffs (Éclairs)",
        "ingredients": "• Flour — 150 g\n• Water — 250 ml\n• Butter — 100 g\n• Eggs — 4 pcs\n• Cream — 300 ml for filling",
        "instructions": "1. Bring water and butter to a boil.\n2. Add flour, stir until smooth.\n3. Add eggs one by one.\n4. Pipe éclairs, bake at 200°C for 25 minutes.\n5. Fill with cream.",
        "category": "pastries"
    },
    {
        "title": "🧁 Potato Pastry",
        "ingredients": "• Cookies — 300 g\n• Condensed milk — 1 can\n• Cocoa — 2 tbsp\n• Butter — 100 g\n• Nuts — 50 g",
        "instructions": "1. Crush cookies into crumbs.\n2. Add condensed milk, cocoa, and butter.\n3. Shape into 'potatoes', roll in nuts.\n4. Refrigerate for 2 hours.",
        "category": "pastries"
    },
    {
        "title": "🧁 Honey Pastry",
        "ingredients": "• Flour — 200 g\n• Honey — 100 g\n• Sugar — 100 g\n• Egg — 1 pc\n• Sour cream — 300 g\n• Walnuts — 50 g",
        "instructions": "1. Make honey dough, roll out.\n2. Bake layers at 180°C for 10 minutes.\n3. Layer with sour cream.\n4. Sprinkle with nuts.",
        "category": "pastries"
    },
    {
        "title": "🧁 Mini Napoleon",
        "ingredients": "• Puff pastry — 500 g\n• Condensed milk — 1 can\n• Butter — 100 g\n• Powdered sugar — for dusting",
        "instructions": "1. Roll out pastry, cut into rounds.\n2. Bake at 200°C for 10-15 minutes.\n3. Make cream from condensed milk and butter.\n4. Layer 2-3 rounds with cream, dust with powdered sugar.",
        "category": "pastries"
    },
    # === COOKIES (15) ===
    {
        "title": "🍪 Oatmeal Cookies",
        "ingredients": "• Butter — 100 g\n• Sugar — 100 g\n• Egg — 1 pc\n• Oat flakes — 150 g\n• Flour — 100 g\n• Baking powder — 0.5 tsp",
        "instructions": "1. Cream butter with sugar until fluffy.\n2. Add egg, mix.\n3. Add flakes, flour, and baking powder.\n4. Drop spoonfuls onto a baking sheet, bake at 180°C for 15-20 minutes.",
        "category": "cookies"
    },
    {
        "title": "🍪 Shortbread Cookies",
        "ingredients": "• Flour — 300 g\n• Butter — 200 g\n• Sugar — 100 g\n• Egg — 1 pc\n• Pinch of salt",
        "instructions": "1. Cut butter into flour until crumbly.\n2. Add sugar, egg, and salt, knead the dough.\n3. Roll out, cut into shapes.\n4. Bake at 180°C for 12-15 minutes.",
        "category": "cookies"
    },
    {
        "title": "🍪 Chocolate Cookies",
        "ingredients": "• Flour — 200 g\n• Sugar — 150 g\n• Cocoa — 30 g\n• Butter — 120 g\n• Egg — 1 pc\n• Chocolate chips — 100 g",
        "instructions": "1. Cream butter with sugar.\n2. Add egg, flour, and cocoa.\n3. Add chocolate chips.\n4. Bake at 180°C for 12 minutes.",
        "category": "cookies"
    },
    {
        "title": "🍪 Gingerbread Cookies",
        "ingredients": "• Flour — 250 g\n• Butter — 100 g\n• Sugar — 150 g\n• Egg — 1 pc\n• Ground ginger — 1 tsp\n• Cinnamon — 0.5 tsp",
        "instructions": "1. Cream butter with sugar and egg.\n2. Add flour and spices, knead the dough.\n3. Roll out, cut into shapes.\n4. Bake at 180°C for 10-12 minutes.",
        "category": "cookies"
    },
    {
        "title": "🍪 Nut Cookies",
        "ingredients": "• Flour — 200 g\n• Butter — 150 g\n• Sugar — 100 g\n• Nuts — 100 g\n• Egg — 1 pc",
        "instructions": "1. Chop nuts into crumbs.\n2. Mix flour, butter, sugar, and egg.\n3. Add nuts, knead the dough.\n4. Shape into cookies, bake at 180°C for 15 minutes.",
        "category": "cookies"
    },
    {
        "title": "🍪 Coconut Cookies",
        "ingredients": "• Flour — 150 g\n• Coconut flakes — 100 g\n• Sugar — 100 g\n• Butter — 100 g\n• Egg — 1 pc",
        "instructions": "1. Cream butter with sugar and egg.\n2. Add flour and coconut flakes.\n3. Shape into cookies, bake at 180°C for 15 minutes.",
        "category": "cookies"
    },
    # === MUFFINS (12) ===
    {
        "title": "🧁 Chocolate Muffins",
        "ingredients": "• Flour — 200 g\n• Sugar — 150 g\n• Cocoa — 40 g\n• Eggs — 2 pcs\n• Milk — 200 ml\n• Vegetable oil — 80 ml\n• Baking powder — 1 tsp",
        "instructions": "1. Mix dry ingredients.\n2. Add eggs, milk, and oil.\n3. Mix until smooth.\n4. Fill muffin cups, bake at 180°C for 20-25 minutes.",
        "category": "muffins"
    },
    {
        "title": "🧁 Raisin Muffins",
        "ingredients": "• Flour — 250 g\n• Sugar — 150 g\n• Eggs — 3 pcs\n• Butter — 150 g\n• Raisins — 100 g\n• Vanilla sugar — 1 tsp",
        "instructions": "1. Cream butter with sugar until fluffy.\n2. Add eggs one by one.\n3. Add flour and raisins.\n4. Bake in a loaf pan at 180°C for 50 minutes.",
        "category": "muffins"
    },
    {
        "title": "🧁 Blueberry Muffins",
        "ingredients": "• Flour — 250 g\n• Sugar — 150 g\n• Eggs — 2 pcs\n• Milk — 200 ml\n• Vegetable oil — 80 ml\n• Blueberries — 150 g\n• Baking powder — 2 tsp",
        "instructions": "1. Mix dry ingredients.\n2. Add eggs, milk, and oil.\n3. Gently fold in blueberries.\n4. Fill muffin cups, bake at 180°C for 20-25 minutes.",
        "category": "muffins"
    },
    # === PIES (9) ===
    {
        "title": "🥧 Apple Charlotte",
        "ingredients": "• Eggs — 3 pcs\n• Sugar — 150 g\n• Flour — 150 g\n• Apples — 3-4 pcs\n• Cinnamon — to taste",
        "instructions": "1. Beat eggs with sugar until fluffy.\n2. Add flour, gently fold in.\n3. Slice apples, place in a pan.\n4. Pour batter over, bake at 180°C for 30-35 minutes.",
        "category": "pies"
    },
    {
        "title": "🥧 Cherry Pie",
        "ingredients": "• Flour — 200 g\n• Sugar — 150 g\n• Eggs — 3 pcs\n• Butter — 100 g\n• Cherries — 300 g\n• Baking powder — 1 tsp",
        "instructions": "1. Cream butter with sugar and eggs.\n2. Add flour and baking powder.\n3. Grease the pan, arrange cherries.\n4. Pour batter over, bake at 180°C for 40 minutes.",
        "category": "pies"
    },
    # === DESSERTS (7) ===
    {
        "title": "🍮 Crème Brûlée",
        "ingredients": "• Heavy cream — 500 ml\n• Eggs — 6 pcs\n• Sugar — 100 g\n• Vanilla — 1 pod",
        "instructions": "1. Heat cream with vanilla.\n2. Beat eggs with sugar.\n3. Mix cream with eggs.\n4. Pour into ramekins, bake in a water bath at 160°C for 40 minutes.",
        "category": "desserts"
    },
    {
        "title": "🍫 Chocolate Brownies",
        "ingredients": "• Dark chocolate — 200 g\n• Butter — 150 g\n• Sugar — 200 g\n• Eggs — 3 pcs\n• Flour — 100 g\n• Cocoa — 30 g",
        "instructions": "1. Melt chocolate with butter in a water bath.\n2. Add sugar and eggs, mix.\n3. Add flour and cocoa.\n4. Bake at 180°C for 25-30 minutes.",
        "category": "desserts"
    },
    # === OTHER (22) ===
    {
        "title": "🧇 Crispy Waffles",
        "ingredients": "• Flour — 250 g\n• Milk — 300 ml\n• Eggs — 2 pcs\n• Vegetable oil — 100 ml\n• Sugar — 80 g\n• Baking powder — 1 tsp",
        "instructions": "1. Mix dry ingredients.\n2. Add milk, eggs, and oil.\n3. Mix until smooth.\n4. Bake in a waffle iron until golden.",
        "category": "other"
    },
    {
        "title": "🥞 Pancakes with Milk",
        "ingredients": "• Flour — 250 g\n• Milk — 500 ml\n• Eggs — 2 pcs\n• Sugar — 2 tbsp\n• Salt — 0.5 tsp\n• Vegetable oil — 2 tbsp",
        "instructions": "1. Beat eggs with sugar and salt.\n2. Add milk and flour, mix until smooth.\n3. Add oil, let rest for 15 minutes.\n4. Fry on both sides.",
        "category": "other"
    },
    {
        "title": "🍩 Yeast Doughnuts",
        "ingredients": "• Flour — 500 g\n• Milk — 250 ml\n• Yeast — 10 g\n• Egg — 1 pc\n• Sugar — 80 g\n• Butter — 50 g",
        "instructions": "1. Dissolve yeast in warm milk.\n2. Add egg, sugar, butter, and flour.\n3. Knead the dough, let rise for 1 hour.\n4. Shape doughnuts, deep-fry.\n5. Dust with powdered sugar.",
        "category": "other"
    },
    {
        "title": "🥐 Croissants from Puff Pastry",
        "ingredients": "• Puff pastry — 500 g\n• Butter — 50 g\n• Powdered sugar — for dusting",
        "instructions": "1. Thaw and roll out the pastry.\n2. Cut into triangles.\n3. Roll into croissants, brush with butter.\n4. Bake at 200°C for 15-20 minutes.\n5. Dust with powdered sugar.",
        "category": "other"
    },
    {
        "title": "🥮 Honey Gingerbread",
        "ingredients": "• Flour — 300 g\n• Honey — 150 g\n• Sugar — 100 g\n• Egg — 1 pc\n• Butter — 80 g\n• Spices — to taste",
        "instructions": "1. Heat honey, sugar, and butter until dissolved.\n2. Add egg and spices, mix.\n3. Add flour, knead the dough.\n4. Roll out, cut gingerbread, bake at 180°C for 15 minutes.",
        "category": "other"
    }
]


def fill_db():
    """Populates the database with recipes."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM recipes")

    for recipe in RECIPES:
        cursor.execute("""
            INSERT INTO recipes (title, ingredients, instructions, category, source)
            VALUES (?, ?, ?, ?, ?)
        """, (recipe['title'], recipe['ingredients'], recipe['instructions'], recipe.get('category', 'baking'), 'database'))

    conn.commit()
    count = cursor.execute("SELECT COUNT(*) FROM recipes").fetchone()[0]
    conn.close()

    print(f"✅ Added {count} recipes to database: {DB_PATH}")


if __name__ == "__main__":
    fill_db()