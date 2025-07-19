
import requests
import telebot

BOT_TOKEN = '7898409981:AAGbbwYLzQPRIXOZnpf6zCwPlA9Vcls9PtM'
OWNER_ID = 7932600874
bot = telebot.TeleBot(BOT_TOKEN)

NUMVERIFY_API_KEY = 'demo'  # Ganti dengan API asli jika tersedia

PLATFORMS = ["instagram.com", "twitter.com", "github.com", "tiktok.com", "facebook.com"]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id != OWNER_ID:
        return
    bot.reply_to(message, "👋 Selamat datang di *CYBER FLAY OSINT Bot v2*\nKetik /help untuk bantuan.", parse_mode="Markdown")

@bot.message_handler(commands=['help'])
def send_help(message):
    if message.from_user.id != OWNER_ID:
        return
    bot.reply_to(message, (
        "🧠 *Perintah OSINT:*\n"
        "/cariuser <username> - Cek username di platform\n"
        "/nomor <noHP> - Cek info nomor HP\n"
        "/ip <alamat_ip> - Info lokasi IP"
    ), parse_mode="Markdown")

@bot.message_handler(commands=['cariuser'])
def cari_user(message):
    if message.from_user.id != OWNER_ID:
        return
    try:
        username = message.text.split()[1]
        hasil = f"🔎 Username *{username}*:\n\n"
        for platform in PLATFORMS:
            url = f"https://{platform}/{username}"
            r = requests.get(url)
            status = "✅ Ada" if r.status_code == 200 else "❌ Tidak ditemukan"
            hasil += f"- {platform}: {status}\n"
        bot.reply_to(message, hasil, parse_mode="Markdown")
    except:
        bot.reply_to(message, "Contoh: /cariuser rafkacyber")

@bot.message_handler(commands=['ip'])
def ip_lookup(message):
    if message.from_user.id != OWNER_ID:
        return
    try:
        ip = message.text.split()[1]
        r = requests.get(f"http://ip-api.com/json/{ip}").json()
        if r['status'] == 'fail':
            bot.reply_to(message, "IP tidak ditemukan.")
            return
        text = (
            f"📡 IP: {ip}\nNegara: {r['country']}\nKota: {r['city']}\nISP: {r['isp']}\n"
            f"Koordinat: {r['lat']}, {r['lon']}"
        )
        bot.reply_to(message, text)
    except:
        bot.reply_to(message, "Contoh: /ip 103.xxx.xxx")

@bot.message_handler(commands=['nomor'])
def nomor_lookup(message):
    if message.from_user.id != OWNER_ID:
        return
    try:
        nomor = message.text.split()[1].replace('+', '')
        url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={nomor}"
        res = requests.get(url).json()
        if not res.get('valid'):
            bot.reply_to(message, "Nomor tidak valid atau tidak ditemukan.")
            return
        hasil = (
            f"📱 Nomor: +{res['country_code']}{res['national_format']}\n"
            f"Negara: {res['country_name']}\n"
            f"Lokasi: {res['location']}\n"
            f"Carrier: {res['carrier']}\n"
            f"Line Type: {res['line_type']}"
        )
        bot.reply_to(message, hasil)
    except:
        bot.reply_to(message, "Contoh: /nomor 628xxxxxx")

bot.polling()
