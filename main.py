import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

# تعريف البورت الذي توفره Render
port = int(os.environ.get("PORT", 10000))

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=port)

# ... (باقي كود البوت كما هو)

if __name__ == '__main__':
    # تشغيل السيرفر ليستقبل الطلبات
    Thread(target=run_flask).start()
    
    # تشغيل البوت
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    # ... (باقي إعدادات البوت)
    application.run_polling()
    
