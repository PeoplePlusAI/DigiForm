import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.env import TELEGRAM_BOT_TOKEN
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler
import telegram.ext.filters as filters
from start import start, language_button
from contact import handle_contact
from message import handle_message

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    language_button_handler = CallbackQueryHandler(language_button)
    application.add_handler(language_button_handler)

    contact_handler = MessageHandler(filters.CONTACT, handle_contact)
    application.add_handler(contact_handler)

    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    application.add_handler(message_handler)

    application.run_polling()
