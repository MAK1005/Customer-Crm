from db import get_connection

def add_email(customer_id, date, subject, body, direction):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO emails (customer_id,date,subject,body,direction) VALUES (?,?,?,?,?)",(customer_id, date, subject, body, direction,))
    conn.commit()
    conn.close()
    # INSERT into emails
    # direction: inbound / outbound

def get_emails_by_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                SELECT emails.id, customers.name, emails.date, emails.subject, emails.body, emails.direction
                FROM emails
                JOIN  customers ON emails.customer_id = customers.id
                WHERE emails.customer_id = ?
""", (customer_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    from db import create_table
    from customer import add_customer
    create_table()
    
    add_customer("Saad", "saad@gmail.com", "0300", "Berlin")
    
    add_email(1, "2024-01-15", "Order Issue", "My order arrived damaged", "inbound")
    add_email(1, "2024-01-16", "Re: Order Issue", "We are sorry, refund initiated", "outbound")
    
    print(get_emails_by_customer(1))