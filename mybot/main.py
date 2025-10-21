from telebot import TeleBot
from services.database import init_db
from handlers.start_handler import register_handlers as register_start_handlers
from handlers.product_handler import register_handlers as register_product_handlers
from handlers.subscription_handler import register_handlers as register_subscription_handlers

init_db()

BOT_TOKEN = ""
bot = TeleBot(BOT_TOKEN)

register_start_handlers(bot)
register_product_handlers(bot)
register_subscription_handlers(bot)

print("Bot is running...")
bot.polling()
