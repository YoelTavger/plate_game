import csv
import random
import time
from datetime import datetime, timedelta
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

compliments = [
    "יפה מאוד!", "מדהים!", "אהבתי את זה!", "איזה תמונה מרהיבה!", "תמונה מדהימה!"
]
positive_emojis = [
    "😊", "😎", "🤩", "👏", "👍", "💪", "🎉", "✨", "🔥", "🥇", "🥳", "💥", "🌟", "💫", "🎊", "🏆"
]

# קבצים לשמירת נתונים
NUMBERS_FILE = 'numbers.txt'
USER_DATA_FILE = 'user_data.csv'
STATS_FILE = 'stats.csv'

def load_numbers():
    """טוען את המספרים מהקובץ."""
    try:
        with open(NUMBERS_FILE, 'r') as f:
            return [int(line.strip()) for line in f]
    except FileNotFoundError:
        return []

def save_numbers(numbers):
    """שומר את המספרים הנותרים."""
    with open(NUMBERS_FILE, 'w') as f:
        f.writelines(f"{num}\n" for num in numbers)

def load_user_data():
    """טוען שמות משתמשים מקובץ."""
    try:
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            return {row[0]: row[1] for row in reader}
    except FileNotFoundError:
        return {}

def save_user_data(user_id, username):
    """שומר משתמש חדש אם הוא לא רשום."""
    user_data = load_user_data()
    if str(user_id) not in user_data:
        with open(USER_DATA_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([user_id, username])

def log_game_data(user_id, username, random_number):
    """שומר סטטיסטיקות לקובץ."""
    with open(STATS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([user_id, username, random_number, datetime.now()])

def load_stats():
    """טוען נתוני סטטיסטיקה."""
    try:
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            return list(reader)
    except FileNotFoundError:
        return []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        f"ברוך הבא, {user.full_name}!\n\n"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    username = update.message.from_user.first_name
    save_user_data(user_id, username)

    # שליחת פעולת הקלדה
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    
    # שליחת מחמאה רנדומלית
    compliment = random.choice(compliments)
    emoji = random.choice(positive_emojis)
    await update.message.reply_text(f"{emoji} {compliment} {username}!")
    
    # ניהול מספרים רנדומליים
    numbers = load_numbers()
    if not numbers:
        await update.message.reply_text("😕 כל המספרים נגמרו להיום!")
        return

    random_number = random.choice(numbers)
    numbers.remove(random_number)
    save_numbers(numbers)
    log_game_data(user_id, username, random_number)

    # שליחת הודעת טעינה
    loading_message = await update.message.reply_text("🎲 טוען מספר רנדומלי...")
    time.sleep(2)
    
    # שליחת המספר הרנדומלי
    await update.message.reply_text(f"✨ המספר הבא: {str(random_number).zfill(3)}")
    
    # מחיקת הודעת הטעינה
    await loading_message.delete()

async def send_remaining_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """שולח את מספר המספרים שנותרו."""
    numbers = load
