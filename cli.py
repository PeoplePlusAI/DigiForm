import requests
import json

# URL of your Django application's endpoints
BASE_URL = "http://localhost:6001/api"  # Change this to your Docker container's URL
ENDPOINT1 = f"{BASE_URL}/start/"
ENDPOINT2 = f"{BASE_URL}/prompt/"

def post_request(endpoint, data):
    response = requests.post(endpoint, json=data)
    return response.json()

def get_request(endpoint, data):
    response = requests.get(endpoint, json=data)
    return response.json()

def main():
    print("DigiForm CLI\n============\n")

    phno = int(input("Phone Number: "))

    data = {
        "user_id": phno,
        "session_id": "cli_session"
    }
    response = get_request(ENDPOINT1, data)
    while True:
        print(f"Bot: {response['bot_reply']}")

        message = input("You: ")
        if message.lower() == 'exit':
            break

        data = {
            "message": message,
            "user_id": phno,
            "session_id": "cli_session"
        }

        response = post_request(ENDPOINT2, data)

if __name__ == "__main__":
    main()
