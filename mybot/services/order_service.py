# services/order_service.py

from mybot.services.database import get_db_connection

def get_sales_summary():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(price) as total FROM orders WHERE DATE(order_date) = DATE('now')")
    daily = cursor.fetchone()["total"] or 0
    cursor.execute("SELECT SUM(price) as total FROM orders WHERE strftime('%W', order_date) = strftime('%W','now')")
    weekly = cursor.fetchone()["total"] or 0
    cursor.execute("SELECT SUM(price) as total FROM orders WHERE strftime('%m-%Y', order_date) = strftime('%m-%Y','now')")
    monthly = cursor.fetchone()["total"] or 0
    conn.close()
    return daily, weekly, monthly
def add_order(buyer_name, buyer_contact, buyer_address, product_id, product_name, product_code, product_price, product_category):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (buyer_name, buyer_contact, buyer_address, product_id, product_name, product_code, product_price, product_category, order_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
    """, (buyer_name, buyer_contact, buyer_address, product_id, product_name, product_code, product_price, product_category))
    conn.commit()
    conn.close()

def get_orders_by_seller(seller_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.* FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE p.owner = ?
    """, (seller_id,))
    orders = cursor.fetchall()
    conn.close()
    return orders
