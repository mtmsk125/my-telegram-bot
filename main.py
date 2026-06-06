import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler

# إعدادات الـ Logs لتتمكن من متابعة الأخطاء في Render
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# دالة الرد على أمر /start
async def start(update, context):
    await update.message.reply_text("أهلاً بك يا هندسة، البوت يعمل الآن بنجاح!")

if __name__ == '__main__':
    # جلب التوكن من إعدادات Render
    TOKEN = os.environ.get("BOT_TOKEN")
    
    # بناء التطبيق
    application = ApplicationBuilder().token(TOKEN).build()
    
    # إضافة أمر الـ Start
    application.add_handler(CommandHandler("start", start))
    
    # تشغيل البوت
    print("Bot is running...")
    application.run_polling()
    
