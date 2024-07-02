from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.env import PORT
from utils.reqs import post_request, get_request
from utils.io import read_file

async def handle_message(update, context):
    client_id = update.effective_user.id
    user_message = update.message.text
    data = {
        "message": user_message,
        "client_id": f"tg:{client_id}"
    }
    _ = post_request(f"http://backend:{PORT}/api/process/", data)
    response = get_request(f"http://backend:{PORT}/api/converse/", {"client_id": f"tg:{client_id}"})
    await context.bot.send_message(chat_id=update.message.chat_id, text=response.get("reply"))
    if response.get("complete"):
        choices = [
            [InlineKeyboardButton("Submit", callback_data="submit")],
            [InlineKeyboardButton("Make Changes", callback_data="change")]
        ]
        reply_markup = InlineKeyboardMarkup(choices)
        await context.bot.send_message(chat_id=update.message.chat_id, text=read_file("static/chat/confirm.txt"), reply_markup=reply_markup)
