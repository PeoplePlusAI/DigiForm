from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.io import read_file
from utils.languages import languages
from utils.reqs import post_request
from utils.env import PORT

hi_text = read_file('static/chat/hi.txt')
lang_text = read_file('static/chat/lang.txt')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = post_request(f"http://backend:{PORT}/api/clear/", {"client_id": f"tg:{update.effective_user.id}"})
    await context.bot.send_message(chat_id=update.effective_chat.id, text=hi_text)
    choices = [
        InlineKeyboardButton(l, callback_data=c) for l,c in languages.items()
    ]
    reply_markup = InlineKeyboardMarkup([[choice] for choice in choices])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=lang_text, reply_markup=reply_markup)
