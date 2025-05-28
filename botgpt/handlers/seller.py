from bot.bot import bot
from utils.states import user_roles, user_states
from utils.helpers import limited_seller_menu, check_subscription

# هندلر افزودن محصول (نسخه کامل، برای فروشنده‌های دارای اشتراک)
@bot.message_handler(func=lambda m: user_roles.get(m.chat.id) == "seller" and m.text == "افزودن محصولات")
def start_add_product(message):
    chat_id = message.chat.id
    if not check_subscription(chat_id):
        bot.send_message(chat_id, "⛔️ اشتراک شما منقضی شده. لطفاً ابتدا اشتراک تهیه کنید.")
        limited_seller_menu(chat_id)
        return
    user_states[chat_id] = "awaiting_name"
    bot.send_message(chat_id, "لطفاً نام محصول را وارد کنید:")

# هندلر افزودن محصول (نسخه محدود، برای فروشنده‌های بدون اشتراک یا محدود)
@bot.message_handler(func=lambda m: user_roles.get(m.chat.id) == "seller" and m.text == "افزودن یک محصول")
def start_add_product_limited(message):
    chat_id = message.chat.id
    from utils.states import products
    user_products = [p for p in products if p.get('owner') == chat_id]
    if len(user_products) >= 1 and not check_subscription(chat_id):
        bot.send_message(chat_id, "❌ شما فقط اجازه افزودن ۱ محصول را دارید. برای افزودن بیشتر باید اشتراک تهیه کنید. دستور /subscribe را بزنید.")
        return
    user_states[chat_id] = {"step": "awaiting_name"}
    bot.send_message(chat_id, "لطفاً نام محصول را وارد کنید:")
