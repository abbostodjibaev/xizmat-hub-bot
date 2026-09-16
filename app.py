import os
import html
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "xizmat_hub").lstrip("@")

BASE = f"https://api.telegram.org/bot{TOKEN}"
WEBHOOK_URL = "https://xizmat-hub-bot.onrender.com/webhook"


def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    requests.post(
        f"{BASE}/sendMessage",
        json=payload,
        timeout=15
    )


def setup_webhook():
    if not TOKEN:
        print("BOT_TOKEN topilmadi")
        return

    try:
        response = requests.post(
            f"{BASE}/setWebhook",
            json={"url": WEBHOOK_URL},
            timeout=15
        )

        print("Telegram webhook:", response.text)

    except Exception as e:
        print("Webhook xatosi:", e)


@app.get("/")
def health():
    return "XIZMAT HUB bot is running", 200


@app.post("/webhook")
def webhook():

    data = request.get_json(silent=True) or {}

    msg = data.get("message") or {}
    chat = msg.get("chat") or {}

    chat_id = chat.get("id")
    text = (msg.get("text") or "").strip()
if text == '/myid':
    send_message(chat_id, f'🆔 Sizning Chat ID: <code>{chat_id}</code>')
    return 'ok', 200
    if not chat_id:
        return "ok", 200

    service = None

    if text.startswith("/start"):
        parts = text.split(maxsplit=1)

        if len(parts) == 2:
            service = (
                parts[1]
                .replace("_", " ")
                .replace("-", " ")
                .strip()
            )

    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "👤 Admin bilan bog‘lanish",
                    "url": f"https://t.me/{ADMIN_USERNAME}"
                }
            ]
        ]
    }

    if service:

        safe_service = html.escape(service)

        reply = (
            "✅ <b>Buyurtmangiz qabul qilindi!</b>\n\n"
            f"🛒 Tanlangan xizmat: <b>{safe_service}</b>\n\n"
            "Buyurtmani davom ettirish uchun "
            "quyidagi tugma orqali admin bilan bog‘laning."
        )

    else:

        reply = (
            "👋 <b>XIZMAT HUB buyurtma botiga xush kelibsiz!</b>\n\n"
            "Kerakli xizmatni xizmathub.uz saytidan tanlang "
            "va “Buyurtma berish” tugmasini bosing."
        )

    send_message(chat_id, reply, keyboard)

    return "ok", 200


setup_webhook()


if __name__ == "__main__":

    port = int(os.environ.get("PORT", "10000"))

    app.run(
        host="0.0.0.0",
        port=port
    )
