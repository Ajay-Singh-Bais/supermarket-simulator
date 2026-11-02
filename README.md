https://github.com/Ajay-Singh-Bais/supermarket-simulator

# Data-Driven Supermarket Administration System

A modular, command-line interface (CLI) Supermarket Simulator and Point-of-Sale (POS) system built using **Python** and **SQLite**. Designed with professional software engineering practices, including atomic database transactions, session-aware terminal logic, and strict role-based separation of concerns.

---

## 🚀 Key Features

* **Role-Based Access Control (RBAC):** Separated environments for administrative back-office management and day-to-day cashier terminal operations.
* **Store Branch Management:** Multi-branch support allowing operations across different physical store locations.
* **Supplier & Inventory Control:** Comprehensive tracking of product categories, cost/selling prices, stock quantities, and low-stock reorder thresholds.
* **Customer Directory & Loyalty Program:** Customer registration via phone numbers with automated loyalty point calculation based on purchase totals.
* **Session-Aware POS Billing Engine:** 
  * Terminal locking to specific store shifts.
  * Interactive shopping cart creation with live stock availability verification.
  * **Atomic Transactions:** Ensures that stock is instantly deducted and orders/order items are logged safely, with rollbacks on failure.

---

## 🛠️ Project Structure

```text
supermarket_simulator/
├── database.py            # SQLite connection manager & automated schema setup
├── back_office.py         # Administrative console for managers (Stores, Supplies)
├── cashier_terminal.py    # Dedicated POS terminal interface for cashiers
├── billing.py             # POS checkout engine, cart logic, and transaction history
├── customers.py           # Customer registration & loyalty point tracking
├── supplies.py            # Supplier profiles and inventory management
├── stores.py              # Store branch location management
└── supermarket.db         # Local SQLite database (auto-generated)