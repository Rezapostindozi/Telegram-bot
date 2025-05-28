from bot.bot import bot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import get_db_connection
from utils.states import user_roles
import datetime

# بررسی وضعیت اشتراک کاربر
def check_subscription(chat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subscriptions WHERE user_id = ?", (chat_id,))
    sub = cursor.fetchone()
    conn.close()

    if not sub or not sub["is_active"]:
        return False
    if datetime.datetime.fromisoformat(sub["expires_at"]) < datetime.datetime.now():
        return False
    return True

# نمایش منوی خریدار
def buyer_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("مشاهده محصولات")
    btn2 = KeyboardButton("پیگیری سفارش")
    btn3 = KeyboardButton("📂 مشاهده دسته‌بندی‌ها")
    btn4 = KeyboardButton("بازگشت به خانه")
    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4)
    bot.send_message(chat_id, "📋 منوی خریدار:", reply_markup=markup)

# نمایش منوی فروشنده (نسخه کامل)
def seller_menu(chat_id):
    # اگر اشتراک منقضی شده باشد، نمایش منوی محدود
    if not check_subscription(chat_id):
        limited_seller_menu(chat_id)
        return
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("مشاهده محصولات ")
    btn2 = KeyboardButton("حذف محصول ")
    btn3 = KeyboardButton("مشاهده سفارشات ")
    btn4 = KeyboardButton("بازگشت به خانه ")
    btn5 = KeyboardButton("افزودن محصولات ")
    btn6 = KeyboardButton("مدیریت اشتراک")
    markup.add(btn1, btn5)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4, btn6)
    bot.send_message(chat_id, "📋 منوی فروشنده:", reply_markup=markup)

# نمایش منوی فروشنده (نسخه محدود)
def limited_seller_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("مشاهده محصولات")
    btn2 = KeyboardButton("افزودن یک محصول")
    btn3 = KeyboardButton("خرید اشتراک")
    btn4 = KeyboardButton("بازگشت به خانه")
    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4)
    bot.send_message(chat_id, "📋 منوی فروشنده (نسخه محدود):\nبرای استفاده از امکانات بیشتر باید اشتراک تهیه کنید.", reply_markup=markup)
