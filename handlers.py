import random
import time
from telegram import Update, ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

compliments = [
    "יפה מאוד!",
    "מדהים!",
    "אהבתי את זה!",
    "איזה תמונה מרהיבה!",
    "תמונה מדהימה!"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        f"ברוך הבא, {user.full_name}!\n\n"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # שליחת פעולת הקלדה
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    
    # שליחת מחמאה רנדומלית
    random_compliment = random.choice(compliments)
    await update.message.reply_text(random_compliment)
    
    # שליחת הודעת טעינה
    loading_message = await update.message.reply_text("טוען מספר רנדומלי...")
    # loading_message = await update.message.reply_text(emoji=random.choice(['🎲', '🎯', '🎰']))

    
    # המתנה של 2 שניות
    await asyncio.sleep(2)
    
    # יצירת מספר רנדומלי מפורמט
    random_number = random.randint(0, 999)
    formatted_number = str(random_number).zfill(3)
    
    # שליחת המספר הרנדומלי
    await update.message.reply_text(f"מספר רנדומלי: {formatted_number}")
    
    # מחיקת הודעת הטעינה
    await loading_message.delete()
