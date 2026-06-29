# 🦄 Pinkie Pie Bot — English Version

A fun and friendly Telegram bot based on Pinkie Pie from "My Little Pony: Friendship is Magic".

> **Status:** ✅ **Active development**
>
> This is an English version of the original Pinkie Pie bot. The Russian version is available at [Pinkie_Pie_Bot_Telegram_Rus](https://github.com).
>
> 👨‍💻 *Author: MADAO81*

---

## 📖 About the Project

Pinkie Pie is an interactive bot that:

- 🎉 Talks in character: cheerful, energetic, and friendly
- 🧁 Shares baking recipes (built-in recipe book with 100+ recipes)
- 🎶 Tells jokes and sings songs
- 🌦️ Changes mood depending on the weather
- 🌍 Shows weather in any city (with language support)
- 📝 Comments on messages in groups (20% probability)
- 🎙️ Recognizes voice messages (Whisper) with 20% probability
- 🖼️ Analyzes images (GPT-4 Vision) with 20% probability
- 🧁 Daily recipe subscriptions
- ⏰ Working hours: 9:00–20:00
- 💾 Stores conversation history (30 days)

---

## 🛠️ Technologies

| Component | Technology |
|-----------|------------|
| Platform | **Telegram** |
| AI Provider | **OpenAI GPT-4-turbo** |
| Voice Recognition | **OpenAI Whisper** |
| Image Analysis | **OpenAI Vision API** |
| Weather | **Open-Meteo** (free, no API key) |
| Recipes | **SQLite** (100+ baking recipes) |
| Language | Python 3.11+ |
| Database | SQLite |
| Deployment | SprintBox (systemd) |

---

## 📋 Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/help` | Help and commands |
| `/recipe` | Get a random baking recipe |
| `/joke` | Tell a joke |
| `/song` | Sing a song |
| `/weather` | Weather in default location |
| `/weather London` | Weather in any city |
| `/subscribe` | Subscribe to daily recipes |
| `/unsubscribe` | Unsubscribe from daily recipes |

### 👑 Admin Commands (for the owner)

| Command | Description |
|---------|-------------|
| `/addrecipe` | Add a new recipe to the database |
| `/listrecipes` | Show last 20 recipes |
| `/delrecipe` | Delete a recipe by ID |
| `/listchats` | Show all subscribed chats |

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com
cd Pinkie_Pie_Bot_English
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your keys:

```env
# Telegram
TELEGRAM_TOKEN=your_bot_token_from_BotFather

# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4-turbo

# Default location (Vorsino, Borovsky District)
DEFAULT_LAT=55.0965
DEFAULT_LON=36.6355

# Bot settings
WORK_START_HOUR=9
WORK_END_HOUR=20
SAD_PROBABILITY=0.2
CONTEXT_EXPIRE_DAYS=30
RECIPE_SEND_TIME=12:00

# Admin (set your Telegram ID)
ADMIN_ID=your_telegram_id

# Default chats for daily recipes
DEFAULT_CHATS=-1001234567890,123456789
```

### 5. Create recipe database

```bash
python bot/scripts/create_recipe_db.py
python bot/scripts/fill_recipes_db.py
```

### 6. Run the bot

```bash
python run.py
```

---

## 📁 Project Structure

```text
Pinkie_Pie_Bot_English/
├── .env                      # Environment variables (DO NOT PUSH!)
├── .env.example              # Example environment variables
├── .gitignore                # Git ignore file
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── run.py                    # Entry point
│
├── bot/                      # Main code
│   ├── __init__.py
│   ├── config.py             # Configuration
│   ├── main.py               # Initialization and launch
│   │
│   ├── handlers/             # Handlers
│   │   ├── __init__.py
│   │   ├── commands.py       # /start, /help, /recipe, /joke, /song, /weather, /subscribe, /unsubscribe
│   │   ├── admin.py          # /addrecipe, /listrecipes, /delrecipe, /listchats
│   │   ├── messages.py       # Text messages
│   │   ├── photos.py         # Photo handling (Vision API)
│   │   └── voice.py          # Voice handling (Whisper)
│   │
│   ├── core/                 # Core logic
│   │   ├── __init__.py
│   │   ├── constants.py      # Constants and system prompt
│   │   ├── mood_system.py    # Mood system
│   │   ├── context_manager.py # Conversation history
│   │   └── scheduler.py      # Scheduler (daily recipes)
│   │
│   ├── scripts/              # Helper scripts
│   │   ├── create_recipe_db.py  # Create recipe DB
│   │   └── fill_recipes_db.py   # Populate recipe DB
│   │
│   ├── services/             # External services
│   │   ├── __init__.py
│   │   ├── ai_service.py     # OpenAI (GPT-4-turbo + Vision + Whisper)
│   │   ├── weather_service.py # Open-Meteo (weather in any city)
│   │   └── recipe_service.py # Recipe database service
│   │
│   └── utils/                # Utilities
│       ├── __init__.py
│       ├── time_utils.py     # Time utilities
│       ├── text_utils.py     # Text utilities
│       └── file_utils.py     # File utilities
│
├── data/                     # Data
│   ├── conversations.db      # SQLite conversation history
│   ├── recipes.db            # SQLite recipe database
│   └── audio/                # Temporary audio storage
│
├── logs/                     # Logs
│   └── bot.log
│
└── tests/                    # Tests
    └── __init__.py
```

---

## 🌤️ Weather

### Default Location (Vorsino)
* **Coordinates:** 55.0965, 36.6355
* Pinkie Pie's mood depends on weather in Vorsino.
* Probability of sadness in bad weather: 20%.

### Any City
Supports queries in English.

Examples:
* `/weather London`
* `/weather New York`
* `/weather Tokyo`

---

## 🧁 Recipes

- SQLite database with 100+ baking recipes.
- Fallback recipes in code (in case of database errors).
- **Categories:** cakes, pastries, cookies, muffins, pies, desserts, other.
- Daily recipe at 12:00 via `/subscribe`.

---

## 📝 Behavior Features

### 🎯 Group Message Reactions

| Situation | Behavior |
|:---|:---|
| Bot mention (`@username`) | ✅ Always responds |
| Reply to bot's message | ✅ Always responds |
| Regular message (no mention) | ✅ 20% probability |
| Private message | ✅ Always responds |

### 🎯 Media Reactions

| Type | Response Probability |
|:---|:---|
| Photos | 20% |
| Voice messages | 20% |

### ⏰ Working Hours
* **Monday — Sunday:** 9:00 — 20:00
* Outside working hours: ignores group messages. In private messages replies: *"I'm resting, come back tomorrow!"*

### 🌤️ Mood System
Pinkie Pie's mood depends on weather in Vorsino (Borovsky District):

| Weather | Sadness Probability | State |
|:---|:---:|:---|
| ☀️ Clear, sunny | 0% | 🎈 Pinkie Pie (happy) |
| ⛅ Cloudy | 0% | 🎈 Pinkie Pie (happy) |
| 🌧️ Rain, overcast | 20% | 😔 Pinkamena Diane Pie (sad) |
| ❄️ Snow | 20% | 😔 Pinkamena Diane Pie (sad) |
| ⛈️ Thunderstorm | 20% | 😔 Pinkamena Diane Pie (sad) |

---

## 🚀 Deployment on Server

### systemd Management

```bash
# Start bot
systemctl start pinkie-bot

# Stop bot
systemctl stop pinkie-bot

# Restart bot
systemctl restart pinkie-bot

# Check status
systemctl status pinkie-bot

# View logs
journalctl -u pinkie-bot -f
```

### Update via Git

```bash
systemctl stop pinkie-bot
git pull origin main
systemctl start pinkie-bot
```

---

## 🐛 Reporting Issues
If you find a bug or have suggestions, create an Issue on GitHub or contact the author.

## 📄 License
MIT License — free use with attribution.

## 👨‍💻 Author
MADAO81 — development and support.

## 🙏 Acknowledgements
* **python-telegram-bot** — Telegram Bot API library
* **OpenAI** — GPT-4-turbo, Vision API, Whisper
* **Open-Meteo** — free weather API (no key required)
* **SprintBox** — deployment platform

🎈 *Made with love and friendship!*
