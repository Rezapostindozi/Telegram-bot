from mybot.services.database import get_db_connection
import datetime

def save_user(user_id, full_name, username, role):
    """
    ذخیره کاربر در جدول users.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, full_name, username, role, joined_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, full_name, username, role, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()
