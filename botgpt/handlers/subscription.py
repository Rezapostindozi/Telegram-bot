from bot.bot import bot
from utils.states import user_roles
from database.db import get_db_connection
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import datetime

# هندلر دستور /subscribe برای فعال‌سازی اشتراک فروشنده
@bot.message_handler(commands=['subscribe'])
def subscribe_handler(message):
    chat_id = message.chat.id
    if user_roles.get(chat_id) != "seller":
        bot.send_message(chat_id, "این دستور فقط مخصوص فروشنده‌ها است.")
        return
    expires = datetime.datetime.now() + datetime.timedelta(days=30)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO subscriptions (user_id, is_active, expires_at, plan)
        VALUES (?, ?, ?, ?)
    """, (chat_id, 1, expires.isoformat(), "monthly"))
    conn.commit()
    conn.close()
    bot.send_message(chat_id, f"✅ اشتراک شما فعال شد و تا {expires.strftime('%Y-%m-%d')} معتبر است.")
    # نمایش منوی فروشنده پس از فعال‌سازی اشتراک
    from utils.helpers import seller_menu
    seller_menu(chat_id)

# هندلر دکمه‌ی «خرید اشتراک»
@bot.message_handler(func=lambda m: user_roles.get(m.chat.id) == "seller" and m.text == "خرید اشتراک")
def buy_subscription(message):
    bot.send_message(message.chat.id, "برای خرید اشتراک لطفاً دستور /subscribe را ارسال کنید.")

# مدیریت اشتراک (انتخاب پلن مدت زمان)
@bot.message_handler(func=lambda m: m.text == "مدیریت اشتراک")
def manage_subscription(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📅 اشتراک ۱ ماهه"), KeyboardButton("📅 اشتراک ۳ ماهه"))
    markup.add(KeyboardButton("📅 اشتراک ۶ ماهه"), KeyboardButton("📅 اشتراک ۱۲ ماهه"))
    markup.add(KeyboardButton("بازگشت به خانه"))
    bot.send_message(chat_id, "مدت زمان اشتراک مورد نظر را انتخاب کنید:", reply_markup=markup)

# پردازش انتخاب زمان اشتراک توسط فروشنده
@bot.message_handler(func=lambda m: m.text.startswith("📅 اشتراک"))
def handle_subscription_choice(message):
    chat_id = message.chat.id
    text = message.text

    # تعیین تعداد روز بر اساس انتخاب کاربر
    days = 30
    if "۳ ماهه" in text:
        days = 90
    elif "۶ ماهه" in text:
        days = 180
    elif "۱۲ ماهه" in text:
        days = 365

    expires = datetime.datetime.now() + datetime.timedelta(days=days)

    # ذخیره اطلاعات اشتراک در دیتابیس
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO subscriptions (user_id, is_active, expires_at, plan)
        VALUES (?, ?, ?, ?)
    """, (chat_id, 1, expires.isoformat(), f"{days}-day"))
    conn.commit()
    conn.close()

    bot.send_message(chat_id, f"✅ اشتراک شما برای مدت {days} روز فعال شد (تا {expires.strftime('%Y-%m-%d')})")
    # بازگشت به منوی فروشنده
    from utils.helpers import seller_menu
    seller_menu(chat_id)
