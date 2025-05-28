import sqlite3

def get_db_connection():
    """
    اتصال به دیتابیس SQLite.
    """
    conn = sqlite3.connect("shop_bot.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    ایجاد جداول لازم در دیتابیس در صورت وجود نداشتن.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # جدول کاربران
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            role TEXT CHECK(role IN ('buyer', 'seller')) NOT NULL,
            joined_at TEXT
        )
    """)

    # جدول محصولات
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner INTEGER,
            name TEXT,
            code TEXT,
            price INTEGER,
            stock INTEGER,
            category TEXT,
            image TEXT
        )
    """)

    # جدول اشتراک‌ها
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            user_id INTEGER PRIMARY KEY,
            is_active INTEGER,
            expires_at TEXT,
            plan TEXT
        )
    """)

    conn.commit()
    conn.close()
