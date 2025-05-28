from mybot.services.database import get_db_connection
import datetime
def check_subscription(user_id):
    """
    بررسی معتبر بودن اشتراک کاربر.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subscriptions WHERE user_id = ?", (user_id,))
    sub = cursor.fetchone()
    conn.close()

    if not sub:
        return False
    if not sub["is_active"]:
        return False
    if datetime.datetime.fromisoformat(sub["expires_at"]) < datetime.datetime.now():
        return False
    return True

def create_subscription(user_id, days, plan):
    """
    ایجاد یا به‌روزرسانی اشتراک کاربر.
    """
    expires = datetime.datetime.now() + datetime.timedelta(days=days)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO subscriptions (user_id, is_active, expires_at, plan)
        VALUES (?, ?, ?, ?)
    """, (user_id, 1, expires.isoformat(), plan))
    conn.commit()
    conn.close()
    return expires
