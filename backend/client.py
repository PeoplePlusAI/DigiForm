import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL = os.environ.get('MODEL')

client = OpenAI(
    api_key=OPENAI_API_KEY
)

def openai_response(prompt):
    completion = client.chat.completions.create(
        messages= [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=MODEL
    )
    return completion.choices[0].message.content.strip()
