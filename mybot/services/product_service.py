from mybot.services.database import get_db_connection

def add_product(owner, name, code, price, stock, category, image):
    """
    افزودن محصول جدید به جدول products.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (owner, name, code, price, stock, category, image)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (owner, name, code, price, stock, category, image))
    conn.commit()
    conn.close()

def get_all_products():
    """
    بازگرداندن همه محصولات موجود در جدول products.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def get_products_by_category(category):
    """
    بازگرداندن محصولات بر اساس دسته‌بندی.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE category = ?", (category,))
    products = cursor.fetchall()
    conn.close()
    return products

def get_categories():
    """
    بازگرداندن لیست دسته‌بندی‌های منحصربه‌فرد از محصولات.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM products")
    rows = cursor.fetchall()
    conn.close()
    return [row["category"] for row in rows]
# services/product_service.py

def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def update_product(product_id, name=None, code=None, price=None, stock=None, category=None, image=None):
    """
    ویرایش فیلدهای محصول در جدول products
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    # مثال: ویرایش نام و قیمت
    if name is not None:
        cursor.execute("UPDATE products SET name = ? WHERE id = ?", (name, product_id))
    if code is not None:
        cursor.execute("UPDATE products SET code = ? WHERE id = ?", (code, product_id))
    if price is not None:
        cursor.execute("UPDATE products SET price = ? WHERE id = ?", (price, product_id))
    if stock is not None:
        cursor.execute("UPDATE products SET stock = ? WHERE id = ?", (stock, product_id))
    if category is not None:
        cursor.execute("UPDATE products SET category = ? WHERE id = ?", (category, product_id))
    if image is not None:
        cursor.execute("UPDATE products SET image = ? WHERE id = ?", (image, product_id))
    conn.commit()
    conn.close()
