
import os
import html
from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "").strip()
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "xizmat_hub").lstrip("@")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "").strip()
WEBHOOK_URL = os.environ.get(
    "WEBHOOK_URL",
    "https://xizmat-hub-bot.onrender.com/webhook"
).strip()

BASE = f"https://api.telegram.org/bot{TOKEN}"
ASSETS_DIR = os.path.dirname(__file__)
SERVICES = {
    "resume": {
        "title": "Resume / CV tayyorlash",
        "photo": "a_clean_modern_advertising_poster_social_media_b.png",
        "price": "69 000 so‘m",
        "text": """<b>Resume / CV tayyorlash</b>

<b>Talab qilinadi:</b>
• Ism va familiya
• Telefon raqam
• Elektron pochta
• Yashash joyi
• Tug‘ilgan sana
• Qaysi lavozimga topshirishingiz
• Ta’lim ma’lumoti
• Ish tajribasi
• Oldingi ish joylari va lavozimlar
• Ishlagan davri
• Kasbiy ko‘nikmalar
• Kompyuter dasturlarini bilish darajasi
• Chet tillari va darajasi
• Sertifikat yoki kurslar bo‘lsa
• Haydovchilik guvohnomasi bo‘lsa
• Professional rasm
• Qo‘shimcha ma’lumotlar

Agar ish tajribasi bo‘lmasa ham Resume tayyorlash mumkin.

<b>Javob namunasi:</b>
1. F.I.Sh.: Aliyev Ali Alisher o‘g‘li
2. Telefon: +998 XX XXX XX XX
3. E-mail: example@gmail.com
4. Manzil: Toshkent shahri
5. Maqsadli lavozim: Sotuv menejeri
6. Ta’lim: Universitet, 2020–2024
7. Ish tajribasi: ABC Company — Sotuvchi, 2024–2025
8. Ko‘nikmalar: MS Office, mijozlar bilan ishlash
9. Tillar: O‘zbek — ona tili, Rus — B1, Ingliz — A2

<b>💳 To‘lov oldindan amalga oshiriladi.</b>"""
    },
    "icloud": {
        "title": "iCloud / Apple ID ochish",
        "photo": "a_clean_modern_advertising_poster_social_media_b.png",
        "price": "59 000 so‘m",
        "text": """<b>iCloud / Apple ID ochish</b>

<b>Nima uchun kerak?</b>
• App Store’dan ilovalar yuklash uchun
• O‘yinlarni yuklash va o‘ynash uchun
• Foto, video va fayllarni bulutli xotirada saqlash uchun
• iPhone’dagi ma’lumotlarni zaxiralash uchun

<b>Talab qilinadi:</b>
• Ism va familiya
• Telefon raqam
• Tug‘ilgan sana
• Elektron pochta

<b>🔐 Muhim:</b>
Xavfsizlik uchun iCloud uchun alohida yangi e-mail ochish tavsiya etiladi. Asosiy shaxsiy e-mail va uning parolini yubormagan ma’qul. Kerak bo‘lsa alohida e-mail ochib beramiz. Xizmat tugagach parollarni mijozning o‘zi almashtiradi.

<b>💳 To‘lov oldindan amalga oshiriladi.</b>"""
    },
    "online_form": {
        "title": "Onlayn forma yaratish",
        "photo": "a_polished_commercial_advertising_poster_graphic.png",
        "price": "69 000 so‘m",
        "text": """<b>Onlayn forma yaratish</b>

<b>Nima uchun kerak?</b>
Mijozlardan kerakli ma’lumotlarni tartibli yig‘ish uchun:
• Ism va familiya
• Telefon raqam
• Yashash joyi
• Elektron pochta
• Boshqa kerakli ma’lumotlar

Bundan tashqari:
• Konkurslar
• So‘rovnoma / opros
• Savol-javob
• Ro‘yxatdan o‘tish
• Buyurtma yoki murojaat yig‘ish

<b>Talab qilinadi:</b>
• Elektron pochta
• Shu elektron pochtaga kirish imkoniyati

<b>🔐 Muhim:</b>
Asosiy shaxsiy pochta o‘rniga alohida ishchi e-mail ishlatish tavsiya etiladi.

<b>💳 To‘lov oldindan amalga oshiriladi.</b>"""
    },
    "insurance": {
        "title": "Majburiy avto sug‘urta",
        "photo": "a_clean_graphic_advertisement_poster_design_squar.png",
        "price": "Xizmat haqi: 20 000 so‘m",
        "text": """<b>Majburiy avto sug‘urta</b>

<b>Talab qilinadi:</b>
• Texnik pasport
• Haydovchilik guvohnomasi
• Pasport yoki ID karta
• JShShIR
• Telefon raqam
• Cheklangan sug‘urta bo‘lsa — polisga kiritiladigan haydovchilarning guvohnomalari

<b>💳 To‘lov oldindan amalga oshiriladi.</b>"""
    },
    "job_application": {
        "title": "Online ishga ariza topshirish",
        "photo": "a_bold_commercial_advertisement_poster_social_me.png",
        "price": "79 000 so‘m",
        "text": """<b>Online ishga ariza topshirish</b>

<b>Mahalliy ishlar:</b>
• Navoiy kon-metallurgiya kombinati
• Olmaliq kon-metallurgiya kombinati (OTMK)
• Boshqa mahalliy korxona va vakansiyalar

Mijoz kerakli ish joyini aytadi, biz online anketa/arizani to‘ldirib topshirib beramiz.

<b>Xorijiy ishlar:</b>
Mijoz avval admin bilan bog‘lanadi. Qaysi davlat va qaysi ish ekaniga qarab talablar aniqlanadi va ariza online topshiriladi.

<b>Talab qilinadi:</b>
• Ism familiya
• Telefon raqam
• Elektron pochta
• Tug‘ilgan sana
• Yashash manzili
• Ta’lim ma’lumoti
• Ish tajribasi
• Resume / CV bo‘lsa
• Pasport yoki ID ma’lumotlari, kerak bo‘lsa

<b>Muhim:</b> ishga qabul qilish bo‘yicha yakuniy qarorni ish beruvchi qabul qiladi.

<b>💳 To‘lov oldindan amalga oshiriladi.</b>"""
    },
    "airport_job": {
        "title": "Aeroportga ishga ariza",
        "photo": "a_polished_promotional_graphic_design_social_med.png",
        "price": "79 000 so‘m",
        "text": """<b>Aeroportga ishga ariza</b>

<b>Avvalo kerak bo‘ladi:</b>
• Ariza uchun alohida yangi e-mail
• Shu e-mail uchun parol
• Telefon raqam

<b>🔐 Muhim:</b>
Asosiy shaxsiy e-mailingizni bermang. Ariza uchun alohida e-mail ochish tavsiya etiladi. Bizga boshqa shaxsiy akkauntlaringiz ma’lumotlari kerak emas. Xizmat uchun olingan ma’lumotlar boshqa maqsadda ishlatilmaydi.

<b>Anketadagi savollar va javob namunasi:</b>
• Fuqaroligi — O‘zbekiston
• Tug‘ilgan joyi — Toshkent shahri
• Millati — O‘zbek
• Yashash manzili — Toshkent viloyati, ...
• Telefon raqam — +998 XX XXX XX XX
• Jinsi — Erkak / Ayol
• Tug‘ilgan sana — 27.10.2001
• Joriy oylik maosh — masalan, 6 000 000 so‘m
• Kutilayotgan oylik maosh — masalan, 10 000 000 so‘m
• Partiyaga a’zolik — tegishli variant / a’zo emas
• Ilmiy daraja — Yo‘q / mavjud bo‘lsa ko‘rsatiladi
• Ilmiy unvon — Yo‘q / mavjud bo‘lsa ko‘rsatiladi
• Oilaviy holat — Bo‘ydoq / Oilali
• Xizmat safariga munosabat — Ijobiy / roziman
• Haydovchilik guvohnomasi — Yo‘q yoki B, C va hokazo
• Smenali ishga munosabat — Roziman
• Bo‘yi — 174 sm
• Og‘irligi — 79 kg
• Harbiy xizmat — xizmat qilgan / qilmagan / zaxirada
• Qo‘shimcha ma’lumot — o‘zi haqida qisqa ma’lumot
• Ish tajribasi — tashkilot, lavozim, ishlagan davri
• Ta’lim — o‘quv muassasasi, mamlakat, yillar, daraja
• Chet tillari — masalan, Rus tili — A1

<b>💳 To‘lov oldindan amalga oshiriladi.</b>"""
    },
    "presentation": {
        "title": "Prezentatsiya tayyorlash",
        "photo": "a_polished_modern_promotional_poster_ad_layout_in.png",
        "price": "59 000 so‘mdan",
        "text": """<b>Prezentatsiya tayyorlash</b>

Ishda, o‘qishda yoki taqdimot uchun matn, rasm va infografikalar asosida professional prezentatsiya tayyorlanadi.

<b>Talab qilinadi:</b>
• Taqdimot mavzusi
• Necha slayd kerakligi
• Kerakli matn yoki asosiy ma’lumotlar
• Rasm / logo bo‘lsa
• Til: o‘zbek / rus / ingliz

<b>Natija:</b>
• PowerPoint formatida
• PDF formatida

<b>💳 To‘lov oldindan amalga oshiriladi.</b>"""
    },
    "vinetka": {
        "title": "Vinetka tayyorlash",
        "photo": "a_clean_modern_commercial_graphic_ad_poster_flye.png",
        "price": "199 000 so‘mdan",
        "text": """<b>Vinetka tayyorlash</b>

Mijoz rasmlarni yuboradi, biz ularni Photoshop’da sayqalab, professional dizayn qilamiz, qog‘ozga chop etib, vinetka kitobiga joylashtirib tayyor holatda topshiramiz.

<b>Talab qilinadi:</b>
• O‘quvchi / bitiruvchilar rasmlari
• Ism-familiyalar
• Sinf / guruh nomi
• Maktab / litsey / kollej / universitet nomi
• Dizayn bo‘yicha istaklar
• Vinetka turi
• Yetkazib berish manzili

<b>Muhim:</b>
• Yetkazib berish mavjud
• Dostavka puli mijoz tomonidan to‘lanadi
• Tayyorlanish muddati: 5–10 kun

<b>💳 To‘lov oldindan amalga oshiriladi.</b>"""
    },
    "invitation_certificate": {
        "title": "Online taklifnoma + sertifikat/diplom dizayni",
        "photo": "a_clean_high_contrast_promotional_graphic_poster.png",
        "price": "79 000 so‘mdan",
        "text": """<b>Online taklifnoma + sertifikat/diplom dizayni</b>

<b>Nima qilinadi?</b>
• Online taklifnoma dizayni
• Kurs, seminar, tadbir yoki tanlov uchun sertifikat dizayni
• Dekorativ diplom dizayni

<b>Talab qilinadi:</b>
• Tadbir yoki sertifikat nomi
• Kim uchun
• Tashkilot / loyiha nomi
• Sana
• Kerakli matn
• Logo bo‘lsa
• Imzo joyi bo‘lsa
• Rang va dizayn bo‘yicha istak

<b>Muhim:</b>
Faqat qonuniy, dekorativ yoki tadbir uchun dizayn tayyorlanadi. Rasmiy davlat hujjatlarini qalbakilashtirish xizmatiga kirmaydi.

<b>💳 To‘lov oldindan amalga oshiriladi.</b>"""
    },
    "trademark": {
        "title": "Brendni patentlash / tovar belgisini ro‘yxatdan o‘tkazish",
        "photo": "a_sleek_high_contrast_promotional_poster_advertis.png",
        "price": "999 000 so‘mdan",
        "text": """<b>Brendni patentlash / tovar belgisini ro‘yxatdan o‘tkazish</b>

<b>Nima qilinadi?</b>
• Brend nomi tekshiriladi
• O‘xshash yoki aynan bir xil ro‘yxatdan o‘tgan brend bor-yo‘qligi ko‘rib chiqiladi
• Logo va nom bo‘yicha ariza tayyorlanadi
• Tovar/xizmat sinfi aniqlanadi
• Ariza topshirishga yordam beriladi

<b>Talab qilinadi:</b>
• OneID yoki elektron kalit
• Brend nomi
• Logo
• Logo ranglari
• Brend qaysi mahsulot yoki xizmat uchun ishlatilishi
• F.I.Sh. yoki tashkilot ma’lumotlari
• Telefon raqam
• Elektron pochta
• Manzil

<b>Muhim:</b>
Dastlabki tekshiruv o‘tkaziladi, ammo yakuniy ro‘yxatdan o‘tkazish qarorini vakolatli davlat organi beradi.
Davlat bojlari alohida to‘lanadi.

<b>💳 To‘lov oldindan amalga oshiriladi.</b>"""
    },
    "maps": {
        "title": "Google Xarita / Yandex Xarita",
        "photo": "a_glossy_high_contrast_advertising_poster_flyer_i.png",
        "price": "Google: 399 000 so‘m | Yandex: 599 000 so‘m",
        "text": """<b>Google Xarita / Yandex Xarita’ga biznes joylash</b>

<b>Nima uchun kerak?</b>
• Biznesingiz xaritada ko‘rinadi
• Mijozlar nom bo‘yicha topa oladi
• Manzil, telefon va ish vaqtlarini ko‘radi
• Yandex Go va boshqa xarita servislaridan joylashuvni topish osonlashadi
• Telegram’da har safar lokatsiya yuborish shart bo‘lmaydi

<b>Talab qilinadi:</b>
• Biznes nomi
• Biznes elektron pochtasi
• Shu e-mailga kirish imkoniyati
• Telefon raqam
• Aniq manzil yoki koordinata
• Ish vaqtlari
• Biznes haqida qisqa ma’lumot
• Faoliyat turi / kategoriya
• Logo
• Biznes joyining rasmlari bo‘lsa

<b>Muhim:</b>
Google yoki Yandex tomonidan tekshiruv/moderatsiya bo‘lishi mumkin. Yakuniy tasdiq platforma qoidalariga bog‘liq.

<b>💳 To‘lov oldindan amalga oshiriladi.</b>"""
    },
    "website_bot": {
        "title": "Sayt yaratish + Telegram bot",
        "photo": "a_polished_dark_themed_marketing_poster_banner_i.png",
        "price": "Vazifaga qarab",
        "text": """<b>Sayt yaratish + Telegram bot</b>

<b>Nima qilinadi?</b>
• Mijoz xohishiga ko‘ra sayt yaratiladi
• Telegram bot yaratiladi
• Sayt va bot bir-biriga ulanadi
• Kerak bo‘lsa buyurtma qabul qilish tizimi qo‘shiladi
• Dizayn va funksiyalar biznesga moslashtiriladi

<b>Talab qilinadi:</b>
• Biznes nomi
• Logo bo‘lsa
• Xizmatlar yoki mahsulotlar
• Saytda kerakli bo‘limlar
• Bot qanday vazifani bajarishi
• Telefon raqam
• Telegram username
• Instagram yoki boshqa ijtimoiy tarmoq havolalari
• Dizayn bo‘yicha istaklar

<b>Narx:</b> vazifa hajmi va murakkabligiga qarab belgilanadi.

<b>💳 To‘lov oldindan yoki kelishilgan tartibda amalga oshiriladi.</b>"""
    },
    "target": {
        "title": "Professional Target reklama",
        "photo": "a_dark_glossy_professional_marketing_ad_poster_i.png",
        "price": "Maqsad va hajmga qarab",
        "text": """<b>Professional Target reklama</b>

<b>Nima uchun kerak?</b>
• Mijozlar oqimini ko‘paytirish
• Savdoni oshirish
• Reklamani kerakli auditoriyaga ko‘rsatish
• Lead generation orqali potensial mijoz kontaktlarini yig‘ish

<b>Talab qilinadi:</b>
• Biznes / xizmat haqida ma’lumot
• Instagram / Facebook sahifa
• Reklama qilinadigan mahsulot yoki xizmat
• Maqsadli auditoriya
• Rasm/video/materiallar bo‘lsa
• Telefon raqam yoki kontakt
• Reklama maqsadi

Batafsil hamkorlik Abbos Todjibaev bilan uchrashib, shartnoma asosida amalga oshirilishi mumkin.

<b>Muhim:</b>
Meta reklama budjeti xizmat haqidan alohida to‘lanadi. Natija bozor, taklif, budjet va auditoriyaga bog‘liq.

<b>💳 To‘lov oldindan yoki shartnoma bo‘yicha.</b>"""
    },
    "search_ads": {
        "title": "Google Search + Yandex qidiruv reklamasi",
        "photo": "a_high_contrast_professional_digital_advertisemen.png",
        "price": "Vazifa va budjetga qarab",
        "text": """<b>Google Search + Yandex qidiruv reklamasi</b>

<b>Nima uchun kerak?</b>
• Mijozlar biznesingizni Google yoki Yandex orqali o‘zlari qidirib topadi
• Reklama aynan kerakli xizmatni qidirayotgan odamlarga ko‘rsatiladi
• Sayt, telefon yoki boshqa aloqa kanaliga murojaatlar kelishi mumkin

<b>Talab qilinadi:</b>
• Biznes / xizmat haqida ma’lumot
• Sayt bo‘lsa — sayt manzili
• Telefon raqam
• Reklama qilinadigan xizmatlar
• Reklama hududi
• Reklama budjeti

Reklama Abbos Todjibaev bilan shartnoma asosida yoqib beriladi.

<b>Muhim:</b>
Google/Yandex reklama budjeti xizmat haqidan alohida to‘lanadi. Natija budjet, raqobat va xizmat turiga bog‘liq.

<b>💳 To‘lov oldindan yoki shartnoma bo‘yicha.</b>"""
    },
    "virtual_number": {
        "title": "Virtual raqamlar",
        "photo": "a_polished_high_contrast_promotional_graphic_post.png",
        "price": "Davlat va raqam turiga qarab",
        "text": """<b>Virtual raqamlar</b>

<b>Mavjud:</b>
• AQSH
• Kanada
• Buyuk Britaniya
• 20+ davlat virtual raqamlari

<b>Talab qilinadi:</b>
• Qaysi davlat raqami kerakligi
• Qaysi platforma uchun ishlatilishi
• Kerak bo‘lsa foydalanish muddati

<b>Muhim:</b>
Har bir platforma virtual raqamlarni qabul qilish qoidalarini o‘zi belgilaydi. Ayrim servislar barcha virtual raqamlarni qabul qilmasligi mumkin.

<b>💳 To‘lov oldindan amalga oshiriladi.</b>"""
    },
    "hhuz": {
        "title": "HH.UZ profil / anketa",
        "photo": "a_polished_commercial_infographic_ad_banner_with_a.png",
        "price": "49 000 so‘m",
        "text": """<b>HH.UZ profil / anketa</b>

HH.UZ orqali O‘zbekistondagi va ayrim MDH/SNG davlatlaridagi vakansiyalarga ariza topshirish mumkin.

<b>Talab qilinadi:</b>
• Ism va familiya
• Telefon raqam
• Elektron pochta
• Tug‘ilgan sana
• Yashash shahri / manzili
• Qaysi lavozimga ish qidirayotgani
• Kutilayotgan oylik maosh
• Oldingi ish joylari
• Lavozimlar va ishlagan davri
• Ish tajribasi va vazifalari
• Ta’lim muassasasi
• Mutaxassislik
• O‘qigan yillari
• Kasbiy ko‘nikmalar
• Chet tillari va darajasi
• Kurs / sertifikatlar bo‘lsa
• Resume uchun rasm bo‘lsa
• Ko‘chib ishlashga tayyormi
• Xizmat safariga munosabati
• Qaysi davlat yoki shaharlarda ishlashga tayyorligi

<b>Muhim:</b>
Profil va arizani tayyorlab beramiz, lekin ishga qabul qilish bo‘yicha yakuniy qarorni ish beruvchi qabul qiladi.

<b>💳 To‘lov oldindan amalga oshiriladi.</b>"""
    },
    "logo_design": {
        "title": "Logo va grafik dizayn",
        "photo": "a_clean_modern_promotional_poster_ad_layout_g.png",
        "price": "Vazifaga qarab",
        "text": """<b>Logo va grafik dizayn xizmati</b>

<b>Nima qilinadi?</b>
• Logo dizayni
• Instagram post va posterlar
• YouTube banner / shapka
• Reklama bannerlari
• Ish topshirish uchun dizaynlar
• Vizitka, flayer va boshqa grafik materiallar
• Biznes uchun turli grafik ishlar

<b>Talab qilinadi:</b>
• Biznes yoki loyiha nomi
• Qanday dizayn kerakligi
• Matnlar
• Logo bo‘lsa
• Ranglar bo‘yicha istak
• O‘lcham / platforma
• Namuna / reference bo‘lsa

<b>Narx:</b> vazifaning turi, hajmi va murakkabligiga qarab belgilanadi.

<b>💳 To‘lov oldindan amalga oshiriladi.</b>"""
    },
}

ALIASES = {
    "cv": "resume",
    "resume_cv": "resume",
    "apple_icloud": "icloud",
    "form": "online_form",
    "auto_insurance": "insurance",
    "sugurta": "insurance",
    "application": "job_application",
    "online_job": "job_application",
    "airport": "airport_job",
    "airport_application": "airport_job",
    "prezentatsiya": "presentation",
    "yearbook": "vinetka",
    "certificate": "invitation_certificate",
    "invitation": "invitation_certificate",
    "brand": "trademark",
    "patent": "trademark",
    "google_yandex_maps": "maps",
    "google_maps": "maps",
    "yandex_maps": "maps",
    "site_bot": "website_bot",
    "telegram_bot": "website_bot",
    "professional_target": "target",
    "google_yandex_ads": "search_ads",
    "google_search": "search_ads",
    "virtual": "virtual_number",
    "hh": "hhuz",
    "hh_uz": "hhuz",
    "design": "logo_design",
    "logo": "logo_design",
}

def api_post(method, payload):
    try:
        r = requests.post(f"{BASE}/{method}", json=payload, timeout=20)
        print(method, r.status_code, r.text[:500])
        return r
    except Exception as e:
        print(method, "ERROR:", e)
        return None

def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return api_post("sendMessage", payload)

def send_photo(chat_id, photo_name):
    photo_path = os.path.join(ASSETS_DIR, photo_name)
    if not os.path.exists(photo_path):
        print("PHOTO FILE NOT FOUND:", photo_path)
        return None
    try:
        with open(photo_path, "rb") as photo_file:
            r = requests.post(
                f"{BASE}/sendPhoto",
                data={"chat_id": chat_id},
                files={"photo": photo_file},
                timeout=30,
            )
        print("sendPhoto", r.status_code, r.text[:500])
        return r
    except Exception as e:
        print("sendPhoto ERROR:", e)
        return None

def admin_keyboard():
    return {
        "inline_keyboard": [[
            {"text": "👤 Admin bilan bog‘lanish", "url": f"https://t.me/{ADMIN_USERNAME}"}
        ]]
    }

def normalize_service(raw):
    if not raw:
        return None
    slug = raw.strip().lower().replace(" ", "_").replace("-", "_")
    slug = ALIASES.get(slug, slug)
    return slug if slug in SERVICES else None

def notify_admin(msg, service):
    if not ADMIN_CHAT_ID or not service:
        return
    user = msg.get("from") or {}
    user_id = user.get("id")
    username = user.get("username")
    full_name = ((user.get("first_name") or "") + " " + (user.get("last_name") or "")).strip() or "Mijoz"
    contact = f"@{html.escape(username)}" if username else f'<a href="tg://user?id={user_id}">{html.escape(full_name)}</a>'
    s = SERVICES[service]
    text = (
        "🆕 <b>Yangi buyurtma!</b>\n\n"
        f"🛒 Xizmat: <b>{html.escape(s['title'])}</b>\n"
        f"👤 Mijoz: {contact}\n"
        f"🆔 Telegram ID: <code>{user_id}</code>"
    )
    send_message(ADMIN_CHAT_ID, text)

def send_service(chat_id, service):
    s = SERVICES[service]
    send_photo(chat_id, s["photo"])
    text = f"{s['text']}\n\n<b>💰 Narx: {html.escape(s['price'])}</b>"
    send_message(chat_id, text, admin_keyboard())

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

    if not chat_id:
        return "ok", 200

    if text == "/myid":
        send_message(chat_id, f"Sizning Telegram chat ID: <code>{chat_id}</code>")
        return "ok", 200

    if text.startswith("/start"):
        parts = text.split(maxsplit=1)
        service = normalize_service(parts[1]) if len(parts) == 2 else None
        if service:
            notify_admin(msg, service)
            send_service(chat_id, service)
        else:
            send_message(
                chat_id,
                "👋 <b>XIZMAT HUB buyurtma botiga xush kelibsiz!</b>\n\n"
                "Kerakli xizmatni <b>xizmithub.uz</b> saytidan tanlang va "
                "“Buyurtma berish” tugmasini bosing.",
                admin_keyboard(),
            )
        return "ok", 200

    send_message(
        chat_id,
        "Kerakli xizmatni <b>xizmithub.uz</b> saytidan tanlab, "
        "“Buyurtma berish” tugmasini bosing.",
        admin_keyboard(),
    )
    return "ok", 200

def setup_webhook():
    if not TOKEN:
        print("BOT_TOKEN topilmadi")
        return
    try:
        r = requests.post(f"{BASE}/setWebhook", json={"url": WEBHOOK_URL}, timeout=20)
        print("Telegram webhook:", r.text)
    except Exception as e:
        print("Webhook xatosi:", e)

setup_webhook()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
