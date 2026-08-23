from db import get_connection

def add_order(customer_id, product_id,date,status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (customer_id, product_id, date,status) VALUES (?,?,?,?)", (customer_id,product_id,date,status,))
    conn.commit()
    conn.close()

def get_orders_by_status(status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT orders.id, customers.name, products.name, orders.date, orders.status
        FROM orders
        JOIN customers ON orders.customer_id = customers.id
        JOIN products  ON orders.product_id  = products.id
        WHERE orders.status = ?
    """, (status,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_order_status(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE id = ? ", (order_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_order_status(order_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    from db import create_table
    from customer import add_customer
    from products import add_product
    create_table()
    
    add_customer("Saad", "saad@gmail.com", "0300", "Berlin")
    add_product("iPhone 15", 999, "Electronics")
    
    add_order(1, 1, "2024-01-15", "completed")
    add_order(1, 1, "2024-01-16", "returned")
    
    print(get_orders_by_status("completed"))
    print(get_order_status(1))
    
    update_order_status(1, "chargeback")
    print(get_orders_by_status("chargeback"))