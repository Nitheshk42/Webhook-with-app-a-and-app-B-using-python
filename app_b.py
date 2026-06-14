import requests
import hmac
import hashlib
import json
from circuit_breaker import CircuitBreaker

# Create circuit breaker instance
cb = CircuitBreaker(failure_threshold=5, timeout=10)

SECRET = "my_secret_key_123"

def send_webhook(event_data):
    url = "https://webhook-with-app-a-and-app-b-using-python-production.up.railway.app/webhook"

    payload = json.dumps(event_data)
    signature = hmac.new(
        SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    response = requests.post(url, json=event_data, headers={"X-Signature": signature})
  #  print(f"✅ Event #{event_data['event_id']} sent")
    print(f"📤 Payload: {payload}")
    print(f"🔐 Signature: {signature}")
    print(f"Sent with signature: {response.status_code}")


def send_webhook_local(event_data):
    url = "http://localhost:3333/webhook"

    # Check if circuit allows request
    if not cb.can_execute():
        print(f"🚫 CIRCUIT OPEN - Request rejected! State: {cb.get_state().value}")
        return

    payload = json.dumps(event_data)
    signature = hmac.new(
        SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    try:
        response = requests.post(url, json=event_data, headers={"X-Signature": signature}, timeout=5)
        print(f"📤 Payload: {payload}")
        print(f"🔐 Signature: {signature}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            cb.record_success()
        else:
            cb.record_failure()
    except Exception as e:
        print(f"❌ Error: {e}")
        cb.record_failure()

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
        send_webhook_local(event)
