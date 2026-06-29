# 🦄 Pinkie Pie Bot — English Version

A fun and friendly Telegram bot based on Pinkie Pie from "My Little Pony: Friendship is Magic".

> **Status:** 🚧 **Under construction**
>
> This is an English version of the original Pinkie Pie bot. The Russian version is available at [Pinkie_Pie_Bot_Telegram_Rus](https://github.com/MADAO81/Pinkie_Pie_Bot_Telegram_Rus).
>
> 👨‍💻 *Author: MADAO81*

---

## 📖 About the Project

Pinkie Pie is an interactive bot that:

- 🎉 Talks in character: cheerful, energetic, and friendly
- 🧁 Shares baking recipes (built-in recipe book)
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
| Recipes | **SQLite** (built-in recipe book) |
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
| `/weather` | Weather in the default location |
| `/weather London` | Weather in any city |
| `/subscribe` | Subscribe to daily recipes |
| `/unsubscribe` | Unsubscribe from daily recipes |

### 👑 Admin commands (for the owner)

| Command | Description |
|---------|-------------|
| `/addrecipe` | Add a new recipe to the database |
| `/listrecipes` | Show last 20 recipes |
| `/delrecipe` | Delete a recipe by ID |
| `/listchats` | Show all subscribed chats |

---

## 📄 License

MIT License — free use with attribution.

---

## 👨‍💻 Author

**MADAO81** — development and support.

---

**🎈 Made with love and friendship!**
