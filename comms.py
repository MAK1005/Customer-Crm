from db import get_connection

def add_communication(customer_id, date, type, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO communications (customer_id,date,type,notes) VALUES (?,?,?,?)", (customer_id,date,type,notes,))
    conn.commit()
    conn.close()
    

def get_communications_by_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT communications.id, customers.name, communications.date, 
                      communications.type, communications.notes
                      FROM communications
                      JOIN customers ON communications.customer_id = customers.id
                      WHERE communications.customer_id = ?                      """,(customer_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows
    


if __name__ == "__main__":
    from db import create_table
    from customer import add_customer
    create_table()
    
    add_customer("Saad", "saad@gmail.com", "0300", "Berlin")
    
    add_communication(1, "2024-01-15", "complaint", "Product arrived damaged")
    add_communication(1, "2024-01-16", "return_request", "Want to return damaged item")
    
    print(get_communications_by_customer(1))