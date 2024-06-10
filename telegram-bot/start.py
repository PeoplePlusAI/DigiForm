
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from read import read_file

hi_text = read_file('static/hi.txt')
lang_text = read_file('static/lang.txt')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=hi_text)
    choices = [
        InlineKeyboardButton("English", callback_data='english'),
        InlineKeyboardButton("हिन्दी", callback_data='hindi'),
    ]
    reply_markup = InlineKeyboardMarkup([[choice] for choice in choices])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=lang_text, reply_markup=reply_markup)
