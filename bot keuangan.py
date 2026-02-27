import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import csv
import os
from datetime import datetime

# Token API kamu
TOKEN = '8547344412:AAEoQOZXL0dzSrkn2lvxytjDkNq4Pg9bxw4'
FILE_NAME = 'data_keuangan.csv'

# Tahapan percakapan
KATEGORI, NOMINAL = range(2)

# --- MENU TOMBOL ---
def main_menu_keyboard():
    keyboard = [['📝 Catat Pengeluaran', '📊 Laporan Hari Ini'], ['❌ Batal']]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

# --- FUNGSI UTAMA ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 **Selamat Datang di @triofile_bot**\n\n"
        "Silakan pilih menu di bawah ini untuk mulai mengelola keuanganmu:",
        reply_markup=main_menu_keyboard()
    )

# --- PROSES MENCATAT ---

async def start_catat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Apa kategori pengeluarannya?\n(Contoh: Makan, Bensin, Jajan)",
        reply_markup=ReplyKeyboardRemove() # Sembunyikan tombol saat mengetik
    )
    return KATEGORI

async def get_kategori(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['kategori'] = update.message.text
    await update.message.reply_text(f"Oke, kategori '{update.message.text}'. Berapa nominalnya? (Hanya angka)")
    return NOMINAL

async def get_nominal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_input = update.message.text.replace('.', '').replace(',', '')
    
    if not raw_input.isdigit():
        await update.message.reply_text("⚠️ Mohon masukkan angka saja!")
        return NOMINAL

    nominal = int(raw_input)
    kategori = context.user_data['kategori']
    tgl_lengkap = datetime.now().strftime("%d/%m/%Y %H:%M")
    tgl_hari_ini = datetime.now().strftime("%d/%m/%Y")
    
    # Simpan ke CSV
    file_exists = os.path.isfile(FILE_NAME)
    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([tgl_hari_ini, tgl_lengkap, kategori, nominal])
    
    await update.message.reply_text(
        f"✅ **Berhasil dicatat!**\n\n📅 {tgl_lengkap}\n📂 {kategori}\n💰 Rp{nominal:,}",
        reply_markup=main_menu_keyboard() # Munculkan tombol lagi
    )
    return ConversationHandler.END

# --- FITUR LAPORAN ---

async def laporan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hari_ini = datetime.now().strftime("%d/%m/%Y")
    total = 0
    catatan = ""

    if not os.path.exists(FILE_NAME):
        await update.message.reply_text("Belum ada data keuangan yang tercatat.")
        return

    with open(FILE_NAME, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == hari_ini:
                total += int(row[3])
                catatan += f"• {row[2]}: Rp{int(row[3]):,}\n"

    if total > 0:
        pesan = f"📊 **Laporan Hari Ini ({hari_ini})**\n\n"
        pesan += catatan
        pesan += f"\n──────────────\n**Total: Rp{total:,}**"
        await update.message.reply_text(pesan, reply_markup=main_menu_keyboard())
    else:
        await update.message.reply_text(f"Belum ada pengeluaran hari ini ({hari_ini}).", reply_markup=main_menu_keyboard())

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Proses dibatalkan.", reply_markup=main_menu_keyboard())
    return ConversationHandler.END

# --- KONFIGURASI BOT ---

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('catat', start_catat),
            MessageHandler(filters.Regex('^📝 Catat Pengeluaran$'), start_catat)
        ],
        states={
            KATEGORI: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_kategori)],
            NOMINAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_nominal)],
        },
        fallbacks=[
            CommandHandler('cancel', cancel),
            MessageHandler(filters.Regex('^❌ Batal$'), cancel)
        ],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("laporan", laporan))
    app.add_handler(MessageHandler(filters.Regex('^📊 Laporan Hari Ini$'), laporan))
    app.add_handler(conv_handler)
    
    print("Bot @triofile_bot siap dengan menu tombol!")
    app.run_polling()

if __name__ == '__main__':
    main()