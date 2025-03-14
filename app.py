from flask import Flask, request, jsonify, Response
import requests, os
from models.chatbot_model import generate_response

app = Flask(__name__)

# Set environment variables or replace with actual values for testing
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "EAAJV6Piz604BO7YBYPUpZA7d5pdmkCb7YiVrKDXhyA3u3YZBgaJRyUdiFkCHbTfzZAKRwOVAjZBG1ZCH4qBo5hb8KqHfAGEgea9ianCj3n780bs5m5PTGG8unpIkETZCfFV6F9k44yAuWWcNfMzZCot2nyg1ge18KNxqcxXzEXtknVHmZBZAtvrFhES6xZAGrf9RdZByEtskkQG21qiHi5p2IKX7hog2hEpIOfnIRuSBGlprKMA")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "558395714031254")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "7890123456")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        hub_challenge = request.args.get("hub.challenge")

        if verify_token == VERIFY_TOKEN:
            return Response(hub_challenge, status=200, mimetype='text/plain')
        return "Invalid token", 403

    data = request.get_json()
    if not data:
        return "Invalid JSON", 400

    process_whatsapp_message(data)
    return jsonify({"status": "received"}), 200

def process_whatsapp_message(data):
    try:
        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        message_data = changes.get("value", {}).get("messages", [{}])[0]

        sender_id = message_data.get("from")
        user_msg = message_data.get("text", {}).get("body", "")

        if sender_id and user_msg:
            response = generate_response(user_msg)
            send_whatsapp_message(sender_id, response)
    except Exception as e:
        print(f"Error processing message: {e}")

def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
