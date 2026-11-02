from database import get_connection

def add_store():
    print("\n--- Add New Store Branch ---")
    branch_name = input("Enter branch name: ").strip()
    location = input("Enter location: ").strip()
    contact_number = input("Enter contact number: ").strip()

    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()

    try:
        query = "INSERT INTO stores (branch_name, location, contact_number) VALUES (?,?,?)"
        cursor.execute(query, (branch_name, location, contact_number))
        conn.commit()
        print(f"Store Branch {branch_name} added successfully.")
    except Exception as e:
        print(f"Error adding this store branch: {e}")
    finally:
        cursor.close()
        conn.close()

def view_stores():
    print("--- Store Branches ---")
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()

    cursor.execute("SELECT store_id, branch_name, location, contact_number FROM stores")
    stores = cursor.fetchall()

    if not stores:
        print("No store branches found.")
    else:
        print(f"{'ID':<5} | {'Branch Name':<20} | {'Location':<25} | {'Contact':<15} |")
        print("-"*75)
        for s in stores:
            print(f"{s['store_id']:<5} | {s['branch_name']:<20} | {s['location']:<25} | {s['contact_number']:<15} |")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    while True:
        print("\n=== STORES MANAGEMENT MODULE ===")
        print("1. ADD STORE BRANCH")
        print("2. VIEW STORE BRANCHES")
        print("3. EXIT")

        ch = int(input("Enter choice: "))
        if ch == 1:
            add_store()
        elif ch == 2:
            view_stores()
        elif ch == 3:
            print("Exiting stores module.")
            break
        else:
            print("INVALID choice! Exiting...")
            break

