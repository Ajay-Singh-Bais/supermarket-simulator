from database import get_connection

ACTIVE_STORE_ID = None
ACTIVE_STORE_NAME = ""

def set_active_store():
    global ACTIVE_STORE_ID, ACTIVE_STORE_NAME

    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()

    cursor.execute("SELECT store_id, branch_name, location FROM stores")
    stores = cursor.fetchall()

    if not stores:
        print("\n[ERROR] No stores found...")
        cursor.close()
        conn.close()
        return False

    print("\n--- Select Cashier Store Branch ---")
    for s in stores:
        print(f"[{s['store_id']}] : {s['branch_name']}, {s['location']}")

    while True:
        try:
            ch = int(input("Enter Store ID for today's session: "))
            cursor.execute("SELECT store_id, branch_name FROM stores WHERE store_id = ?", (ch,))
            store = cursor.fetchone()
            if store:
                ACTIVE_STORE_ID = store['store_id']
                ACTIVE_STORE_NAME = store['branch_name']
                print(f"\n[SESSION ACTIVE] Terminal locked to: {ACTIVE_STORE_ID} {ACTIVE_STORE_NAME}")
                break
            else:
                print("INVALID Store id. Please enter a valid store id...")
        except ValueError:
            print("Please enter a valid numeric Store id.")

    cursor.close()
    conn.close()
    return True

def process_checkout():
    global ACTIVE_STORE_ID, ACTIVE_STORE_NAME
    if not ACTIVE_STORE_ID:
        success = set_active_store()
        if not success:
            return

    print(f"\n--- POS Checkout Counter [{ACTIVE_STORE_NAME}] ---")

    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()

    try:
        customer_id = None
        phone_input = input("Enter customer phone number (or press ENTER to skip.): ").strip()
        if phone_input:
            cursor.execute('SELECT customer_id, name, loyalty_pts FROM customers WHERE phone = ?', (phone_input,))
            cust = cursor.fetchone()
            if cust:
                customer_id = cust['customer_id']
                print(f"Customer Found: {cust['name']} (Current points: {cust['loyalty_pts']})")
            else:
                print("Customer not found. Proceeding as Guest")

        cart = []
        grand_total = 0.0

        print("\n--- Add Items to Cart ---")
        while True:
            try:
                product_id = int(input("Enter product id (or 0 to finish cart): "))
                if product_id == 0:
                    break

                cursor.execute("SELECT product_id, product_name, sell_price, stock_qty FROM products WHERE product_id = ?", (product_id,))
                product = cursor.fetchone()

                if not product:
                    print("Product not found. Try again")
                    continue

                print(f"Selected product: {product['product_name']} | Price: {product['sell_price']:.2f} | Available Stock: {product['stock_qty']}")

                quantity = int(input("Enter quantity purchased: "))
                if quantity <= 0:
                    print("QUANTITY MUST BE >=1")
                    continue

                if quantity > product['stock_qty']:
                    print(f"ERROR: Insufficient stock! Only {product['stock_qty']} left...")
                    continue

                item_total = product['sell_price']*quantity
                cart.append(
                    {"product_id": product['product_id'],
                     "product_name": product['product_name'],
                     "unit_price": product['sell_price'],
                     "quantity": quantity,
                     "item_total": item_total}
                )
                grand_total += item_total
                print(f"Added {quantity}X{product['product_name']} to cart. Subtotal: Rs.{grand_total:.2f}")

            except ValueError:
                print("INVALID input. Please enter valid numbers.")

        if not cart:
            print("Checkout calcelled. Cart is empty")
            return

        print("\n==============================================")
        print(f"        BILL [{ACTIVE_STORE_NAME}]        ")
        print("==============================================")
        print(f"{'Item':<18} | {'Qty':<4} | {'Price':<8} | {'Total':<8}")
        print("-"*46)
        for item in cart:
            print(f"{item['product_name']:<18} | {item['quantity']:<4} | Rs.{item['unit_price']:<8} | Rs.{item['item_total']:<7.2f}")
        print("-"*46)
        print(f"GRAND TOTAL: Rs.{grand_total:.2f}")

        confirm = input("Confirm and proceed to payment? (y/n): ").strip()
        if confirm != 'y':
            print("Transaction Cancelled!")
            return

        cursor.execute("""
        INSERT INTO orders(store_id, customer_id, total_amount) VALUES (?,?,?)
        """, (ACTIVE_STORE_ID, customer_id, grand_total,))

        order_id = cursor.lastrowid

        for item in cart:
            cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)""", (order_id, item['product_id'], item['quantity'], item['unit_price'],))

            cursor.execute("""
            UPDATE products
            SET stock_qty = stock_qty - ?
            WHERE product_id = ?""", (item['quantity'], item['product_id'],))

        if customer_id:
            pts_earned = int(grand_total / 10)
            cursor.execute("""
            UPDATE customers
            SET loyalty_pts = loyalty_pts + ?
            WHERE customer_id = ?""", (pts_earned, customer_id,))
            print(f"\nSUCCESS! Awarded {pts_earned} loyalty points to customer.")

        conn.commit()
        print(f"\nTransaction #{order_id} completed successfully.")

    except Exception as e:
        conn.rollback()
        print(f"Transaction failed! Due to error: {e}")
    finally:
        cursor.close()
        conn.close()

def view_order_history():
    print("\n--- Order Transaction History ---")
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()

    cursor.execute("""
    SELECT o.order_id, s.branch_name, c.name as customer_name, o.order_date, o.total_amount
    FROM orders o
    JOIN stores s ON o.store_id = s.store_id
    LEFT JOIN customers c ON o.customer_id = c.customer_id
    ORDER BY o.order_date DESC""")
    orders = cursor.fetchall()

    if not orders:
        print("No transactions yet.")
    else:
        print(f"{'ID':<5} | {'Branch':<15} | {'Customer':<15} | {'Date-Time':<20} | {'Total (Rs)':<10}")
        print("-"*75)
        for o in orders:
            cust = o['customer_name'] if o['customer_name'] else "Guest"
            print(f"{o['order_id']:<5} | {o['branch_name']:<15} | {cust:<15} | {o['order_date']:<20} | Rs.{o['total_amount']:<9.2f}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    if set_active_store():
        while True:
            print(f"\n=== BILLING & POS MODULE [{ACTIVE_STORE_NAME}] ===")
            print("1. Process New Checkout.")
            print("2. View order History")
            print("3. Switch Active Store Branch")
            print("4. Exit")

            ch = int(input("Enter your choice: "))
            if ch == 1:
                process_checkout()
            elif ch == 2:
                view_order_history()
            elif ch == 3:
                set_active_store()
            elif ch == 4:
                print("Exiting...")
                break
            else:
                print("INVALID CHOICE!")
                break
