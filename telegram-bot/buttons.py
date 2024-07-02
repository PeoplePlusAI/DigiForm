from utils.reqs import post_request
from utils.env import PORT
from utils.io import read_file

upload_text = read_file('static/chat/upload.txt')

async def button(update, context):
    query = update.callback_query
    await query.answer()
    client_id = update.effective_user.id
    if query.data == "submit":
        response = post_request(f"http://backend:{PORT}/api/done/", {"client_id": f"tg:{client_id}"})
        await context.bot.send_message(chat_id=query.message.chat_id, text=read_file("static/chat/thanks.txt").replace('#####', response.get("time_taken")))
    elif query.data == "change":
        await context.bot.send_message(chat_id=query.message.chat_id, text=read_file("static/chat/change.txt"))
    else:
        _ = post_request(f"http://backend:{PORT}/api/update/", {"client_id": f"tg:{client_id}", "details": {"chat_preferred_language": query.data}})
        await context.bot.send_message(chat_id=query.message.chat_id, text=upload_text.replace("#####", query.data))
