from bot.bot import bot
from database.db import get_db_connection
from utils.states import user_states, user_roles, products
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# دریافت نام محصول
@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == "awaiting_name")
def product_name(message):
    chat_id = message.chat.id
    name = message.text
    user_states[chat_id] = {"name": name, "step": "awaiting_code"}
    bot.send_message(chat_id, "لطفاً کد محصول را وارد کنید:")

# دریافت کد محصول
@bot.message_handler(func=lambda m: isinstance(user_states.get(m.chat.id), dict) and user_states[m.chat.id].get('step') == 'awaiting_code')
def product_code(message):
    chat_id = message.chat.id
    code = message.text
    user_states[chat_id]['code'] = code
    user_states[chat_id]['step'] = 'awaiting_price'
    bot.send_message(chat_id, "قیمت محصول را وارد کنید:")

# دریافت قیمت محصول
@bot.message_handler(func=lambda m: isinstance(user_states.get(m.chat.id), dict) and user_states[m.chat.id].get('step') == 'awaiting_price')
def product_price(message):
    chat_id = message.chat.id
    price = message.text
    if not price.isdigit():
        bot.send_message(chat_id, "قیمت باید عدد باشد. لطفاً دوباره وارد کنید:")
        return
    user_states[chat_id]['price'] = int(price)
    user_states[chat_id]['step'] = 'awaiting_stock'
    bot.send_message(chat_id, "موجودی (تعداد) را وارد کنید:")

# دریافت موجودی محصول
@bot.message_handler(func=lambda m: isinstance(user_states.get(m.chat.id), dict) and user_states[m.chat.id].get('step') == 'awaiting_stock')
def product_stock(message):
    chat_id = message.chat.id
    stock = message.text
    if not stock.isdigit():
        bot.send_message(chat_id, "موجودی باید عدد باشد. لطفاً دوباره وارد کنید:")
        return
    user_states[chat_id]['stock'] = int(stock)
    user_states[chat_id]['step'] = 'awaiting_category'
    # نمایش منوی انتخاب دسته‌بندی
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("آرایشی و بهداشتی", "لباس و پوشاک")
    markup.add("کفش", "دیگر")
    btn_home = KeyboardButton("بازگشت به خانه")
    markup.add(btn_home)
    bot.send_message(chat_id, "لطفاً دسته‌بندی محصول را انتخاب کنید:", reply_markup=markup)

# دریافت دسته‌بندی محصول
@bot.message_handler(func=lambda m: isinstance(user_states.get(m.chat.id), dict) and user_states[m.chat.id].get('step') == 'awaiting_category')
def get_category(message):
    chat_id = message.chat.id
    category = message.text
    user_states[chat_id]['category'] = category
    user_states[chat_id]['step'] = 'awaiting_image'
    bot.send_message(chat_id, "لطفاً عکس محصول را ارسال کنید.")

# دریافت عکس محصول و ذخیره همه اطلاعات در دیتابیس
@bot.message_handler(content_types=['photo'])
def product_photo(message):
    chat_id = message.chat.id
    if user_states.get(chat_id, {}).get('step') == 'awaiting_image':
        file_id = message.photo[-1].file_id
        # افزودن تصویر به اطلاعات محصول
        user_states[chat_id]['image'] = file_id
        # ذخیره اطلاعات محصول در دیتابیس
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (owner, name, code, price, stock, category, image)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            chat_id,
            user_states[chat_id]['name'],
            user_states[chat_id]['code'],
            user_states[chat_id]['price'],
            user_states[chat_id]['stock'],
            user_states[chat_id]['category'],
            file_id
        ))
        conn.commit()
        conn.close()
        bot.send_message(chat_id, "✅ محصول با موفقیت ثبت شد.")
        # پاک کردن وضعیت کاربر پس از ثبت محصول
        user_states.pop(chat_id, None)
