import sqlite3
import datetime
from config.config import DATABASE

def get_db_connection():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # ایجاد جدول کاربران
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            role TEXT CHECK(role IN ('buyer', 'seller')) NOT NULL,
            joined_at TEXT,
            subscription_status TEXT DEFAULT 'inactive'
        )
    """)

    # ایجاد جدول محصولات
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

    # ایجاد جدول اشتراک
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

def save_user(user_id, full_name, username, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, full_name, username, role, joined_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, full_name, username, role, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()
