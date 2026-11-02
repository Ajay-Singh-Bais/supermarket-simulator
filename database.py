import sqlite3

def get_connection():
    try:
        conn = sqlite3.connect('supermarket.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to Sqlite3 Database: {e}")
        return None

def initialize_database():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    #Suppliers table
    cursor.execute("""CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    contact_person TEXT,
    phone TEXT,email TEXT);
    """)
    #Products table
    cursor.execute("""CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    cost_price REAL NOT NULL,
    sell_price REAL NOT NULL,
    stock_qty INTEGER DEFAULT 0,
    reorder_level INTEGER DEFAULT 10,
    supplier_id INTEGER,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id) ON DELETE SET NULL);
    """)
    #Stores table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stores(
    store_id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_name TEXT NOT NULL,
    location TEXT NOT NULL,
    contact_number TEXT);
    """)
    #Customers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers(
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    loyalty_pts INTEGER DEFAULT 0);
    """)
    #Orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id INTEGER NOT NULL,
    customer_id INTEGER,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL NOT NULL,
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id));
    """)
    #Order_Items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items(
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id));
    """)
    conn.commit()
    cursor.close()
    print("Database and tables initialized successfully.")

if __name__ == "__main__":
    initialize_database()