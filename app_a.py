from flask import Flask, request
import hmac
import hashlib
import json

app = Flask(__name__)
SECRET = "my_secret_key_123"

@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Signature')
    payload = request.get_data()

    expected_sig = hmac.new(SECRET.encode(), payload, hashlib.sha256).hexdigest()

    if signature != expected_sig:
        print("Unauthorized - signature mismatch")
        return {"error": "Unauthorized"}, 401
        
    data = request.get_json()
    print(f"Webhook Received: {data}")
    return {"status": "received"}, 200

if __name__ == '__main__':
    app.run(port=3000, debug=True)