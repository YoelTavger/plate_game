from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN, WEBHOOK_URL, PORT
from handlers import handle_message, start

def setup_bot():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    
    application.add_handler(MessageHandler(filters.PHOTO, handle_message))
    
    # נוסיף פקודות נוספות לטופ מצטיינים
    application.add_handler(CommandHandler("מצטיין_יומי", send_top_players, period=1))
    application.add_handler(CommandHandler("מצטיין_שבועי", send_top_players, period=7))
    application.add_handler(CommandHandler("מצטיין_חודשי", send_top_players, period=30))
    application.add_handler(CommandHandler("מצטיין_כללי", send_top_players, period="all"))

    return application

def run_webhook(application: Application):
    application.run_webhook(
        listen='0.0.0.0',
        port=PORT,
        url_path=TELEGRAM_BOT_TOKEN,
        webhook_url=f'{WEBHOOK_URL}/{TELEGRAM_BOT_TOKEN}'
    )
