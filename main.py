import telebot
import sqlite3
import os
from telebot import types

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

# إعداد قاعدة البيانات
def init_db():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, usage_count INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

init_db()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🌍 عالم الأوتوكاد والريفت", callback_data='menu_bim'))
    bot.reply_to(message, "أهلاً بك يا هندسة. أنا مساعدك الذكي.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'menu_bim':
        bot.answer_callback_query(call.id, "جاري فتح الخدمات...")
        bot.send_message(call.message.chat.id, "🛠 اختر الخدمة المطلوبة:")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    bot.reply_to(message, "تم استلام المخطط، جاري المعالجة...")

bot.infinity_polling()
  
