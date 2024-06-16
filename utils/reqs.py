import requests
import json

def get_request(endpoint, data):
    response = requests.get(endpoint, json=data)
    return response.json()

def post_request(endpoint, data):
    response = requests.post(endpoint, json=data)
    return response.json()

def get_image(filepath):
    response = requests.get(filepath)
    return response.content

def post_image(endpoint, client_id, image_data):
    files = {'client_id': client_id, 'image': image_data}
    response = requests.post(endpoint, files=files)
    return response.json()
