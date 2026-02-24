import telebot
from telebot import types
import time

# Masukkan Token Bot kamu
TOKEN = "8547344412:AAEoQOZXL0dzSrkn2lvxytjDkNq4Pg9bxw4"
bot = telebot.TeleBot(TOKEN)

# Database sederhana untuk menyimpan info file (di dalam memori)
# Format: {'nama_file': 'file_id'}
file_database = {}

# --- FUNGSI TOMBOL MENU ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_list = types.KeyboardButton('📂 Semua File')
    btn_search = types.KeyboardButton('🔍 Cara Cari File')
    btn_stats = types.KeyboardButton('📊 Statistik')
    markup.add(btn_list, btn_search, btn_stats)
    return markup

# --- COMMAND START ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Selamat datang di **Trio File Storage**! ☁️\n\n"
        "Kirimkan file apa saja (dokumen, foto, video), maka saya akan menyimpannya.\n"
        "Anda bisa mencari file tersebut hanya dengan mengetik namanya."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_menu())

# --- PROSES MENERIMA & MENYIMPAN FILE ---
@bot.message_handler(content_types=['document', 'audio', 'video'])
def save_file_info(message):
    # Mengambil ID file dan Nama file
    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
    elif message.video:
        file_id = message.video.file_id
        file_name = message.video.file_name or f"video_{int(time.time())}"
    elif message.audio:
        file_id = message.audio.file_id
        file_name = message.audio.title or f"audio_{int(time.time())}"
    
    # Simpan ke database sementara
    file_database[file_name.lower()] = file_id
    
    bot.reply_to(message, f"✅ **Berhasil Disimpan!**\nNama: `{file_name}`\n\nKetik nama file kapan saja untuk mengambilnya kembali.", parse_mode="Markdown")

# --- SISTEM PENCARIAN (Cukup ketik nama file) ---
@bot.message_handler(func=lambda message: True)
def handle_search(message):
    text = message.text.lower()

    if text == '📂 semua file':
        if not file_database:
            bot.send_message(message.chat.id, "Belum ada file yang disimpan.")
        else:
            daftar = "\n".join([f"- `{n}`" for n in file_database.keys()])
            bot.send_message(message.chat.id, f"Daftar file tersimpan:\n{daftar}", parse_mode="Markdown")

    elif text == '🔍 cara cari file':
        bot.send_message(message.chat.id, "Caranya cukup ketik nama file yang pernah kamu kirim.\nContoh: jika kamu kirim `tugas.pdf`, cukup ketik `tugas` maka saya akan kirim filenya.")

    elif text == '📊 statistik':
        bot.send_message(message.chat.id, f"📊 Total file tersimpan: {len(file_database)}")

    else:
        # Logika Pencarian Nama
        found = False
        for name, f_id in file_database.items():
            if text in name: # Mencari jika ada kata yang mirip
                bot.send_document(message.chat.id, f_id, caption=f"Hasil pencarian untuk: {message.text}")
                found = True
                break
        
        if not found:
            bot.send_message(message.chat.id, "❌ File tidak ditemukan. Pastikan nama file benar.")

# --- JALANKAN BOT ---
if __name__ == "__main__":
    print("Bot Trio File Storage Aktif...")
    bot.infinity_polling()