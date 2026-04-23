# ☕ Coffee Cleaning Schedule Bot

A Telegram bot that sends daily reminders at **4:30 PM Cambodia time** to your group, based on the weekly cleaning schedule in the Excel file.

---

## 📋 What It Does

- Reads `Coffee_Cleaning_Schedule_2026.xlsx` for the cleaning schedule
- Every day at **4:30 PM (Asia/Phnom_Penh)**, checks if today has a scheduled shift
- If yes → sends a reminder message to your Telegram group
- If no shift today → does nothing

---

## 🚀 Setup Guide

### Step 1: Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy the **bot token** (looks like `123456789:ABCdef...`)

### Step 2: Get Your Group Chat ID

1. Add your bot to the target Telegram group
2. Also add **@userinfobot** to the group — it will reply with the group ID
3. The group ID is a **negative number** like `-1001234567890`
4. You can remove @userinfobot after getting the ID

### Step 3: Set Up Locally (for testing)

```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your bot token and group ID

# Make sure the Excel file is in the project root
# Then run:
python bot.py
```

### Step 4: Deploy to Railway

1. Push your code to GitHub (make sure `.env` is in `.gitignore` — it is!)
2. Go to [railway.app](https://railway.app) and create a new project
3. Click **"Deploy from GitHub repo"** and select your repo
4. In Railway dashboard → your service → **Variables** tab, add:
   - `TELEGRAM_BOT_TOKEN` = your bot token
   - `TELEGRAM_GROUP_ID` = your group ID (e.g. `-1001234567890`)
   - `EXCEL_FILE` = `Coffee_Cleaning_Schedule_2026.xlsx`
5. Railway will auto-detect the `Procfile` and deploy as a **worker**

> ⚠️ **Important**: Upload `Coffee_Cleaning_Schedule_2026.xlsx` to your GitHub repo alongside `bot.py`.

---

## 📁 Project Structure

```
telegram-cleaning-bot/
├── bot.py                          # Main bot code
├── Coffee_Cleaning_Schedule_2026.xlsx  # The schedule (commit this to git)
├── requirements.txt                # Python dependencies
├── Procfile                        # Railway process type
├── runtime.txt                     # Python version
├── .env.example                    # Environment variable template
├── .env                            # Your secrets (DO NOT commit)
└── .gitignore
```

---

## 📨 Example Reminder Message

```
☕ Coffee Area Cleaning Reminder

📅 Date: Thursday, April 23, 2026
👥 Team: Camera Team

🧹 Assigned Members:
  • C.Raksmey
  • Chheangey

⏰ Please remember to clean the coffee area today. Thank you! 🙏
```

---

## 🔧 Customization

| What | Where | How |
|------|-------|-----|
| Change reminder time | `bot.py` line with `hour=16, minute=30` | Edit hour/minute (24h format) |
| Change message text | `build_message()` function in `bot.py` | Edit the f-string |
| Update schedule | `Coffee_Cleaning_Schedule_2026.xlsx` | Add/edit rows, re-deploy |

---

## 🛠 Troubleshooting

**Bot doesn't send messages?**
- Make sure the bot is an **admin** in the group (or at least has permission to send messages)
- Double-check `TELEGRAM_GROUP_ID` — it must include the `-` sign for groups

**Wrong timezone?**
- The bot uses `Asia/Phnom_Penh` (UTC+7). No changes needed for Cambodia.

**Railway keeps restarting?**
- Check Railway logs for errors. Most common cause is a wrong bot token or group ID.
