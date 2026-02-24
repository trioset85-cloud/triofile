import telebot
from telebot import types

TOKEN = "8547344412:AAEoQOZXL0dzSrkn2lvxytjDkNq4Pg9bxw4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Membuat tombol menu di tempat ngetik
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('📂 Daftar File')
    itembtn2 = types.KeyboardButton('📊 Statistik')
    itembtn3 = types.KeyboardButton('❓ Bantuan')
    markup.add(itembtn1, itembtn2, itembtn3)
    
    bot.send_message(message.chat.id, "Halo! Pilih menu di bawah:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == '📂 Daftar File':
        bot.reply_to(message, "Menampilkan daftar file kamu...")
    elif message.text == '📊 Statistik':
        bot.reply_to(message, "Kamu telah menyimpan 0 file.")
    elif message.text == '❓ Bantuan':
        bot.reply_to(message, "Kirim file apa saja, nanti saya simpan!")
    else:
        bot.reply_to(message, f"Kamu memilih: {message.text}")

if __name__ == "__main__":
    bot.infinity_polling()