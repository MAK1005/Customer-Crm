from db import get_connection

def add_review(product_id, customer_id, rating, comment):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (product_id, customer_id, rating, comment) VALUES (?,?,?,?)", (product_id, customer_id, rating, comment))
    conn.commit()
    conn.close()

    # INSERT into reviews
    # rating: 1-5

def get_reviews_by_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                SELECT reviews.id, products.name, customers.name, reviews.rating, reviews.comment
                FROM reviews
                JOIN products ON reviews.product_id = products.id
                JOIN customers ON reviews.customer_id = customers.id
                WHERE reviews.product_id = ?
""", (product_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


    # SELECT with JOIN to get product name and customer name
    # JOIN both customers and products

def get_average_rating(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(rating) FROM reviews WHERE product_id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0]


if __name__ == "__main__":
    from db import create_table
    from customer import add_customer
    from products import add_product
    create_table()
    
    add_customer("Saad", "saad@gmail.com", "0300", "Berlin")
    add_customer("Ali", "ali@gmail.com", "0311", "Karachi")
    add_product("iPhone 15", 999, "Electronics")
    
    add_review(1, 1, 5, "Amazing product!")
    add_review(1, 2, 2, "Battery drains fast")
    
    print(get_reviews_by_product(1))
    print("Average rating:", get_average_rating(1))