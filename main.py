import os
import sqlite3
import logging
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. إعداد خادم Flask الوهمي لإرضاء Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. إعداد قاعدة البيانات
def init_db():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)''')
    conn.commit()
    conn.close()

init_db()

# 3. القائمة الرئيسية
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌍 عالم الأوتوكاد والريفت", callback_data='menu_bim')],
        [InlineKeyboardButton("📚 المرجع الهندسي", callback_data='mep_tools')],
        [InlineKeyboardButton("🤖 اسأل المساعد الذكي", callback_data='tech_solutions')]
    ])

# 4. وظيفة البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()
    await update.message.reply_text("🏗️ أهلاً بك يا هندسة في منصتك الهندسية!\nاختر الخدمة:", reply_markup=get_main_menu())

# 5. معالج الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'menu_bim':
        await query.edit_message_text("🛠 عالم الأوتوكاد والريفت...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data='back')]]))
    elif query.data == 'back':
        await query.edit_message_text("🏗️ أهلاً بك يا هندسة في منصتك الهندسية!\nاختر الخدمة:", reply_markup=get_main_menu())

if __name__ == '__main__':
    # تشغيل Flask في خلفية منفصلة
    Thread(target=run_flask).start()
    
    # تشغيل البوت
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()
