from db import get_connection

def most_returned_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                SELECT products.name, COUNT(*) as return_count
                FROM  orders
                JOIN  products ON orders.product_id = products.id
                WHERE orders.status = 'returned'
                GROUP BY products.id
                ORDER BY return_count DESC
            """)
    rows = cursor.fetchall()
    conn.close()
    return rows
    

def most_cancelled_by_product():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                SELECT products.name, COUNT(*) as return_count
                FROM  orders
                JOIN  products ON orders.product_id = products.id
                WHERE orders.status = 'cancelled'
                GROUP BY products.id
                ORDER BY return_count DESC
            """)
    rows = cursor.fetchall()
    conn.close()
    return rows
    
    

def chargeback_summary():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT products.name, COUNT(*) as return_count
                    FROM  orders
                    JOIN  products ON orders.product_id = products.id
                    WHERE orders.status = 'chargeback'
                    GROUP BY products.id
                    ORDER BY return_count DESC
                """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def top_selling_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                SELECT products.name, COUNT(*) as sale_count
                FROM  orders
                JOIN products ON orders.product_id = products.id
                WHERE status = 'completed'
                GROUP BY products.id
                ORDER BY sale_count DESC
            """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def lowest_rated_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                SELECT products.name, AVG(reviews.rating) as avg_rating
                FROM  reviews
                JOIN  products ON reviews.product_id = products.id
                GROUP BY products.id
                ORDER BY avg_rating ASC
            """)
    rows = cursor.fetchall()
    conn.close()
    return rows
    

def customer_communication_history(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                SELECT communications.id, customers.name, communications.date,
                communications.type, communications.notes 
                FROM  communications
                JOIN  customers ON communications.customer_id = customers.id
                WHERE communications.customer_id = ?
            """, (customer_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def customer_email_thread(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                SELECT emails.id, customers.name, emails.date,
                emails.subject, emails.body, emails.direction
                FROM  emails
                JOIN  customers ON emails.customer_id = customers.id
                WHERE emails.customer_id = ?
            """, (customer_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    from db import create_table
    from customer import add_customer
    from products import add_product
    from order import add_order
    from comms import add_communication
    from emails import add_email
    from reviews import add_review
    
    create_table()
    
    # add customers
    add_customer("Saad", "saad@gmail.com", "0300", "Berlin")
    add_customer("Ali", "ali@gmail.com", "0311", "Karachi")
    
    # add products
    add_product("iPhone 15", 999, "Electronics")
    add_product("Nike Air Max", 150, "Shoes")
    add_product("Sony Headphones", 250, "Electronics")
    
    # add orders with mixed statuses
    add_order(1, 1, "2024-01-15", "completed")
    add_order(1, 2, "2024-01-16", "returned")
    add_order(2, 1, "2024-01-17", "chargeback")
    add_order(2, 3, "2024-01-18", "cancelled")
    add_order(1, 1, "2024-01-19", "returned")
    
    # add communications
    add_communication(1, "2024-01-15", "complaint", "Product arrived damaged")
    add_communication(1, "2024-01-16", "return_request", "Want to return item")
    
    # add emails
    add_email(1, "2024-01-15", "Order Issue", "My order arrived damaged", "inbound")
    add_email(1, "2024-01-16", "Re: Order Issue", "Refund initiated", "outbound")
    
    # add reviews
    add_review(1, 1, 5, "Amazing product!")
    add_review(1, 2, 2, "Battery drains fast")
    add_review(2, 1, 4, "Great shoes!")
    
    print("\n=== Most Returned Products ===")
    for row in most_returned_products():
        print(f"{row[0]} — {row[1]} returns")
    
    print("\n=== Most Cancelled Products ===")
    for row in most_cancelled_by_product():
        print(f"{row[0]} — {row[1]} cancellations")
    
    print("\n=== Chargeback Summary ===")
    for row in chargeback_summary():
        print(f"{row[0]} — {row[1]} chargebacks")
    
    print("\n=== Top Selling Products ===")
    for row in top_selling_products():
        print(f"{row[0]} — {row[1]} sales")
    
    print("\n=== Lowest Rated Products ===")
    for row in lowest_rated_products():
        print(f"{row[0]} — avg rating: {row[1]:.1f}")
    
    print("\n=== Customer 1 Communication History ===")
    for row in customer_communication_history(1):
        print(row)
    
    print("\n=== Customer 1 Email Thread ===")
    for row in customer_email_thread(1):
        print(row)