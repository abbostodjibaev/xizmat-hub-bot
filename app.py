import os
import html
from flask import Flask, request
import requests

app = Flask(__name__)
TOKEN = os.environ.get('BOT_TOKEN', '')
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'xizmat_hub').lstrip('@')
BASE = f'https://api.telegram.org/bot{TOKEN}'


def send_message(chat_id, text, reply_markup=None):
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    if reply_markup:
        payload['reply_markup'] = reply_markup
    requests.post(f'{BASE}/sendMessage', json=payload, timeout=15)


@app.get('/')
def health():
    return 'XIZMAT HUB bot is running', 200


@app.post('/webhook')
def webhook():
    data = request.get_json(silent=True) or {}
    msg = data.get('message') or {}
    chat = msg.get('chat') or {}
    chat_id = chat.get('id')
    text = (msg.get('text') or '').strip()
    if not chat_id:
        return 'ok', 200

    service = None
    if text.startswith('/start'):
        parts = text.split(maxsplit=1)
        if len(parts) == 2:
            service = parts[1].replace('_', ' ').replace('-', ' ').strip()

    keyboard = {
        'inline_keyboard': [[
            {'text': '👤 Admin bilan bog‘lanish', 'url': f'https://t.me/{ADMIN_USERNAME}'}
        ]]
    }

    if service:
        safe = html.escape(service)
        reply = (
            '✅ <b>Buyurtmangiz qabul qilindi</b>\n\n'
            f'🛒 Tanlangan xizmat: <b>{safe}</b>\n\n'
            'Davom etish uchun quyidagi tugma orqali admin bilan bog‘laning.'
        )
    else:
        reply = (
            '👋 <b>XIZMAT HUB buyurtma botiga xush kelibsiz!</b>\n\n'
            'Xizmatni xizmithub.uz saytidan tanlang va “Buyurtma berish” tugmasini bosing.'
        )
    send_message(chat_id, reply, keyboard)
    return 'ok', 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '10000'))
    app.run(host='0.0.0.0', port=port)
