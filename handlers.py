import os  # הוספת מודול os
import random
import time
from datetime import datetime, timedelta
import csv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes
from config import STATS_FILE, NUMBERS_FILE, USER_DATA_FILE

# רשימות מחמאות ואימוג'ים לשיפור תגובות הבוט
compliments = [
    "וואו, איזה יופי!", "יצירת אומנות!", "מהמם!",
    "מדהים! יש לך עין טובה!", "פשוט קסום!"
]

positive_emojis = [
    "😊", "😎", "🤩", "👏", "👍", "💪", "🎉", "✨",
    "🔥", "🥇", "🥳", "💥", "🌟", "💫", "🎊", "🏆"
]

# פונקציה לטעינת מספרים מקובץ
def load_numbers():
    with open(NUMBERS_FILE, 'r') as f:
        return [int(line.strip()) for line in f]

# פונקציה לשמירת רשימת המספרים המעודכנת לקובץ
def save_numbers(numbers):
    with open(NUMBERS_FILE, 'w') as f:
        f.writelines(f"{num}\n" for num in numbers)

# פונקציה לטעינת שמות משתמשים מקובץ
def load_user_data():
    try:
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            return {row[0]: row[1] for row in reader}
    except FileNotFoundError:
        return {}

# פונקציה לשמירת משתמש חדש לקובץ אם הוא אינו קיים
def save_user_data(user_id, username):
    user_data = load_user_data()
    if str(user_id) not in user_data:
        with open(USER_DATA_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([user_id, username])

# פונקציה לשמירת סטטיסטיקות משתמשים לקובץ
def log_game_data(user_id, username, random_number):
    with open(STATS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([user_id, username, random_number, datetime.now()])

# פונקציה לקבלת שם משתמש מהקובץ או שם ברירת מחדל
def get_username(user_id, default_name):
    user_data = load_user_data()
    return user_data.get(str(user_id), default_name)

# פונקציה לבדוק וליצור קבצים אם הם לא קיימים
def create_files_if_not_exist():
    # יצירת קובץ מספרים אם הוא לא קיים
    if not os.path.exists(NUMBERS_FILE):
        with open(NUMBERS_FILE, 'w') as f:
            f.writelines(f"{i}\n" for i in range(0, 1000))  # ניתן לשנות את טווח המספרים לפי הצורך

    # יצירת קובץ סטטיסטיקות אם הוא לא קיים
    if not os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'username', 'number', 'timestamp']) 

    # יצירת קובץ משתמשים אם הוא לא קיים
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'username'])  # רשומת כותרת

# פונקציה ראשית לטיפול בהודעות תמונה ושילוב מחמאה ומספר רנדומלי
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = get_username(user_id, update.effective_user.full_name)
    save_user_data(user_id, username)

    # שליחת מחמאה עם אימוג'י מותאם אישית
    compliment = random.choice(compliments)
    emoji = random.choice(positive_emojis)
    await update.message.reply_text(f"{emoji} {compliment} {username}!")

    # שליפת מספרים מהקובץ ושמירת השינויים
    numbers = load_numbers()
    if not numbers:
        await update.message.reply_text("😕 כל המספרים נגמרו להיום!")
        return

    random_number = random.choice(numbers)
    numbers.remove(random_number)
    save_numbers(numbers)
    log_game_data(user_id, username, random_number)

    # הצגת טעינת מספר
    loading_message = await update.message.reply_text("🎲 זורק קוביה...")
    time.sleep(2)
    await loading_message.edit_text(f"✨ המספר הבא: {str(random_number).zfill(3)}")

# פונקציה לטעינת סטטיסטיקות מהקובץ
def load_stats():
    try:
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            return list(reader)
    except FileNotFoundError:
        return []

# קריאה לפונקציה ליצירת קבצים אם הם לא קיימים
create_files_if_not_exist()
