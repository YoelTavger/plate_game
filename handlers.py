import random
import time
from telegram import Update

compliments = [
    "יפה מאוד!",
    "מדהים!",
    "אהבתי את זה!",
    "איזה תמונה מרהיבה!",
    "תמונה מדהימה!"
]

bot = telebot.TeleBot(API_TOKEN)

def start(update: Update):
    user = update.effective_user
    await update.message.reply_html(
        f"ברוך הבא, {user.full_name}!\n\n"
    )

def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)


def format_number(number):
    formatted_number = str(number).zfill(3)
    return formatted_number

@bot.message_handler(content_types=['photo'])
def send_random_compliment_and_number(message):
    random_compliment = random.choice(compliments)
    bot.reply_to(message, random_compliment)

    loading_message = bot.send_message(message.chat.id, "טוען מספר רנדומלי...")

    time.sleep(2)

    random_number = random.randint(0, 999)
    formatted_number = format_number(random_number)
    bot.send_message(message.chat.id, f"מספר רנדומלי: {formatted_number}")

    bot.delete_message(message.chat.id, loading_message.message_id)
