from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

MAX_BOT_TOKEN = "ВАШ_ТОКЕН_MAX"
MAX_CHAT_ID = "ВАШ_CHAT_ID"
TWILIO_SID = "ВАШ_TWILIO_SID"
TWILIO_TOKEN = "ВАШ_TWILIO_TOKEN"
TWILIO_FROM = "whatsapp:+14155238886"
TWILIO_TO = "whatsapp:+7XXXXXXXXXX"

def send_max(msg):
    url = "https://platform-api.max.ru/v1/messages/send"
    headers = {"Authorization": f"Bearer {MAX_BOT_TOKEN}"}
    requests.post(url, headers=headers, json={"chat_id": MAX_CHAT_ID, "text": msg})

def send_whatsapp(msg):
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"
    requests.post(url, data={"From": TWILIO_FROM, "To": TWILIO_TO, "Body": msg}, auth=(TWILIO_SID, TWILIO_TOKEN))

def format_msg(data):
    signal = data.get("signal","?")
    ticker = data.get("ticker","?")
    price = data.get("price","?")
    score = data.get("score","?")
    emoji = "🟢 КУПИТЬ" if signal == "BUY" else "🔴 ПРОДАТЬ"
    return f"{emoji}\n📊 {ticker}\n💰 Цена: {price}\n⚡ Сила: {score}\n🕐 {datetime.now().strftime('%H:%M:%S')}"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    msg = format_msg(data)
    send_max(msg)
    send_whatsapp(msg)
    return jsonify({"status": "ok"}), 200

@app.route("/")
def home():
    return "Сервер работает! ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
