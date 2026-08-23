import sqlite3
from db import get_connection

def add_customer(name, email, phone, city):
    conn = get_connection()
    cursor = conn.cursor() 
    cursor.execute("INSERT INTO customers (name, email, phone, city) VALUES (?,?,?,?) ", (name, email, phone, city,))
    conn.commit()
    conn.close()

def get_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    row = cursor.fetchone()    # fetchone DIRECTLY after execute
    conn.close()
    return row

def get_all_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers ORDER BY name ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_customer(customer_id, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET email = ? WHERE id = ?", (email,customer_id))
    conn.commit()
    conn.close()

def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    from db import create_table
    create_table()
    
    add_customer("Saad", "saad@gmail.com", "0300-1234567", "Berlin")
    add_customer("Ali", "ali@gmail.com", "0311-9876543", "Karachi")
    
    print("All customers:", get_all_customers())
    print("Customer 1:", get_customer(1))
    print("Customer 2:", get_customer(2))