import telebot
from telebot import types
import time

# Masukkan Token Bot kamu di sini
TOKEN = "8547344412:AAEoQOZXL0dzSrkn2lvxytjDkNq4Pg9bxw4"
bot = telebot.TeleBot(TOKEN)

# --- MENU UTAMA (TOMBOL) ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('📂 Daftar File')
    btn2 = types.KeyboardButton('📊 Statistik')
    btn3 = types.KeyboardButton('❓ Bantuan')
    markup.add(btn1, btn2, btn3)
    return markup

# --- HANDLER PERINTAH /START ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        "Selamat datang di @triofile_bot!\nSilakan pilih menu di bawah ini untuk mengelola file kamu:", 
        reply_markup=main_menu()
    )

# --- HANDLER UNTUK MENERIMA FILE ---
@bot.message_handler(content_types=['document', 'photo', 'video', 'audio'])
def handle_docs(message):
    bot.reply_to(message, "✅ File berhasil diterima dan disimpan di server!")

# --- HANDLER UNTUK TOMBOL MENU ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == '📂 Daftar File':
        bot.send_message(message.chat.id, "📁 Belum ada file yang tersimpan.")
    elif message.text == '📊 Statistik':
        bot.send_message(message.chat.id, "📊 Kamu telah mengirim 0 file hari ini.")
    elif message.text == '❓ Bantuan':
        bot.send_message(message.chat.id, "Cara pakai: Cukup kirimkan file apa saja (gambar, dokumen, video) ke bot ini.")
    else:
        bot.send_message(message.chat.id, "Gunakan tombol di bawah untuk berinteraksi.", reply_markup=main_menu())

# --- JALANKAN BOT ---
if __name__ == "__main__":
    print("Bot sedang berjalan...")
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)