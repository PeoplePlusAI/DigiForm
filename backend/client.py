from openai import OpenAI
from utils.env import OPENAI_API_KEY, CHAT_MODEL

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
        model=CHAT_MODEL
    )
    return completion.choices[0].message.content.strip()
