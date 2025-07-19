import telebot
import requests

# Ganti token & ID dengan milikmu
bot = telebot.TeleBot("7898409981:AAGbbwYLzQPRIXOZnpf6zCwPlA9Vcls9PtM")
admin_id = "7932600874"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🔍 Selamat datang di *TRACE-FLAY*\nKirim /help untuk melihat perintah.", parse_mode="Markdown")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    text = """
📌 *Perintah Tersedia*:
• /nomor <nomor> - Info nomor HP
• /ip <alamat_ip> - Info IP Address
• /cariuser <username> - Cek username (eksperimen)
"""
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['nomor'])
def nomor_handler(message):
    try:
        nomor = message.text.split()[1]
        res = requests.get(f"https://htmlweb.ru/geo/api.php?json&telcod={nomor}")
        data = res.json()
        if "country" in data:
            text = f"🌍 *Negara:* {data['country']['english']}\n🏙 *Wilayah:* {data['region']['english']}\n📱 *Operator:* {data['0']['oper']}"
        else:
            text = "❌ Gagal mengambil data. Pastikan format nomor benar."
    except:
        text = "⚠️ Gunakan format: /nomor 6281234567890"
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['ip'])
def ip_handler(message):
    try:
        ip = message.text.split()[1]
        res = requests.get(f"http://ip-api.com/json/{ip}")
        data = res.json()
        if data["status"] == "success":
            text = f"🌍 *Negara:* {data['country']}\n🏙 *Kota:* {data['city']}\n📶 *ISP:* {data['isp']}"
        else:
            text = "❌ IP tidak ditemukan atau tidak valid."
    except:
        text = "⚠️ Gunakan format: /ip 8.8.8.8"
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['cariuser'])
def cari_user(message):
    try:
        username = message.text.split()[1]
        text = f"🔍 Sedang mencari username: {username}...\n(Fitur ini belum sepenuhnya aktif)"
    except:
        text = "⚠️ Gunakan format: /cariuser username"
    bot.reply_to(message, text)

bot.send_message(admin_id, "🤖 TRACE-FLAY aktif.")
bot.polling()