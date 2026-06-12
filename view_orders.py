import sqlite3

conn = sqlite3.connect("orders.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM orders")

orders = cursor.fetchall()

print("\n===== ORDERS DATABASE =====\n")

for order in orders:

    print(f"Order ID      : {order[0]}")
    print(f"Customer Name : {order[1]}")
    print(f"Product       : {order[2]}")
    print(f"Status        : {order[3]}")
    print(f"Delivery Date : {order[4]}")
    print(f"Return Status : {order[5]}")
    print(f"Refund Status : {order[6]}")
    print("-" * 40)

conn.close()