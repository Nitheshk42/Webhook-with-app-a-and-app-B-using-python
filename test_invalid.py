import requests
import json

def send_invalid_webhook():
    url = "http://localhost:3000/webhook"

    event = {
        "action": "user_input",
        "data": "im application 3"
    }

    response = requests.post(url, json=event, 
        headers={"X-Signature": "wrong_signature_12345"})

    print(f"Response: {response.status_code}")
    print(f"Message: {response.json()}")

send_invalid_webhook()