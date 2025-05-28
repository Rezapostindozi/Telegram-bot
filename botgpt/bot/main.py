from database.db import init_db
from bot.bot import bot
import handlers.start
import handlers.buyer
import handlers.seller
import handlers.product
import handlers.subscription


# راه‌اندازی دیتابیس و شروع ربات
init_db()
print("ربات فروشگاهی شروع به کار کرد...")
bot.polling()
