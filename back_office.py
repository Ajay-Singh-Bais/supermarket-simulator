from database import initialize_database
import supplies
import stores
import billing

def main_menu():
    initialize_database()

    while True:
        print('\n===========================================================================')
        print("     SUPERMARKET SIMULATOR CLI      ")
        print("============================================================================")
        print("1. Manage Store Branches")
        print("2. Manage Suppliers & Inventory")
        print("3. Process Bill Checkout")
        print("4. Exit Simulator.")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            while True:
                print("\n--- Store Branch Menu ---")
                print("1. Add Store Branch")
                print("2. View Store Branches")
                print("3. Back to Main Menu")

                ch = int(input("Enter your choice: "))
                if ch == 1:
                    stores.add_store()
                elif ch == 2:
                    stores.view_stores()
                elif ch == 3:
                    break
                else:
                    print("Invalid choice. Please Enter 1,2,3.")

        elif choice == 2:
            while True:
                print('\n--- Supplies & Inventory Menu ---')
                print("1. Add Supplier\n2. View Suppliers\n3. Add Product\n4. View Inventory\n5. Back to Main Menu")
                ch1 = int(input("Enter your choice: "))
                if ch1 == 1:
                    supplies.add_supplier()
                elif ch1 == 2:
                    supplies.view_suppliers()
                elif ch1 == 3:
                    supplies.add_product()
                elif ch1 == 4:
                    supplies.view_inventory()
                elif ch1 == 5:
                    break
                else:
                    print("Invalid choice. Please enter 1,2,3,4,5")

        elif choice == 3:
            while True:
                print("\n--- Billing Module ---")
                print("First select Store:-")
                billing.set_active_store()
                print("Now POS Checkout will begin.")
                billing.process_checkout()
                end = input("Do you want to end billing for today? (Press Enter to end or 'y' to continue)").strip()
                if end != 'y':
                    break
        
        elif choice == 4:
            print("\nThank you for running Supermarket Simulator. GoodBye!")
            break
        else:
            print("Innvalid choice. Please enter a number between 1 and 3")

if __name__ == "__main__":
    main_menu()

