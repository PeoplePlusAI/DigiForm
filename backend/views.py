import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
import numpy as np
import cv2
import pytesseract
from PIL import Image
from .client import generate_questions, parse_message, parse_image
from .models import User
from utils.io import read_file
from utils.phone_number import normalize_phone_number
import datetime
from dateutil import parser

@require_http_methods(["GET"])
def details(request):
    try:
        data = json.loads(request.body)
        client_id = data.get('client_id')
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    if not all([client_id]):
        return HttpResponseBadRequest("Missing required fields")

    try:
        user = User.objects.filter(client_id=client_id).get()
    except:
        user = User(client_id=client_id)
        user.save()

    details_ = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "mobile": user.mobile,
        "email": user.email,
        "gender": user.gender,
        "marital_status": user.marital_status,
        "dob": user.dob,
    }

    response_data = {
        'details': details_,
        'complete': bool(all(details_.values())),
        'status': 'success'
    }
    return JsonResponse(response_data)

@require_http_methods(["POST"])
def clear(request):
    try:
        data = json.loads(request.body)
        client_id = data.get('client_id')
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    if not all([client_id]):
        return HttpResponseBadRequest("Missing required fields")

    try:
        user = User.objects.filter(client_id=client_id).get()
        user.delete()
        user = User(client_id=client_id)
        user.save()
    except:
        user = User(client_id=client_id)
        user.save()

    response_data = {
        'complete': False,
        'status': 'success'
    }
    return JsonResponse(response_data)

@require_http_methods(["POST"])
def done(request):
    try:
        data = json.loads(request.body)
        client_id = data.get('client_id')
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    if not all([client_id]):
        return HttpResponseBadRequest("Missing required fields")

    try:
        user = User.objects.filter(client_id=client_id).get()
    except:
        raise Exception("User not found")

    user.confirm_details = True

    try:
        user.save()
    except Exception as e:
        print(f"Unable to save user details: {e}")
        return JsonResponse({
            'details': {
                "first_name": str(user.first_name),
                "last_name": str(user.last_name),
                "mobile": str(user.mobile),
                "email": str(user.email),
                "gender": str(user.gender),
                "marital_status": str(user.marital_status),
                "dob": str(user.dob),
            },
            'complete': True,
            'status': 'failure'
        })

    timestart = str(user.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    timeend = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    timestart = parser.parse(timestart)
    timeend = parser.parse(timeend)

    diff = timeend - timestart
    total_seconds = int(diff.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    response_data = {
        'time_taken': f"{minutes} minutes {seconds} seconds",
        'complete': True,
        'status': 'success'
    }
    return JsonResponse(response_data)

@require_http_methods(["POST"])
def update(request):
    try:
        data = json.loads(request.body)
        details_ = data.get('details')
        client_id = data.get('client_id')
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    if not all([details_, client_id]):
        return HttpResponseBadRequest("Missing required fields")

    try:
        user = User.objects.filter(client_id=client_id).get()
    except:
        user = User(client_id=client_id)
        user.save()

    current = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "mobile": user.mobile,
        "email": user.email,
        "gender": user.gender,
        "marital_status": user.marital_status,
        "dob": user.dob,
        "chat_preferred_language": user.chat_preferred_language
    }

    try:
        for key in current:
            if details_.get(key):
                current[key] = details_[key]
    except Exception as e:
        print(f"Unable to match keys from user data: {e}")
        return JsonResponse({
            'details': {
                "first_name": str(user.first_name),
                "last_name": str(user.last_name),
                "mobile": str(user.mobile),
                "email": str(user.email),
                "gender": str(user.gender),
                "marital_status": str(user.marital_status),
                "dob": str(user.dob),
            },
            'complete': False,
            'status': 'failure'
        })

    user.first_name = current["first_name"]
    user.last_name = current["last_name"]
    user.mobile = normalize_phone_number(current["mobile"]) if current["mobile"] is not None else None
    user.email = current["email"]
    user.gender = current["gender"]
    user.marital_status = current["marital_status"]
    user.dob = current["dob"]
    user.chat_preferred_language = current["chat_preferred_language"]

    try:
        user.save()
    except Exception as e:
        print(f"Unable to save user details: {e}")
        return JsonResponse({
            'details': {
                "first_name": str(user.first_name),
                "last_name": str(user.last_name),
                "mobile": str(user.mobile),
                "email": str(user.email),
                "gender": str(user.gender),
                "marital_status": str(user.marital_status),
                "dob": str(user.dob),
            },
            'complete': False,
            'status': 'failure'
        })

    details_ = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "mobile": user.mobile,
        "email": user.email,
        "gender": user.gender,
        "marital_status": user.marital_status,
        "dob": user.dob,
        "chat_preferred_language": user.chat_preferred_language
    }

    response_data = {
        'details': details_,
        'complete': bool(all(details_.values())),
        'status': 'success'
    }
    return JsonResponse(response_data)

@require_http_methods(["POST"])
def process(request):
    try:
        data = json.loads(request.body)
        message = data.get('message')
        client_id = data.get('client_id')
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    if not all([message, client_id]):
        return HttpResponseBadRequest("Missing required fields")

    try:
        user = User.objects.filter(client_id=client_id).get()
    except:
        user = User(client_id=client_id)
        user.save()

    current = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "mobile": user.mobile,
        "email": user.email,
        "gender": user.gender,
        "marital_status": user.marital_status,
        "dob": user.dob,
    }

    try:
        update = parse_message(message, user.chat_preferred_language)
    except Exception as e:
        print(f"Unable to parse message: {e}")
        return JsonResponse({
            'details': {
                "first_name": str(user.first_name),
                "last_name": str(user.last_name),
                "mobile": str(user.mobile),
                "email": str(user.email),
                "gender": str(user.gender),
                "marital_status": str(user.marital_status),
                "dob": str(user.dob),
            },
            'complete': False,
            'status': 'failure'
        })

    try:
        for key in current.keys():
            if key in update.keys():
                current[key] = update[key]
    except Exception as e:
        print(f"Unable to match keys from LLM response: {e}")
        return JsonResponse({
            'details': {
                "first_name": str(user.first_name),
                "last_name": str(user.last_name),
                "mobile": str(user.mobile),
                "email": str(user.email),
                "gender": str(user.gender),
                "marital_status": str(user.marital_status),
                "dob": str(user.dob),
            },
            'complete': False,
            'status': 'failure'
        })

    user.first_name = current["first_name"]
    user.last_name = current["last_name"]
    user.mobile = normalize_phone_number(current["mobile"]) if current["mobile"] is not None else None
    user.email = current["email"]
    user.gender = current["gender"]
    user.marital_status = current["marital_status"]
    user.dob = current["dob"]

    try:
        user.save()
    except Exception as e:
        print(f"Unable to save user details: {e}")
        return JsonResponse({
            'details': {
                "first_name": str(user.first_name),
                "last_name": str(user.last_name),
                "mobile": str(user.mobile),
                "email": str(user.email),
                "gender": str(user.gender),
                "marital_status": str(user.marital_status),
                "dob": str(user.dob),
            },
            'complete': False,
            'status': 'failure'
        })

    details_ = {
        "first_name": str(user.first_name),
        "last_name": str(user.last_name),
        "mobile": str(user.mobile),
        "email": str(user.email),
        "gender": str(user.gender),
        "marital_status": str(user.marital_status),
        "dob": str(user.dob),
    }
    response_data = {
        'details': details_,
        'complete': bool(all(details_.values())),
        'status': 'success'
    }
    return JsonResponse(response_data)

@require_http_methods(["POST"])
def image(request):
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image uploaded'}, status=400)

    try:
        image_file = request.FILES['image']
        image_bytes = image_file.read()
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            return JsonResponse({'error': 'Failed to decode image'}, status=400)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        pil_img = Image.fromarray(thresh)
        string = pytesseract.image_to_string(pil_img)
    except Exception as e:
        print(f"Unable to process image: {e}")
        return JsonResponse({
            'details': {},
            'complete': False,
            'status': 'failure'
        })

    if 'client_id' not in request.FILES:
        return JsonResponse({'error': 'Missing client_id'}, status=400)
    client_id = request.FILES['client_id'].read().decode('utf-8')

    if not all([client_id]):
        return HttpResponseBadRequest("Missing required fields")

    try:
        user = User.objects.filter(client_id=client_id).get()
    except:
        user = User(client_id=client_id)
        user.save()

    current = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "mobile": user.mobile,
        "email": user.email,
        "gender": user.gender,
        "marital_status": user.marital_status,
        "dob": user.dob,
    }

    try:
        update = parse_image(string, user.chat_preferred_language)
    except Exception as e:
        print(f"LLM unable to parse image: {e}")
        return JsonResponse({
            'details': {
                "first_name": str(user.first_name),
                "last_name": str(user.last_name),
                "mobile": str(user.mobile),
                "email": str(user.email),
                "gender": str(user.gender),
                "marital_status": str(user.marital_status),
                "dob": str(user.dob),
            },
            'complete': False,
            'status': 'failure'
        })

    try:
        for key in current.keys():
            if key in update.keys():
                current[key] = update[key]

    except Exception as e:
        print(f"Unable to match keys from LLM response: {e}")
        return JsonResponse({
            'details': {
                "first_name": str(user.first_name),
                "last_name": str(user.last_name),
                "mobile": str(user.mobile),
                "email": str(user.email),
                "gender": str(user.gender),
                "marital_status": str(user.marital_status),
                "dob": str(user.dob),
            },
            'complete': False,
            'status': 'failure'
        })

    user.first_name = current["first_name"]
    user.last_name = current["last_name"]
    user.mobile = normalize_phone_number(current["mobile"]) if current["mobile"] is not None else None
    user.email = current["email"]
    user.gender = current["gender"]
    user.marital_status = current["marital_status"]
    user.dob = current["dob"]

    try:
        user.save()
    except Exception as e:
        print(f"Unable to save user details: {e}")
        return JsonResponse({
            'details': {
                "first_name": str(user.first_name),
                "last_name": str(user.last_name),
                "mobile": str(user.mobile),
                "email": str(user.email),
                "gender": str(user.gender),
                "marital_status": str(user.marital_status),
                "dob": str(user.dob),
            },
            'complete': False,
            'status': 'failure'
        })

    details_ = {
        "first_name": str(user.first_name),
        "last_name": str(user.last_name),
        "mobile": str(user.mobile),
        "email": str(user.email),
        "gender": str(user.gender),
        "marital_status": str(user.marital_status),
        "dob": str(user.dob),
    }
    response_data = {
        'details': details_,
        'complete': bool(all(details_.values())),
        'status': 'success'
    }
    return JsonResponse(response_data)

@require_http_methods(["GET"])
def converse(request):
    try:
        data = json.loads(request.body)
        client_id = data.get('client_id')
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    if not all([client_id]):
        return HttpResponseBadRequest("Missing required fields")

    try:
        user = User.objects.filter(client_id=client_id).get()
    except:
        user = User(client_id=client_id)
        user.save()

    details_ = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "mobile": user.mobile,
        "email": user.email,
        "gender": user.gender,
        "marital_status": user.marital_status,
        "dob": user.dob,
    }

    if all(details_.values()):
        reply = read_file("static/chat/table.txt").replace('#####', "\n".join([
            "First Name: " + str(user.first_name),
            "Last Name: " + str(user.last_name),
            "Mobile: " + str(user.mobile),
            "Email: " + str(user.email),
            "Gender: " + str(user.gender),
            "Marital Status: " + str(user.marital_status),
            "Date of Birth: " + str(user.dob)
        ]))
    else:
        missing_field = None
        for field in details_: 
            if not details_[field]:
                missing_field = field
                break
        try:
            questions = generate_questions({missing_field: None},user_language=user.chat_preferred_language)
        except Exception as e:
            print(f"Unable to generate question: {e}")
            return JsonResponse({
                'reply': read_file("static/chat/error.txt"),
                'status': 'failure'
            })
        reply = '\n'.join(list(questions.values()))

    response_data = {
        'reply': reply,
        'complete': bool(all(details_.values())),
        'status': 'success'
    }
    return JsonResponse(response_data)
