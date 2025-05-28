from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from telebot import TeleBot

def buyer_menu(bot: TeleBot, chat_id):
    """
    نمایش منوی خریدار.
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("مشاهده محصولات")
    btn2 = KeyboardButton("پیگیری سفارش")
    btn3 = KeyboardButton("📂 مشاهده دسته‌بندی‌ها")
    btn4 = KeyboardButton("بازگشت به خانه")
    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4)
    bot.send_message(chat_id, "📋 منوی خریدار:", reply_markup=markup)
