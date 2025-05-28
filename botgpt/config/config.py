# فایل پیکربندی و بارگذاری متغیرهای محیطی
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")  # توکن ربات تلگرام
DATABASE = os.getenv("DATABASE", "shop_bot.db")  # مسیر فایل دیتابیس
print(TOKEN)