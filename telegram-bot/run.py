import os
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler
import telegram.ext.filters as filters
from start import start
from language import language_button
from contact import handle_contact
from message import message

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    language_button_handler = CallbackQueryHandler(language_button)
    application.add_handler(language_button_handler)

    contact_handler = MessageHandler(filters.CONTACT, handle_contact)
    application.add_handler(contact_handler)

    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, message)
    application.add_handler(message_handler)

    application.run_polling()
