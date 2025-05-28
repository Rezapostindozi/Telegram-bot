from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot import TeleBot
from mybot.services.product_service import add_product, get_all_products, get_products_by_category, get_categories
from mybot.services.state import user_states, user_roles
from mybot.services.subscription_service import check_subscription
from mybot.handlers.seller_handler import seller_menu, limited_seller_menu

def register_handlers(bot: TeleBot):
    @bot.message_handler(func=lambda m: m.text == "مشاهده محصولات")
    def show_products(message):
        """
        نمایش همه محصولات.
        """
        chat_id = message.chat.id
        products = get_all_products()
        if not products:
            bot.send_message(chat_id, "هیچ محصولی یافت نشد.")
            return
        for product in products:
            caption = (
                f"📌 نام: {product['name']}\n"
                f"🔢 کد: {product['code']}\n"
                f"💰 قیمت: {product['price']}\n"
                f"📦 موجودی: {product['stock']}"
            )
            bot.send_photo(chat_id, product['image'], caption=caption)

    @bot.message_handler(func=lambda m: m.text == "📂 مشاهده دسته‌بندی‌ها")
    def show_categories(message):
        """
        نمایش لیست دسته‌بندی‌ها برای انتخاب.
        """
        chat_id = message.chat.id
        categories = get_categories()
        if not categories:
            bot.send_message(chat_id, "هنوز هیچ دسته‌بندی‌ای ثبت نشده است.")
            return
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for category in categories:
            markup.add(KeyboardButton(f"🗂 {category}"))
        markup.add(KeyboardButton("بازگشت به خانه"))
        bot.send_message(chat_id, "دسته‌بندی مورد نظر را انتخاب کنید:", reply_markup=markup)

    @bot.message_handler(func=lambda m: m.text.startswith("🗂 "))
    def show_products_by_category(message):
        """
        نمایش محصولات بر اساس دسته‌بندی انتخاب‌شده.
        """
        chat_id = message.chat.id
        selected_category = message.text.replace("🗂 ", "")
        products = get_products_by_category(selected_category)
        if not products:
            bot.send_message(chat_id, "هیچ محصولی در این دسته‌بندی وجود ندارد.")
            return
        for product in products:
            caption = (
                f"📌 نام: {product['name']}\n"
                f"🔢 کد: {product['code']}\n"
                f"💰 قیمت: {product['price']}\n"
                f"📦 موجودی: {product['stock']}"
            )
            bot.send_photo(chat_id, product['image'], caption=caption)

    @bot.message_handler(func=lambda m: user_roles.get(m.chat.id) == "seller" and m.text in ["افزودن محصولات", "افزودن یک محصول"])
    def start_add_product(message):
        """
        آغاز فرآیند افزودن محصول جدید.
        """
        chat_id = message.chat.id
        user_products = get_all_products()
        if message.text == "افزودن محصولات":
            # فروشنده کامل
            if not check_subscription(chat_id):
                bot.send_message(chat_id, "⛔️ اشتراک شما منقضی شده. لطفاً ابتدا اشتراک تهیه کنید.")
                limited_seller_menu(bot, chat_id)
                return
        else:
            # فروشنده محدود (بدون اشتراک)
            if user_products:
                bot.send_message(chat_id, "❌ شما فقط اجازه افزودن ۱ محصول را دارید. برای افزودن بیشتر باید اشتراک تهیه کنید. دستور /subscribe را بزنید.")
                return

        user_states[chat_id] = {"step": "awaiting_name"}
        bot.send_message(chat_id, "لطفاً نام محصول را وارد کنید:")

    @bot.message_handler(func=lambda m: isinstance(user_states.get(m.chat.id), dict) and user_states[m.chat.id].get('step') == 'awaiting_name')
    def product_name(message):
        chat_id = message.chat.id
        product_name = message.text
        user_states[chat_id] = {"name": product_name, "step": "awaiting_code"}
        bot.send_message(chat_id, "لطفاً کد محصول را وارد کنید:")

    @bot.message_handler(func=lambda m: isinstance(user_states.get(m.chat.id), dict) and user_states[m.chat.id].get('step') == 'awaiting_code')
    def product_code(message):
        chat_id = message.chat.id
        code = message.text
        user_states[chat_id]['code'] = code
        user_states[chat_id]['step'] = 'awaiting_price'
        bot.send_message(chat_id, "لطفاً قیمت محصول را وارد کنید:")

    @bot.message_handler(func=lambda m: isinstance(user_states.get(m.chat.id), dict) and user_states[m.chat.id].get('step') == 'awaiting_price')
    def product_price(message):
        chat_id = message.chat.id
        price = message.text
        if not price.isdigit():
            bot.send_message(chat_id, "قیمت باید عدد باشد. لطفاً دوباره وارد کنید:")
            return
        user_states[chat_id]['price'] = int(price)
        user_states[chat_id]['step'] = 'awaiting_stock'
        bot.send_message(chat_id, "لطفاً موجودی (تعداد) را وارد کنید:")

    @bot.message_handler(func=lambda m: isinstance(user_states.get(m.chat.id), dict) and user_states[m.chat.id].get('step') == 'awaiting_stock')
    def product_stock(message):
        chat_id = message.chat.id
        stock = message.text
        if not stock.isdigit():
            bot.send_message(chat_id, "موجودی باید عدد باشد. لطفاً دوباره وارد کنید:")
            return
        user_states[chat_id]['stock'] = int(stock)
        user_states[chat_id]['step'] = 'awaiting_category'

        # ارسال گزینه‌های دسته‌بندی
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("آرایشی و بهداشتی"), KeyboardButton("لباس و پوشاک"))
        markup.add(KeyboardButton("کفش"), KeyboardButton("دیگر"))
        markup.add(KeyboardButton("بازگشت به خانه"))
        bot.send_message(chat_id, "لطفاً دسته‌بندی محصول را انتخاب کنید:", reply_markup=markup)

    @bot.message_handler(func=lambda m: isinstance(user_states.get(m.chat.id), dict) and user_states[m.chat.id].get('step') == 'awaiting_category')
    def get_category(message):
        chat_id = message.chat.id
        category = message.text
        user_states[chat_id]['category'] = category
        user_states[chat_id]['step'] = 'awaiting_image'
        bot.send_message(chat_id, "لطفاً عکس محصول را ارسال کنید.", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True))

    @bot.message_handler(content_types=["photo"])
    def product_photo(message):
        chat_id = message.chat.id
        if user_states.get(chat_id, {}).get('step') == "awaiting_image":
            file_id = message.photo[-1].file_id
            data = user_states.pop(chat_id)
            add_product(
                owner=chat_id,
                name=data['name'],
                code=data['code'],
                price=data['price'],
                stock=data['stock'],
                category=data['category'],
                image=file_id
            )
            bot.send_message(chat_id, "✅ محصول با موفقیت ثبت شد.")
            # بازگشت به منوی فروشنده
            seller_menu(bot, chat_id)
