import requests
import hmac
import hashlib
import json
#import time

SECRET = "my_secret_key_123"

def send_webhook(event_data):
    url = "http://localhost:3000/webhook"

    payload = json.dumps(event_data)
    signature = hmac.new(
        SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    response = requests.post(url, json=event_data, headers={"X-Signature": signature})
  #  print(f"✅ Event #{event_data['event_id']} sent")
    print(f"Sent with signature: {response.status_code}")


if __name__ == '__main__':
    while True:
        user_input = input("Enter change (or 'quit'): ")
        if user_input.lower() == 'quit':
            break

        event = {
            "action" : "user_input",
            "data": user_input
        }
        send_webhook(event)

# counter = 1
# while True:
#     event = {"event_id": counter, "message": f"Change #{counter}"}
#     send_webhook(event)
#     counter += 1
#     time.sleep(5)