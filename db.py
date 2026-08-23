import sqlite3

db_file = "project.db"

def get_connection():
    return sqlite3.connect(db_file)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS reviews")
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS emails")
    cursor.execute("DROP TABLE IF EXISTS communications")
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS customers")
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                name             TEXT,
                email            TEXT,
                phone            INTEGER,
                city             TEXT
                )
            """)
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                name             TEXT,
                price            REAL,
                category         TEXT
            )
            """)
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id      INTEGER,
                product_id       INTEGER,
                date             INTEGER,
                status           TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (product_id)  REFERENCES products(id)
            )
            """)
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS communications (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id      INTEGER,
                date             TEXT,
                type             TEXT,
                notes            TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id)   
                )
            """)
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS emails (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id      INTEGER,
                date             TEXT,
                subject          TEXT,
                body             TEXT,
                direction        TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
                )

            """)

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id      INTEGER,
                product_id       INTEGER,
                rating           INTEGER,
                comment          TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (product_id)  REFERENCES products(id)
                )
            """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    print("All tables created successfully")