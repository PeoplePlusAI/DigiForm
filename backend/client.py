from openai import OpenAI
from groq import Groq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_groq import ChatGroq
from utils.env import OPENAI_API_KEY, OPENAI_CHAT_MODEL, GROQ_API_KEY, GROQ_CHAT_MODEL
from utils.io import read_file

if len(OPENAI_API_KEY):
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )
    model = OPENAI_CHAT_MODEL
else:
    client = Groq(
        api_key=GROQ_API_KEY
    )
    model = GROQ_CHAT_MODEL

def llm_response(prompt):
    completion = client.chat.completions.create(
        messages= [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model
    )
    return completion.choices[0].message.content.strip()

chat = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name=GROQ_CHAT_MODEL)

question_prompt = PromptTemplate(
    template=read_file("static/prompts/ask_question.txt"),
    input_variables=["field", "language"],
)
question = question_prompt | chat | StrOutputParser()

def generate_questions(form_data, user_language):
    questions = {}
    for field, value in form_data.items():
        try:
            if value is None:
                prompt_input = {"field": field, "language": user_language}
                response = question.invoke(prompt_input)
                questions[field] = response.strip()
        except:
            questions[field] = "Groq API Limit Reached. Please try again later."
            break
    return questions

parsing_prompt = PromptTemplate(
    template=read_file("static/prompts/process_response.txt"),
    input_variables=["message", "language"],
)
parsing = parsing_prompt | chat | JsonOutputParser()

def parse_message(message, user_language):
    prompt_input = {"message": message, "language": user_language}
    try:
        returned_dict = parsing.invoke(prompt_input)
    except Exception as e:
        print(f"Error while parsing message: {e}")
        return dict()
    return returned_dict
