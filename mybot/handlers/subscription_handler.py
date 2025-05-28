from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot import TeleBot
from mybot.services.subscription_service import create_subscription
from mybot.services.state import user_roles
from mybot.handlers.seller_handler import seller_menu

def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['subscribe'])
    def subscribe_command(message):
        """
        فعال‌سازی اشتراک یک‌ماهه پیش‌فرض.
        """
        chat_id = message.chat.id
        # بررسی نقش کاربر (فروشنده)
        if user_roles.get(chat_id) != "seller":
            bot.send_message(chat_id, "این دستور فقط مخصوص فروشنده‌ها است.")
            return
        expires = create_subscription(chat_id, 30, "monthly")
        bot.send_message(chat_id, f"✅ اشتراک شما فعال شد و تا {expires.strftime('%Y-%m-%d')} معتبر است.")
        seller_menu(bot, chat_id)

    @bot.message_handler(func=lambda m: m.text == "خرید اشتراک")
    def buy_subscription(message):
        """
        راهنمای کاربر برای خرید اشتراک.
        """
        bot.send_message(message.chat.id, "برای خرید اشتراک لطفاً دستور /subscribe را ارسال کنید.")

    @bot.message_handler(func=lambda m: m.text == "مدیریت اشتراک")
    def manage_subscription(message):
        """
        نمایش گزینه‌های مدت زمان اشتراک.
        """
        chat_id = message.chat.id
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(
            KeyboardButton("📅 اشتراک ۱ ماهه"),
            KeyboardButton("📅 اشتراک ۳ ماهه")
        )
        markup.add(
            KeyboardButton("📅 اشتراک ۶ ماهه"),
            KeyboardButton("📅 اشتراک ۱۲ ماهه")
        )
        markup.add(KeyboardButton("بازگشت به خانه"))
        bot.send_message(chat_id, "مدت زمان اشتراک مورد نظر را انتخاب کنید:", reply_markup=markup)

    @bot.message_handler(func=lambda m: m.text.startswith("📅 اشتراک"))
    def handle_subscription_choice(message):
        """
        ثبت اشتراک بر اساس انتخاب کاربر.
        """
        chat_id = message.chat.id
        text = message.text
        days = 30
        plan_name = ""
        if "۱ ماهه" in text:
            days = 30
            plan_name = "monthly"
        elif "۳ ماهه" in text:
            days = 90
            plan_name = "3-month"
        elif "۶ ماهه" in text:
            days = 180
            plan_name = "6-month"
        elif "۱۲ ماهه" in text:
            days = 365
            plan_name = "12-month"

        expires = create_subscription(chat_id, days, plan_name)
        bot.send_message(chat_id, f"✅ اشتراک شما برای مدت {days} روز فعال شد (تا {expires.strftime('%Y-%m-%d')}).")
        seller_menu(bot, chat_id)
