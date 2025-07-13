
from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__, template_folder='templates')

API_KEY = os.environ.get("API_KEY")  # Secret on Railway
MODEL = "mistralai/mistral-7b-instruct"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://railway.app",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": user_message}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        return jsonify({"response": bot_reply})
    else:
        return jsonify({"error": response.text}), 500

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
