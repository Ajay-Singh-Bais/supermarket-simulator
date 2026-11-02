from database import initialize_database
import billing
import customers

def cashier_cli():
    initialize_database()

    print("\n=========================================================")
    print("     SUPERMARKET POS CASHIER DESK       ")
    print("==========================================================")

    if not billing.set_active_store():
        print("Terminal initialization failed. No stores available.")
        return

    while True:
        print(f"\n--- POS Main Menu ---")
        print("1. Process New Checkout\n2. Register New Customer\n3. View Recent Order History\n" \
        "4. Switch Active Store/Branch\n5.Close Terminal")
        choice = int(input("Enter choice: "))
        if choice == 1:
            billing.process_checkout()
        elif choice == 2:
            customers.add_customer()
        elif choice == 3:
            billing.view_order_history()
        elif choice == 4:
            billing.set_active_store()
        elif choice == 5:
            print("\nClosing POS Terminal. Have a Great Day!")
            break
        else:
            print("Invalid choice! Please enter a valid number between 1 and 5...")


if __name__ == "__main__":
    cashier_cli()