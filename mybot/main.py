from telebot import TeleBot
from services.database import init_db
from handlers.start_handler import register_handlers as register_start_handlers
from handlers.product_handler import register_handlers as register_product_handlers
from handlers.subscription_handler import register_handlers as register_subscription_handlers

# ایجاد و آماده‌سازی دیتابیس
init_db()

# توکن ربات تلگرام (دسترسی شخصی خود را جایگزین کنید)
BOT_TOKEN = "7949112582:AAHUS0d19fvKn0G3eGo6MzdDbBIiBAibES8"
bot = TeleBot(BOT_TOKEN)

# ثبت هندلرها
register_start_handlers(bot)
register_product_handlers(bot)
register_subscription_handlers(bot)

print("Bot is running...")
bot.polling()
