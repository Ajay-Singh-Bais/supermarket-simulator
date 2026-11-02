from database import get_connection
import os

def add_supplier():
    print("\n--- Add New Supplier ---")
    company = input("Enter company name: ").strip()
    contact = input("Enter contact person: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()
    
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()

    try:
        query = "INSERT INTO suppliers(company_name, contact_person, phone, email) VALUES(?,?,?,?)"
        cursor.execute(query, (company, contact, phone, email))
        conn.commit()
        #(f'[DEBUG] Rows affected: {cursor.rowcount}')
        print(f"Supplier {company} added successfully.")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        cursor.close()
        conn.close()

def view_suppliers():
    print("\n--- Supplier List ---")

    #db_path = os.path.abspath("supermarket.db")
    #print(f"Reading from database at: {db_path}")
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()

    cursor.execute("SELECT supplier_id, company_name, contact_person, phone, email FROM suppliers")
    suppliers = cursor.fetchall()
    #print(f"[DEBUG] Found {len(suppliers)} supplier rows.")

    if not suppliers:
        print("No suppliers found.")
    else:
        print(f"{'ID':<5} | {'Company Name':<20} | {'Contact Person':<15} | {'Phone':<15} | {'Email':<20} |")
        print('-'*89)
        for s in suppliers:
            print(f"{s['supplier_id']:<5} | {s['company_name']:<20} | {s['contact_person']:<15} | {s['phone']:<15} | {s['email']:<20} |")

    cursor.close()
    conn.close()

def add_product():
    print('\n--- Add New Product/ Supply Item ---')
    name = input("Enter product name: ").strip()
    category = input("Enter category: ").strip()
    try:
        cost_price = float(input("Enter cost price: "))
        sell_price = float(input("Enter selling price: "))
        stock_qty = int(input("Enter stock quantity: "))
        reorder_level = int(input("Enter reorder warning level: "))
        supplier_id = int(input("Enter supplier_id for this product: "))
    except ValueError:
        print("Invalid numeric input. Please enter valid numbers for prices and quantities.")
        return 

    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()

    try:
        query = "INSERT INTO products(product_name, category, cost_price, sell_price, stock_qty, reorder_level, supplier_id)\
            VALUES(?,?,?,?,?,?,?)"
        cursor.execute(query, (name, category, cost_price, sell_price, stock_qty, reorder_level, supplier_id))
        conn.commit()
        print(f"Product '{name}' added to inventory successfully.")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        cursor.close()
        conn.close()

def view_inventory():
    print("\n--- Current inventory ---")
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    if not products:
        print("No product found.")
    else:
        print(f"{'ID':<5} | {'Product Name':<20} | {'Category':<15} | {'Price':<8} | {'Stock':<6}")
        print('-'*65)
        for p in products:
            print(f"{p['product_id']:<5} | {p['product_name']:<20} | {p['category']:<15} | {p['sell_price']:<8.2f} | {p['stock_qty']:<6}")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    while True:
        print("\n=== SUPPLIES & INVENTORY MODULE ===")
        print("1. Add Supplier\n2. View Supplier\n3. Add Product\n4. View Inventory\n5. Exit")
        ch = int(input("Enter your choice: "))
        if ch == 1:
            add_supplier()
        elif ch ==2:
            view_suppliers()
        elif ch==3:
            add_product()
        elif ch==4:
            view_inventory()
        elif ch==5:
            print("Exiting Supplies module.")
            break
        else:
            print("Invalid choice. Exiting")
            break
