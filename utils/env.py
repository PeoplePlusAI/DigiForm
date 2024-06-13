import os
from dotenv import load_dotenv
load_dotenv()

PORT = int(os.environ.get('PORT'))
POSTGRES_PORT = int(os.environ.get('PGPORT'))
POSTGRES_USER = str(os.environ.get('POSTGRES_USER'))
POSTGRES_PASSWORD = str(os.environ.get('POSTGRES_PASSWORD'))
POSTGRES_DB = str(os.environ.get('POSTGRES_DB'))
OPENAI_API_KEY = str(os.environ.get('OPENAI_API_KEY'))
CHAT_MODEL = str(os.environ.get('CHAT_MODEL'))
DJANGO_SECRET_KEY = str(os.environ.get('DJANGO_SECRET_KEY'))
TELEGRAM_BOT_TOKEN = str(os.environ.get('TELEGRAM_BOT_TOKEN'))
