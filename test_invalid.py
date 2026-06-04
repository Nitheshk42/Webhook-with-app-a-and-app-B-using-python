import requests
import json

def send_invalid_webhook():
    url = "https://webhook-with-app-a-and-app-b-using-python-production.up.railway.app/webhook"

    event = {
        "action": "user_input",
        "data": "im application 3"
    }

    response = requests.post(url, json=event, 
        headers={"X-Signature": "wrong_signature_12345"})

    print(f"Response: {response.status_code}")
    print(f"Message: {response.json()}")

send_invalid_webhook()