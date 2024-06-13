import requests

def get_request(endpoint, data):
    response = requests.get(endpoint, json=data)
    return response.json()

def post_request(endpoint, data):
    response = requests.post(endpoint, json=data)
    return response.json()
