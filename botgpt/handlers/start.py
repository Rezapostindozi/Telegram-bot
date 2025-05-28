from bot.bot import bot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from utils.states import user_roles
from database.db import save_user
from utils.helpers import buyer_menu, seller_menu, limited_seller_menu, check_subscription

# هندلر دستور /start برای خوش‌آمدگویی و انتخاب نقش کاربر
@bot.message_handler(commands=['start'])
def wellcome(message):
    bot.send_message(message.chat.id, "👋 خوش آمدید به فروشگاه")
    btn1 = KeyboardButton("🛒 من خریدار هستم")
    btn2 = KeyboardButton("🧾 من فروشنده هستم")
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "لطفاً نقش خود را انتخاب کنید:", reply_markup=markup)

# هندلر تشخیص نقش کاربر (خریدار یا فروشنده)
@bot.message_handler(func=lambda msg: msg.text in ["🛒 من خریدار هستم", "🧾 من فروشنده هستم"])
def shenasaii_user(message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    username = message.from_user.username

    if "خریدار" in message.text:
        user_roles[chat_id] = "buyer"
        save_user(chat_id, full_name, username, "buyer")
        buyer_menu(chat_id)
    else:
        user_roles[chat_id] = "seller"
        save_user(chat_id, full_name, username, "seller")
        # بررسی اشتراک فروشنده
        if check_subscription(chat_id):
            seller_menu(chat_id)
        else:
            limited_seller_menu(chat_id)
