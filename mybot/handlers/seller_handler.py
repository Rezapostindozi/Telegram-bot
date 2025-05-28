from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from telebot import TeleBot
from mybot.services.subscription_service import check_subscription

def seller_menu(bot: TeleBot, chat_id):
    """
    نمایش منوی کامل فروشنده.
    """
    # بررسی اشتراک
    if not check_subscription(chat_id):
        limited_seller_menu(bot, chat_id)
        return
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("مشاهده محصولات")
    btn2 = KeyboardButton("حذف محصول")
    btn3 = KeyboardButton("مشاهده سفارشات")
    btn4 = KeyboardButton("بازگشت به خانه")
    btn5 = KeyboardButton("افزودن محصولات")
    btn6 = KeyboardButton("مدیریت اشتراک")
    markup.add(btn1, btn5)
    markup.add(btn2)
    markup.add(btn3, btn6)
    markup.add(btn4)
    bot.send_message(chat_id, "📋 منوی فروشنده:", reply_markup=markup)

def limited_seller_menu(bot: TeleBot, chat_id):
    """
    نمایش منوی محدود فروشنده (بدون اشتراک).
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("مشاهده محصولات")
    btn2 = KeyboardButton("افزودن یک محصول")
    btn3 = KeyboardButton("خرید اشتراک")
    btn4 = KeyboardButton("بازگشت به خانه")
    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4)
    bot.send_message(chat_id, "📋 منوی فروشنده (نسخه محدود):\nبرای استفاده از امکانات بیشتر باید اشتراک تهیه کنید.", reply_markup=markup)
