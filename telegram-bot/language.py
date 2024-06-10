from read import read_file
from contact import contact

contact_text = read_file('static/contact_details.txt')

async def language_button(update, context):
    query = update.callback_query
    await query.answer()
    choice = query.data
    await contact(query, context)
