import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from .client import openai_response
from .models import User

@require_http_methods(["GET"])
def start(request):
    try:
        data = json.loads(request.body)

        user_id = data.get('user_id')
        session_id = data.get('session_id')

        if not all([user_id, session_id]):
            return HttpResponseBadRequest("Missing required fields")
        
        try:
            user = User.objects.filter(mobile=user_id).get()
        except:
            user = User(mobile=user_id)
            user.save()

        starter = get_started()

        response_data = {
            'bot_reply': starter,
            'context': None,
            'status': 'success'
        }
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

@require_http_methods(["POST"])
def prompt(request):
    try:
        data = json.loads(request.body)
        
        message = data.get('message')
        user_id = data.get('user_id')
        session_id = data.get('session_id')

        if not all([message, user_id, session_id]):
            return HttpResponseBadRequest("Missing required fields")
        
        user = User.objects.filter(mobile=user_id).get()

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
            next_question = "Thank you for providing the information. Your form is complete."
        else:
            next_question = next_message(status)

        response_data = {
            'bot_reply': next_question,
            'context': None,
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
