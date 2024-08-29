import re
import json
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from utils.env import GROQ_API_KEY, GROQ_CHAT_MODEL
from utils.io import read_file

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

def extract_json(S):
    json_match = re.search(r'\{.*\}', S, re.DOTALL)
    json_str = json_match.group(0)
    return json.loads(json_str)

parsing_prompt = PromptTemplate(
    template=read_file("static/prompts/process_response.txt"),
    input_variables=["message", "language"],
)
parsing = parsing_prompt | chat | StrOutputParser()

def parse_message(message, user_language):
    prompt_input = {"message": message, "language": user_language}
    try:
        returned_dict = extract_json(parsing.invoke(prompt_input))
    except Exception as e:
        print(f"Error while parsing message: {e}")
        return dict()
    return returned_dict

image_parsing_prompt = PromptTemplate(
    template=read_file("static/prompts/process_image.txt"),
    input_variables=["string", "language"],
)
image_parsing = image_parsing_prompt | chat | StrOutputParser()

def parse_image(string, user_language):
    prompt_input = {"string": string, "language": user_language}
    try:
        returned_dict = extract_json(image_parsing.invoke(prompt_input))
    except Exception as e:
        print(f"Error while parsing image: {e}")
        return dict()
    return returned_dict
