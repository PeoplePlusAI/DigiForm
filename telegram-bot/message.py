from contact import phone_numbers, contact
import requests
import os
from dotenv import load_dotenv
load_dotenv()
PORT = os.environ.get('PORT')

def post_request(endpoint, data):
    response = requests.post(endpoint, json=data)
    return response.json()

async def message(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_message = update.message.text
    try:
        phone_number = phone_numbers[user_id]
        data = {
            "message": user_message,
            "phone_number": phone_number,
            "user_id": user_id
        }
        response = post_request(f"http://backend:{PORT}/api/parse/", data)
        reply = response.get('reply')
        await context.bot.send_message(chat_id=chat_id, text=reply)
    except KeyError:
        await contact(update, context)
