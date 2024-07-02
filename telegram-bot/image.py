from utils.env import PORT
from utils.reqs import get_request, post_image

async def handle_image(update, context):
    client_id = update.effective_user.id
    file_id = update.message.photo[-1].file_id
    new_file = await context.bot.get_file(file_id)
    image_data = await new_file.download_as_bytearray()
    _ = post_image(f"http://backend:{PORT}/api/image/", f"tg:{client_id}", image_data)
    response = get_request(f"http://backend:{PORT}/api/converse/", {"client_id": f"tg:{client_id}"})
    await context.bot.send_message(chat_id=update.message.chat_id, text=response.get("reply"))
