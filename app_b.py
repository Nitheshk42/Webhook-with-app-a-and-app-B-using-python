import requests
#import time

def send_webhook(event_data):
    url = "http://localhost:3000/webhook"
    response = requests.post(url, json=event_data)
  #  print(f"✅ Event #{event_data['event_id']} sent")
    print(f"Sent: {response.status_code}")


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