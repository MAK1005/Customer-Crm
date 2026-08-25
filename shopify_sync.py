import requests
import os
from dotenv import load_dotenv
from db import get_connection

load_dotenv()

STORE = os.getenv("SHOPIFY_STORE")
TOKEN = os.getenv("SHOPIFY_TOKEN")
headers = {"X-Shopify-Access-Token": TOKEN}

def sync_customers():
    conn = get_connection()
    cursor = conn.cursor()
    response = requests.get(
        f"https://{STORE}/admin/api/2024-01/customers.json?limit=50",
        headers=headers
    )
    customers = response.json()["customers"]
    for c in customers:
        name = f"{c['first_name']} {c['last_name']}"
        email = c["email"]
        phone = c["phone"] or "N/A"
        city = c.get("default_address", {}).get("city", "N/A")
        cursor.execute("""
            INSERT OR IGNORE INTO customers (id, name, email, phone, city)
            VALUES (?,?,?,?,?)
        """, (c["id"], name, email, phone, city))
    conn.commit()
    conn.close()
    print(f"Synced {len(customers)} customers")

def sync_products():
    conn = get_connection()
    cursor = conn.cursor()
    response = requests.get(
        f"https://{STORE}/admin/api/2024-01/products.json?limit=50",
        headers=headers
    )
    products = response.json()["products"]
    for p in products:
        price = float(p["variants"][0]["price"]) if p["variants"] else 0
        cursor.execute("""
            INSERT OR IGNORE INTO products (id, name, price, category)
            VALUES (?,?,?,?)
        """, (p["id"], p["title"], price, p["product_type"] or "Uncategorized"))
    conn.commit()
    conn.close()
    print(f"Synced {len(products)} products")

def sync_orders():
    conn = get_connection()
    cursor = conn.cursor()
    response = requests.get(
        f"https://{STORE}/admin/api/2024-01/orders.json?limit=50&status=any",
        headers=headers
    )
    orders = response.json()["orders"]
    for o in orders:
        customer_id = o["customer"]["id"] if o.get("customer") else None
        product_id = o["line_items"][0]["product_id"] if o["line_items"] else None
        date = o["created_at"][:10]
        status = o["financial_status"]
        if customer_id and product_id:
            cursor.execute("""
                INSERT OR IGNORE INTO orders (id, customer_id, product_id, date, status)
                VALUES (?,?,?,?,?)
            """, (o["id"], customer_id, product_id, date, status))
    conn.commit()
    conn.close()
    print(f"Synced {len(orders)} orders")

def sync_refunds():
    conn = get_connection()
    cursor = conn.cursor()
    
    response = requests.get(
        f"https://{STORE}/admin/api/2024-01/orders.json?limit=50&status=any&financial_status=refunded",
        headers=headers
    )
    orders = response.json()["orders"]
    count = 0
    
    for order in orders:
        customer_id = order["customer"]["id"] if order.get("customer") else None
        if not customer_id:
            continue
        for refund in order["refunds"]:
            date = refund["created_at"][:10]
            note = refund.get("note", "No reason provided")
            if refund["refund_line_items"]:
                product = refund["refund_line_items"][0]["line_item"]["title"]
                note = f"{note} — Product: {product}"
            cursor.execute("""
                INSERT INTO communications (customer_id, date, type, notes)
                VALUES (?,?,?,?)
            """, (customer_id, date, "return_request", note))
            count += 1
    
    conn.commit()
    conn.close()
    print(f"Synced {count} refunds as communications")

if __name__ == "__main__":
    print("=== Shopify Sync ===")
    from db import get_connection, create_table
    create_table()
    sync_customers()
    sync_products()
    sync_orders()
    sync_refunds()
    print("Done!")

    from db import get_connection

    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM customers")
    print("Customers:", cursor.fetchone()[0])
    
    cursor.execute("SELECT COUNT(*) FROM products")
    print("Products:", cursor.fetchone()[0])
    
    cursor.execute("SELECT COUNT(*) FROM orders")
    print("Orders:", cursor.fetchone()[0])
    
    cursor.execute("SELECT * FROM customers LIMIT 3")
    for row in cursor.fetchall():
        print(row)
    
    conn.close()

    from reports import most_returned_products, top_selling_products

    print(most_returned_products())
    print(top_selling_products())

    from reports import most_returned_products, top_selling_products, chargeback_summary

    print("\n=== Most Returned Products ===")
    for row in most_returned_products():
        print(f"{row[0]} — {row[1]} returns")

    print("\n=== Top Selling Products ===")
    for row in top_selling_products():
        print(f"{row[0]} — {row[1]} sales")

  