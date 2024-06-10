from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
import requests
import os
from dotenv import load_dotenv
load_dotenv()
PORT = os.environ.get('PORT')

phone_numbers = {}

def get_request(endpoint, data):
    response = requests.get(endpoint, json=data)
    return response.json()

async def contact(query, context):
    button = KeyboardButton(text="Share Phone Number", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], one_time_keyboard=True, resize_keyboard=True)
    await context.bot.send_message(chat_id=query.message.chat_id, text="Kindly provide your phone number", reply_markup=reply_markup)

async def handle_contact(update, context):
    contact = update.effective_message.contact
    if contact:
        phone_number = contact.phone_number
        user_id = update.effective_user.id
        phone_numbers[user_id] = phone_number
        data = {
            "phone_number": phone_number,
            "user_id": user_id
        }
        response = get_request(f"http://backend:{PORT}/api/check/", data)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Thank you for providing your phone number. Kindly provide your email address.")
