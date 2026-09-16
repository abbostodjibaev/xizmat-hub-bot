XIZMAT HUB Telegram Bot

GitHub repositoryga ushbu 3 faylni yuklang:
- app.py
- requirements.txt
- README.txt

Render Web Service sozlamalari:
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app

Environment Variables:
BOT_TOKEN = BotFather bergan token (MAXFIY)
ADMIN_USERNAME = xizmat_hub

Muhim: BOT_TOKEN ni GitHub fayllariga yozmang.

Deploy bo'lgach Render sizga https://...onrender.com manzil beradi.
Webhook keyingi bosqichda shu manzil + /webhook ga ulanadi.

Saytdagi xizmat tugmalari keyin Telegram deep-link shaklida bo'ladi:
https://t.me/Xizmat_hub_bot?start=<service_code>
Masalan:
https://t.me/Xizmat_hub_bot?start=airport_job
