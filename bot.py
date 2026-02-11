import os
import sqlite3
import threading
from telebot import TeleBot
from flask import Flask

# Ambil Token dari settingan server nanti
TOKEN = os.getenv('BOT_TOKEN')
bot = TeleBot(TOKEN)
server = Flask(__name__)

# Fungsi buat database
def init_db():
    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS my_files 
                 (file_id TEXT, file_type TEXT, caption TEXT)''')
    conn.commit()
    conn.close()

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Kirim file dengan caption sebagai kata kunci untuk menyimpan.")

# Simpan file yang dikirim
@bot.message_handler(content_types=['document', 'photo', 'video', 'audio'])
def handle_file(message):
    if not message.caption:
        bot.reply_to(message, "❌ Gagal! Berikan caption pada file sebagai kata kunci.")
        return
    
    # Ambil ID file unik dari Telegram
    if message.content_type == 'photo': file_id = message.photo[-1].file_id
    elif message.content_type == 'video': file_id = message.video.file_id
    elif message.content_type == 'document': file_id = message.document.file_id
    else: file_id = message.audio.file_id

    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    c.execute("INSERT INTO my_files VALUES (?, ?, ?)", (file_id, message.content_type, message.caption.lower()))
    conn.commit()
    conn.close()
    bot.reply_to(message, f"✅ Tersimpan! Cari dengan ketik: {message.caption.lower()}")

# Cari file berdasarkan teks
@bot.message_handler(func=lambda message: True)
def search(message):
    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    c.execute("SELECT file_id, file_type FROM my_files WHERE caption LIKE ?", ('%' + message.text.lower() + '%',))
    res = c.fetchall()
    conn.close()

    if res:
        for f_id, f_type in res:
            if f_type == 'photo': bot.send_photo(message.chat.id, f_id)
            elif f_type == 'video': bot.send_video(message.chat.id, f_id)
            elif f_type == 'document': bot.send_document(message.chat.id, f_id)
            elif f_type == 'audio': bot.send_audio(message.chat.id, f_id)
    else:
        bot.reply_to(message, "🔍 File tidak ditemukan.")

@server.route("/")
def home(): return "Bot Aktif", 200

if __name__ == "__main__":
    init_db()
    threading.Thread(target=bot.infinity_polling).start()
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))