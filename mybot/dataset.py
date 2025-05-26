import sqlite3
import datetime

def get_db_connection():
    conn = sqlite3.connect("shop_bot.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

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

    # جدول اشتراک کاربران فروشنده
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
