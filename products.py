from db import get_connection

def add_product(name,price,category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name,price, category) VALUES (?,?,?)", (name,price,category,))
    conn.commit()
    conn.close()

def get_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products ORDER BY name ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_price(product_id,price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET price = ? WHERE id = ?", (price, product_id))
    conn.commit()
    conn.close()

def delete_product(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    from db import create_table
    create_table()
    
    add_product("iPhone 15", 999, "Electronics")
    add_product("Nike Air Max", 150, "Shoes")
    add_product("Sony Headphones", 250, "Electronics")
    
    print("All products:", get_all())
    print("Product 1:", get_product(1))
    
    update_price(1, 899)
    print("After price update:", get_product(1))
    
    delete_product(2)
    print("After delete:", get_all())
    
    
    
    