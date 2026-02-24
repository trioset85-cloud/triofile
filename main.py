import telebot
import time
from flask import Flask
from threading import Thread

# --- BAGIAN WEB SERVER (AGAR BOT TIDAK TIDUR) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot @triofile_bot sedang Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BAGIAN BOT TELEGRAM ---
TOKEN = "8547344412:AAEoQOZXL0dzSrkn2lvxytjDkNq4Pg9bxw4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Bot ini sudah menggunakan sistem anti-tidur dan aktif 24 jam.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Pesan diterima: {message.text}")

# --- JALANKAN SEMUANYA ---
if __name__ == "__main__":
    print("Memulai Web Server...")
    keep_alive()  # Menjalankan Flask di latar belakang
    print("Bot @triofile_bot sedang berjalan...")
    
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)