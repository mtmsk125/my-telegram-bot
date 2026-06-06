import os
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. إعداد قاعدة البيانات
def init_db():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)''')
    conn.commit()
    conn.close()

init_db()

# 2. القائمة الرئيسية
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌍 عالم الأوتوكاد والريفت", callback_data='menu_bim')],
        [InlineKeyboardButton("📚 المرجع الهندسي", callback_data='mep_tools')],
        [InlineKeyboardButton("🤖 اسأل المساعد الذكي", callback_data='tech_solutions')]
    ])

# 3. وظيفة البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تسجيل المستخدم
    user_id = update.effective_user.id
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()
    
    await update.message.reply_text("🏗️ أهلاً بك يا هندسة في منصتك الهندسية!\nاختر الخدمة:", reply_markup=get_main_menu())

# 4. معالج الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'menu_bim':
        await query.edit_message_text("🛠 عالم الأوتوكاد والريفت...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data='back')]]))
    elif query.data == 'back':
        await query.edit_message_text("🏗️ أهلاً بك يا هندسة في منصتك الهندسية!\nاختر الخدمة:", reply_markup=get_main_menu())

# 5. تشغيل البوت
if __name__ == '__main__':
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
