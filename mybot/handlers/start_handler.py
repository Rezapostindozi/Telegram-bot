from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from telebot import TeleBot
from mybot.services.user_service import save_user
from mybot.services.subscription_service import check_subscription
from mybot.services.state import user_roles
from mybot.handlers.seller_handler import seller_menu, limited_seller_menu

def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def welcome(message):
        """
        نمایش پیغام خوشامدگویی و انتخاب نقش کاربر.
        """
        chat_id = message.chat.id
        bot.send_message(chat_id, "خوش آمدید به فروشگاه!")
        btn1 = KeyboardButton("🛒 من خریدار هستم")
        btn2 = KeyboardButton("🧾 من فروشنده هستم")
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn1, btn2)
        bot.send_message(chat_id, "لطفاً یک گزینه را انتخاب کنید:", reply_markup=markup)

    @bot.message_handler(func=lambda msg: msg.text in ["🛒 من خریدار هستم", "🧾 من فروشنده هستم"])
    def identify_user(message):
        """
        شناسایی نقش کاربر و نمایش منوی مناسب.
        """
        chat_id = message.chat.id
        full_name = message.from_user.full_name
        username = message.from_user.username or ""
        if "خریدار" in message.text:
            user_roles[chat_id] = "buyer"
            save_user(chat_id, full_name, username, "buyer")
            # نمایش منوی خریدار
            from handlers.buyer_handler import buyer_menu
            buyer_menu(bot, chat_id)
        else:
            user_roles[chat_id] = "seller"
            save_user(chat_id, full_name, username, "seller")
            if check_subscription(chat_id):
                seller_menu(bot, chat_id)
            else:
                limited_seller_menu(bot, chat_id)

    @bot.message_handler(func=lambda m: m.text == "بازگشت به خانه")
    def back_to_home(message):
        """
        بازگشت به حالت شروع.
        """
        welcome(message)
