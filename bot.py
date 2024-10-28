from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN, WEBHOOK_URL, PORT
from handlers import handle_message, start

def setup_bot():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    
    application.add_handler(MessageHandler(filters.PHOTO | filters.VOICE, handle_message))

    return application

def run_webhook(application: Application):
    application.run_webhook(
        listen='0.0.0.0',
        port=PORT,
        url_path=TELEGRAM_BOT_TOKEN,
        webhook_url=f'{WEBHOOK_URL}/{TELEGRAM_BOT_TOKEN}'
    )
