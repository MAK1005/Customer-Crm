from db import create_table
from customer import add_customer, get_all_customers, get_customer
from products import add_product, get_all_products
from order import add_order, get_orders_by_status, get_order_status
from comms import add_communication, get_communications_by_customer
from emails import add_email, get_emails_by_customer
from reviews import add_review, get_reviews_by_product, get_average_rating
from reports import (most_returned_products, most_cancelled_by_product,
                     chargeback_summary, top_selling_products,
                     lowest_rated_products, customer_communication_history,
                     customer_email_thread)

if __name__ == "__main__":

    # 1. setup
    create_table()
    print("=== Customer CRM ===\n")

    add_customer("sara", "sara@gmail.com", "1556670", "berlin")
    add_customer("Ali","ali@gmail.com", "514890742", "Karachi")
    add_customer("salar", "salar@gmail.com", "45098655", "Peshawer")

    # Saad, Ali, Sara — with email, phone, city

    # 3. add 3 products
    add_product("sony headphones", 200, "electronics")
    add_product("iphone 15", 1200, "electronics")
    add_product("Nike air max", 50, "clothing")

   
    add_order(1, 1, "2024-01-15", "completed")
    add_order(1, 2, "2024-01-16", "returned")
    add_order(2, 1, "2024-01-17", "chargeback")
    add_order(2, 3, "2024-01-18", "cancelled")
    add_order(1, 1, "2024-01-19", "returned")

    # 5. add communications for customer 1
    add_communication(1,"10-11-2025","return", "Broken")


    add_email(1,"15-10-2026", "Cancelled order", "Why was it cancelled", "outbound")
    add_email(1,"10-11-2026", "late order", "Why late", "inbound")# one inbound, one outbound

    add_review(1,2,5,"Amazing")
    add_review(1,4,4,"outstanding service")
    add_review(3,3,1,"late shipment")
    # at least 3 reviews across 2 products

    # 8. print all customers
    print("\n=== All Customers ===")
    # printing customers
    for row in get_all_customers():
        print(f"ID:{row[0]}  {row[1]}  {row[2]}  {row[4]}")

    # 9. print all products
    print("\n=== All Products ===")
    # printing customers
    for row in get_all_products():
        print(f"ID:{row[0]}  {row[1]}  {row[2]} ")

    print("\ncompleted orders")
    for row in get_orders_by_status("completed"):
        print(row)

    print("\n--- Most Returned Products ---")
    for row in most_returned_products():
        print(f"{row[0]} — {row[1]} returns")

    print("\n--- Most Cancelled Products ---")
    for row in most_cancelled_by_product():
        print(f"{row[0]} — {row[1]} cancellations")

    print("\n--- Chargeback Summary ---")
    for row in chargeback_summary():
        print(f"{row[0]} — {row[1]} chargebacks")

    print("\n--- Top Selling Products ---")
    for row in top_selling_products():
        print(f"{row[0]} — {row[1]} sales")

    print("\n--- Lowest Rated Products ---")
    for row in lowest_rated_products():
        print(f"{row[0]} — avg rating: {row[1]:.1f}")

    print("\n--- Customer 1 Communication History ---")
    for row in customer_communication_history(1):
        print(row)

    print("\n--- Customer 1 Email Thread ---")
    for row in customer_email_thread(1):
        print(row)