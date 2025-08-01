from flask import Flask, request
import requests

app = Flask(__name__)

BALE_TOKEN = '1130752224:9isXHEmSFu3E9cgwckgM6JOXTfVVAKBZzbrhJDLU'
OPENAI_API_KEY = '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'

def ask_gpt(text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": text}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if data.get("message") and data["message"].get("text"):
        user_text = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]
        reply = ask_gpt(user_text)
        requests.post(
            f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )
    return "ok"

@app.route("/status")
def status():
    return "✅ ربات فعال است"
