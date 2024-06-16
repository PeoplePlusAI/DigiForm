from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.io import read_file
from utils.languages import languages
from utils.reqs import get_request, post_request
from utils.env import PORT

hi_text = read_file('static/chat/hi.txt')
lang_text = read_file('static/chat/lang.txt')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = get_request(f"http://backend:{PORT}/api/details/", {"client_id": f"tg:{update.effective_user.id}"})
    await context.bot.send_message(chat_id=update.effective_chat.id, text=hi_text)
    choices = [
        InlineKeyboardButton(l, callback_data=c) for l,c in languages.items()
    ]
    reply_markup = InlineKeyboardMarkup([[choice] for choice in choices])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=lang_text, reply_markup=reply_markup)

async def language_button(update, context):
    query = update.callback_query
    await query.answer()
    client_id = update.effective_user.id
    _ = post_request(f"http://backend:{PORT}/api/update/", {"client_id": f"tg:{client_id}", "details": {"chat_preferred_language": query.data}})
    await context.bot.send_message(chat_id=query.message.chat_id, text=f"Your language has been set to {query.data}.")
    response = get_request(f"http://backend:{PORT}/api/converse/", {"client_id": f"tg:{client_id}"})
    await context.bot.send_message(chat_id=query.message.chat_id, text=response.get("reply"))
