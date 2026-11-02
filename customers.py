from database import get_connection

def add_customer():
    print('\n--- Register new Customer ---')
    name = input("Enter name of customer: ").strip()
    phone = input("Enter phone number: ").strip()

    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()

    try:
        query = "INSERT INTO customers(name, phone, loyalty_pts) VALUES (?,?,0)"
        cursor.execute(query, (name, phone))
        conn.commit()
        print(f"Customer '{name}' registered successfully")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        cursor.close()
        conn.close()

def view_customers():
    print("\n--- Customers Directory ---")
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()

    cursor.execute("SELECT customer_id, name, phone, loyalty_pts FROM customers")
    customers = cursor.fetchall()

    if not customers:
        print("No customers found!")
    else:
        print(f"{'ID':<5} | {'Customer Name':<20} | {'Phone':<15} | {'Loyalty Points':<15} |")
        print('-'*65)
        for c in customers:
            print(f"{c['customer_id']:<5} | {c['name']:<20} | {c['phone']:<15} | {c['loyalty_pts']:<15} |")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    while True:
        print("\n=== CUSTOMER MANAGEMENT MODULE ===")
        print("1. Register Customer")
        print("2. View Customer")
        print("3. Exit")
        ch = int(input("Enter your choice: "))
        if ch == 1:
            add_customer()
        elif ch == 2:
            view_customers()
        elif ch == 3:
            break
        else:
            print("INVALID")
            continue
