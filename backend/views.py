import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from .client import openai_response
from .models import User
import re

def clean_phone_number(phone_number):
    cleaned_number = re.sub(r'\D', '', phone_number)
    return int(cleaned_number)


@require_http_methods(["GET"])
def check(request):
    try:
        data = json.loads(request.body)

        phone_number = clean_phone_number(data.get('phone_number'))
        user_id = data.get('user_id')

        if not all([user_id, phone_number]):
            return HttpResponseBadRequest("Missing required fields")

        try:
            user = User.objects.filter(mobile=phone_number).get()
        except:
            user = User(mobile=phone_number)
            user.save()

        response_data = {
            'status': 'success'
        }
        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

@require_http_methods(["POST"])
def parse(request):
    try:
        data = json.loads(request.body)

        message = data.get('message')
        phone_number = clean_phone_number(data.get('phone_number'))
        user_id = data.get('user_id')

        if not all([message, user_id, phone_number]):
            return HttpResponseBadRequest("Missing required fields")

        user = User.objects.filter(mobile=phone_number).get()

        status = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "mobile": user.mobile,
            "email": user.email,
            "gender": user.gender,
            "marital_status": user.marital_status,
            "dob": user.dob,
        }

        if not all(status.values()):
            response = process_message(message, status)
            status = json.loads(response)

        user.first_name = status["first_name"]
        user.last_name = status["last_name"]
        user.mobile = status["mobile"]
        user.email = status["email"]
        user.gender = status["gender"]
        user.marital_status = status["marital_status"]
        user.dob = status["dob"]
        user.save()

        if all(status.values()):
            next_question = read_file("static/complete.txt").replace('#####', "\n".join([
                "First Name: " + str(user.first_name),
                "Last Name: " + str(user.last_name),
                "Mobile: " + str(user.mobile),
                "Email: " + str(user.email),
                "Gender: " + str(user.gender),
                "Marital Status: " + str(user.marital_status),
                "Date of Birth: " + str(user.dob)
            ]))
        else:
            next_question = next_message(status)

        response_data = {
            'reply': next_question,
            'status': 'success'
        }
        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

def read_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    return content

def get_started():
    return read_file("static/start.txt")

def process_message(message, status):
    prompt = read_file("static/construct.txt").replace('#####', str(status)) + str(message)
    return openai_response(prompt)

def next_message(status):
    prompt = read_file("static/ask_next.txt").replace('#####', str(status))
    return openai_response(prompt)
