import sqlite3

conn = sqlite3.connect("orders.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (

    order_id TEXT PRIMARY KEY,

    customer_name TEXT,

    product TEXT,

    status TEXT,

    delivery_date TEXT,

    return_status TEXT,

    refund_status TEXT

)
""")

sample_orders = [

    (
        "24362728",
        "Padmanethra",
        "Dell Laptop",
        "Processing",
        "2026-06-15",
        "None",
        "None"
    ),

    (
        "87654321",
        "John",
        "iPhone 15",
        "Shipped",
        "2026-06-12",
        "None",
        "None"
    ),

    (
        "55555555",
        "Alice",
        "Smart Watch",
        "Delivered",
        "2026-06-01",
        "Requested",
        "Processing"
    )

]

cursor.executemany(
    """
    INSERT OR REPLACE INTO orders
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    sample_orders
)

conn.commit()

conn.close()

print("Orders inserted successfully.")