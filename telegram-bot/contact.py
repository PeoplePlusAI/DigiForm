import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.env import PORT
from utils.reqs import get_request
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup

async def contact(query, context):
    button = KeyboardButton(text="Share Phone Number", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], one_time_keyboard=True, resize_keyboard=True)
    await context.bot.send_message(chat_id=query.message.chat_id, text="Kindly provide your phone number", reply_markup=reply_markup)

async def handle_contact(update, context):
    contact = update.effective_message.contact
    if contact:
        phone_number = contact.phone_number
        client_id = update.effective_user.id
        data = {
            "client_id": f"tg:{client_id}"
        }
        response = get_request(f"http://backend:{PORT}/api/details/", data)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Thank you for providing your phone number. Kindly provide your email address.")
