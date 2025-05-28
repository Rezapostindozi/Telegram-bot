from bot.bot import bot
from database.db import get_db_connection
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# هندلر نمایش همه محصولات
@bot.message_handler(func=lambda m: m.text == "مشاهده محصولات")
def show_product(message):
    chat_id = message.chat.id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    all_products = cursor.fetchall()
    conn.close()

    if not all_products:
        bot.send_message(chat_id, "هیچ محصولی یافت نشد")
        return

    for product in all_products:
        msg = (
            f"📌 نام: {product['name']}\n"
            f"🔢 کد: {product['code']}\n"
            f"💰 قیمت: {product['price']}\n"
            f"📦 موجودی: {product['stock']}"
        )
        bot.send_photo(chat_id, product['image'], caption=msg)

# هندلر نمایش دسته‌بندی‌ها
@bot.message_handler(func=lambda m: m.text == "📂 مشاهده دسته‌بندی‌ها")
def show_categories(message):
    chat_id = message.chat.id
    # دریافت دسته‌بندی‌های یکتا از لیست محصولات
    from utils.states import products
    categories = set([p['category'] for p in products])

    if not categories:
        bot.send_message(chat_id, "هنوز هیچ دسته‌بندی‌ای ثبت نشده است.")
        return

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for category in categories:
        markup.add(KeyboardButton(f"🗂 {category}"))
    markup.add(KeyboardButton("بازگشت به خانه"))

    bot.send_message(chat_id, "دسته‌بندی مورد نظر را انتخاب کنید:", reply_markup=markup)

# هندلر نمایش محصولات بر اساس دسته‌بندی انتخاب شده
@bot.message_handler(func=lambda m: m.text.startswith("🗂 "))
def show_products_by_category(message):
    chat_id = message.chat.id
    from utils.states import products
    selected_category = message.text.replace("🗂 ", "")
    filtered = [p for p in products if p['category'] == selected_category]

    if not filtered:
        bot.send_message(chat_id, "هیچ محصولی در این دسته‌بندی وجود ندارد.")
        return

    for product in filtered:
        msg = (
            f"📌 نام: {product['name']}\n"
            f"🔢 کد: {product['code']}\n"
            f"💰 قیمت: {product['price']}\n"
            f"📦 موجودی: {product['stock']}"
        )
        bot.send_photo(chat_id, product['image'], caption=msg)
