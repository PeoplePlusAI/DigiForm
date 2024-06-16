import os
from dotenv import load_dotenv
load_dotenv()

PORT = int(os.environ.get('PORT'))
POSTGRES_PORT = int(os.environ.get('PGPORT'))
POSTGRES_USER = str(os.environ.get('POSTGRES_USER'))
POSTGRES_PASSWORD = str(os.environ.get('POSTGRES_PASSWORD'))
POSTGRES_DB = str(os.environ.get('POSTGRES_DB'))
OPENAI_API_KEY = str(os.environ.get('OPENAI_API_KEY'))
OPENAI_CHAT_MODEL = str(os.environ.get('OPENAI_CHAT_MODEL'))
GROQ_API_KEY = str(os.environ.get('GROQ_API_KEY'))
GROQ_CHAT_MODEL = str(os.environ.get('GROQ_CHAT_MODEL'))
DJANGO_SECRET_KEY = str(os.environ.get('DJANGO_SECRET_KEY'))
TELEGRAM_BOT_TOKEN = str(os.environ.get('TELEGRAM_BOT_TOKEN'))
