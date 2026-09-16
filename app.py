import os
import html
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "xizmat_hub").lstrip("@")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "").strip()

BASE = f"https://api.telegram.org/bot{TOKEN}"
WEBHOOK_URL = "https://xizmat-hub-bot.onrender.com/webhook"


# Saytdan keladigan xizmat kodlari -> chiroyli nomlar
SERVICES = {
    "resume_cv": "Resume / CV",
    "icloud": "Apple / iCloud akkaunt",
    "online_form": "Onlayn forma yaratish",
    "insurance": "Majburiy avto sug‘urta",
    "account_recovery": "Akkauntga kirishni tiklash",
    "job_application": "Ishga ariza topshirish",
    "airport_job": "Aeroportga ishga ariza",
    "presentation": "Prezentatsiya tayyorlash",
    "vinetka": "Vinetka / yilnoma",
    "certificate": "Diplom / sertifikat dizayni",
    "invitation": "Onlayn taklifnoma / sertifikat",
    "trademark": "Brendni patentlash",
    "maps": "Google / Yandex Maps",
    "website_bot": "Sayt + Telegram bot",
    "target": "Professional Target",
    "search_ads": "Google / Yandex reklama",
    "virtual_number": "AQSH virtual raqami",
    "hhuz": "HH.UZ profil / anketa",
    "logo_design": "Logo va grafik dizayn"
}


def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        response = requests.post(
            f"{BASE}/sendMessage",
            json=payload,
            timeout=15
        )
        return response.json()
    except Exception as e:
        print("Xabar yuborish xatosi:", e)
        return None


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
    user = msg.get("from") or {}

    chat_id = chat.get("id")
    text = (msg.get("text") or "").strip()

    if not chat_id:
        return "ok", 200

    # Chat ID ni ko‘rish
    if text == "/myid":
        send_message(
            chat_id,
            f"🆔 Sizning Chat ID: <code>{chat_id}</code>"
        )
        return "ok", 200

    service_slug = None

    if text.startswith("/start"):
        parts = text.split(maxsplit=1)

        if len(parts) == 2:
            service_slug = parts[1].strip()

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

    if service_slug:
        service_name = SERVICES.get(
            service_slug,
            service_slug.replace("_", " ").replace("-", " ").title()
        )

        safe_service = html.escape(service_name)

        # Mijozga javob
        reply = (
            "✅ <b>Buyurtmangiz qabul qilindi!</b>\n\n"
            f"🛒 Tanlangan xizmat: <b>{safe_service}</b>\n\n"
            "Buyurtmani davom ettirish uchun quyidagi "
            "tugma orqali admin bilan bog‘laning."
        )

        send_message(chat_id, reply, keyboard)

        # Admin uchun mijoz ma'lumotlari
        first_name = user.get("first_name", "")
        last_name = user.get("last_name", "")
        username = user.get("username", "")
        user_id = user.get("id", "")

        full_name = f"{first_name} {last_name}".strip()
        safe_name = html.escape(full_name or "Mijoz")

        if username:
            customer = f"@{html.escape(username)}"
        else:
            customer = (
                f'<a href="tg://user?id={user_id}">'
                f'{safe_name}</a>'
            )

        # Adminga avtomatik xabar
        if ADMIN_CHAT_ID:
            admin_message = (
                "🆕 <b>Yangi buyurtma!</b>\n\n"
                f"🛒 Xizmat: <b>{safe_service}</b>\n"
                f"👤 Mijoz: {customer}\n"
                f"🆔 Telegram ID: <code>{user_id}</code>"
            )

            send_message(ADMIN_CHAT_ID, admin_message)

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
    app.run(host="0.0.0.0", port=port)
