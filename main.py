from telebot import types

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Membuat wadah tombol
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Membuat tombol-tombolnya
    btn_list = types.InlineKeyboardButton("Daftar File 📂", callback_data="list_files")
    btn_stats = types.InlineKeyboardButton("Statistik 📊", callback_data="show_stats")
    btn_help = types.InlineKeyboardButton("Bantuan ❓", callback_data="show_help")
    btn_admin = types.InlineKeyboardButton("Kontak Admin 👨‍💻", url="https://t.me/username_kamu")

    # Memasukkan tombol ke wadah
    markup.add(btn_list, btn_stats, btn_help, btn_admin)

    bot.send_message(message.chat.id, "Halo! Selamat datang di @triofile_bot.\nSilakan pilih menu di bawah ini:", reply_markup=markup)

# Logika untuk menangani ketika tombol dipencet
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "list_files":
        bot.answer_callback_query(call.id, "Membuka daftar file...")
        bot.send_message(call.message.chat.id, "Fitur Daftar File sedang dalam pengembangan.")
    elif call.data == "show_stats":
        bot.send_message(call.message.chat.id, "Total file tersimpan: 0")
    elif call.data == "show_help":
        bot.send_message(call.message.chat.id, "Cara simpan file: Cukup kirimkan dokumen/foto ke bot ini.")