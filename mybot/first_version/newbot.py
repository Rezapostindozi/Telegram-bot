import pandas as pd
import telebot
from telebot.types import InlineKeyboardButton , InlineKeyboardMarkup , ReplyKeyboardMarkup , KeyboardButton
import datetime
import sqlite3
from dataset import init_db, get_db_connection , save_user # ایمپورت توابع دیتابیس

# ساخت دیتابیس موقع اجرای ربات (یک بار فقط)
init_db()

bot = telebot.TeleBot("7949112582:AAHUS0d19fvKn0G3eGo6MzdDbBIiBAibES8")
user_subscriptions={}
user_roles={}
user_states={}
products=[]
@bot.message_handler(commands=['start'])
def wellcome (message):
    bot.send_message(message.chat.id , "Wellcome to Shope")
    btn1 = KeyboardButton("🛒 من خریدار هستم")
    btn2 = KeyboardButton("🧾 من فروشنده هستم")
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(message.chat.id , "Please Enter one more ",reply_markup=markup)
#--------------------------------------------------------------------------------------
def check_subscription(chat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subscriptions WHERE user_id = ?", (chat_id,))
    sub = cursor.fetchone()
    conn.close()

    if not sub:
        return False
    if not sub["is_active"]:
        return False
    if datetime.datetime.fromisoformat(sub["expires_at"]) < datetime.datetime.now():
        return False
    return True

#-----------------------------------------------------------------------------------

@bot.message_handler(func=lambda msg : msg.text in ["🛒 من خریدار هستم", "🧾 من فروشنده هستم"])
def shenasaii_user (message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    username = message.from_user.username

    if "خریدار" in message.text :
        user_roles[chat_id] = "buyer"
        save_user(chat_id,full_name ,username,"buyer" )
        buyer_menu(chat_id)
    else:
        user_roles[chat_id] = "seller"
        save_user(chat_id , full_name,username , "seller")
        if check_subscription(chat_id):
            seller_menu(chat_id)
        else:
            limited_seller_menu(chat_id)
            


def buyer_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("مشاهده محصولات")
    btn2 = KeyboardButton("پیگیری سفارش")
    btn3 = KeyboardButton("📂 مشاهده دسته‌بندی‌ها")
    btn4 = KeyboardButton("بازگشت به خانه")
    markup.add(btn1,btn2)
    markup.add(btn3)
    markup.add(btn4)

    bot.send_message(chat_id, "📋 منوی خریدار:", reply_markup=markup)

def seller_menu(chat_id):
    if not check_subscription(chat_id):
        limited_seller_menu(chat_id)
        return
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 =KeyboardButton("مشاهده محصولات ")
    btn2 =KeyboardButton("حذف محصول ")
    btn3 =KeyboardButton("مشاهده سفارشات ")
    btn4 =KeyboardButton("بازگشت به خانه ")
    btn5 =KeyboardButton("افزودن محصولات ")
    btn6 = KeyboardButton("مدیریت اشتراک")

    markup.add(btn1 , btn5)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4 , btn6)

    bot.send_message(chat_id, "📋 منوی فروشنده:", reply_markup=markup)

#----------------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------------------


@bot.message_handler(func=lambda msg: msg.text == "بازگشت به خانه")
def back_to_home(message):
    wellcome(message)  # دوباره تابع start رو صدا می‌زنیم

@bot.message_handler(func=lambda m: user_roles.get(m.chat.id)=="seller"and m.text =="افزودن محصولات")
def start_add_product(message):
    chat_id = message.chat.id
    if not check_subscription(chat_id):  # ✅ اضافه کن
        bot.send_message(chat_id, "⛔️ اشتراک شما منقضی شده. لطفاً ابتدا اشتراک تهیه کنید.")
        limited_seller_menu(chat_id)
        return
    chat_id =message.chat.id
    user_states[chat_id] ="awaiting_name"
    bot.send_message(chat_id,"Please Enter product name ")

#--------------------------------------------------------------------------------------------
@bot.message_handler(func=lambda m: user_roles.get(m.chat.id) == "seller" and m.text == "افزودن یک محصول")
def start_add_product_limited(message):
    chat_id = message.chat.id
    user_products = [p for p in products if p.get('owner') == chat_id]
    if len(user_products) >= 1 and not check_subscription(chat_id):
        bot.send_message(chat_id, "❌ شما فقط اجازه افزودن ۱ محصول را دارید. برای افزودن بیشتر باید اشتراک تهیه کنید. دستور /subscribe را بزنید.")
        return
    user_states[chat_id] = {"step": "awaiting_name"}
    bot.send_message(chat_id, "لطفاً نام محصول را وارد کنید:")

#--------------------------------------------------------------------------------------------



@bot.message_handler(func=lambda m: user_states.get(m.chat.id)=="awaiting_name")
def product_name(message):
    chat_id = message.chat.id
    product_name = message.text
    user_states[chat_id]= {"name": product_name,"step":"awaiting_code"}
    bot.send_message(chat_id,"Enter the product code")
@bot.message_handler(func=lambda m: isinstance(user_states.get(m.chat.id), dict) and user_states[m.chat.id].get('step') == 'awaiting_code')
def product_code(message):
    chat_id = message.chat.id
    product_code = message.text
    user_states[chat_id]['code'] = product_code
    user_states[chat_id]['step'] = 'awaiting_price'
    bot.send_message(chat_id, "قیمت محصول را وارد کنید:")

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


@bot.message_handler(func=lambda m: isinstance(user_states.get(m.chat.id), dict) and user_states[m.chat.id].get('step') == 'awaiting_stock')
def product_stock(message):
    chat_id = message.chat.id
    stock = message.text
    if not stock.isdigit():
        bot.send_message(chat_id, "موجودی باید عدد باشد. لطفاً دوباره وارد کنید:")
        return
    user_states[chat_id]['stock'] = int(stock)
    # بعد از گرفتن موجودی:
    user_states[chat_id]['stock'] = message.text
    user_states[chat_id]['step'] = 'awaiting_image'
    #bot.send_message(chat_id, "لطفاً عکس محصول را ارسال کنید.")

    #---------------------------------------------------------------------------------------
    user_states[chat_id]['stock'] = int(stock)
    user_states[chat_id]['step'] = 'awaiting_category'

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("آرایشی و بهداشتی", "لباس و پوشاک")
    markup.add("کفش", "دیگر")
    btn1 =KeyboardButton('بازگشت به خانه')
    markup.add(btn1)

    bot.send_message(chat_id, "لطفاً دسته‌بندی محصول را انتخاب کنید:", reply_markup=markup)
#--------------------------------------------------------------------------------------------
@bot.message_handler(func=lambda m: isinstance(user_states.get(m.chat.id), dict) and user_states[m.chat.id].get(
    'step') == 'awaiting_category')
def get_category(message):
    chat_id = message.chat.id
    category = message.text
    user_states[chat_id]['category'] = category
    user_states[chat_id]['step'] = 'awaiting_image'

    bot.send_message(chat_id, "لطفاً عکس محصول را ارسال کنید.", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True))
#------------------------------------------------------------------------------------------------


@bot.message_handler(content_types=["photo"])
def product_photo(message):
    chat_id=message.chat.id
    if user_states.get(chat_id, {}).get('step')=="awaiting_image":
        file_id = message.photo[-1].file_id
        user_states[chat_id]['image']=file_id
    bot.send_message(chat_id , "محصول ثبت شد ")
    # حالا همه اطلاعات رو داریم، می‌تونیم ذخیره کنیم
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

    """user_states.pop(chat_id)  # پاک کردن حالت فعلی کاربر

    bot.send_message(chat_id, f"محصول با موفقیت اضافه شد:\n"
                              f"نام: {product['name']}\n"
                              f"کد: {product['code']}\n"
                              f"قیمت: {product['price']}\n"
                              f"موجودی: {product['stock']}\n"
                              f"{product['image']}")

    # برگرداندن فروشنده به منوی خودش
    seller_menu(chat_id)"""

@bot.message_handler(func=lambda m : m.text == "مشاهده محصولات")
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

#------------------------------------------------------------------------
@bot.message_handler(func=lambda m: m.text == "📂 مشاهده دسته‌بندی‌ها")
def show_categories(message):
    chat_id = message.chat.id
    categories = set([p['category'] for p in products])

    if not categories:
        bot.send_message(chat_id, "هنوز هیچ دسته‌بندی‌ای ثبت نشده است.")
        return

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for category in categories:
        markup.add(KeyboardButton(f"🗂 {category}"))
    markup.add(KeyboardButton("بازگشت به خانه"))

    bot.send_message(chat_id, "دسته‌بندی مورد نظر را انتخاب کنید:", reply_markup=markup)
#-------------------------------------------------------------------------------------
@bot.message_handler(func=lambda m: m.text.startswith("🗂 "))
def show_products_by_category(message):
    chat_id = message.chat.id
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
#--------------------------------------------------------------------------------------

# هندلر دستور /subscribe
@bot.message_handler(commands=['subscribe'])
def subscribe_handler(message):
    chat_id = message.chat.id
    if user_roles.get(chat_id) != "seller":
        bot.send_message(chat_id, "این دستور فقط مخصوص فروشنده‌ها است.")
        return
    expires = datetime.datetime.now() + datetime.timedelta(days=30)
    conn = get_db_connection()
    cursor = conn.cursor()
    expires = datetime.datetime.now() + datetime.timedelta(days=30)
    cursor.execute("""
        INSERT OR REPLACE INTO subscriptions (user_id, is_active, expires_at, plan)
        VALUES (?, ?, ?, ?)
    """, (chat_id, 1, expires.isoformat(), "monthly"))
    conn.commit()
    conn.close()

    bot.send_message(chat_id, f"✅ اشتراک شما فعال شد و تا {expires.strftime('%Y-%m-%d')} معتبر است.")
    seller_menu(chat_id)

# هندلر دکمه "خرید اشتراک"
@bot.message_handler(func=lambda m: user_roles.get(m.chat.id) == "seller" and m.text == "خرید اشتراک")
def buy_subscription(message):
    bot.send_message(message.chat.id, "برای خرید اشتراک لطفاً دستور /subscribe را ارسال کنید.")
#______________________________________________________________________________________________________
@bot.message_handler(func=lambda m: m.text == "مدیریت اشتراک")
def manage_subscription(message):
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
    chat_id = message.chat.id
    text = message.text

    # تعیین تعداد روزها بر اساس انتخاب کاربر
    days = 30
    if "۳ ماهه" in text:
        days = 90
    elif "۶ ماهه" in text:
        days = 180
    elif "۱۲ ماهه" in text:
        days = 365

    expires = datetime.datetime.now() + datetime.timedelta(days=days)

    # ذخیره در دیتابیس
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO subscriptions (user_id, is_active, expires_at, plan)
        VALUES (?, ?, ?, ?)
    """, (chat_id, 1, expires.isoformat(), f"{days}-day"))
    conn.commit()
    conn.close()

    bot.send_message(chat_id, f"✅ اشتراک شما برای مدت {days} روز فعال شد (تا {expires.strftime('%Y-%m-%d')})")
    seller_menu(chat_id)  # برگشت به منوی فروشنده





print("Bot is Running ...")
bot.polling()