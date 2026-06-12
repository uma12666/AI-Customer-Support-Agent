import sqlite3

conn = sqlite3.connect("orders.db")

cursor = conn.cursor()


sample_orders = [
    ("90000001", "Alice", "Samsung S25", "Pending", "2026-06-20", "None", "None"),
    ("90000002", "Bob", "MacBook Air", "Processing", "2026-06-18", "None", "None"),
    ("90000003", "Charlie", "Sony Headphones", "Shipped", "2026-06-15", "None", "None"),
    ("90000004", "David", "iPad Pro", "Delivered", "2026-06-10", "None", "None"),
    ("90000005", "Emma", "Dell XPS 15", "Delivered", "2026-06-08", "Requested", "None"),
    ("90000006", "Frank", "Apple Watch", "Cancelled", "2026-06-12", "None", "None"),
    ("90000007", "Grace", "AirPods Pro", "Delivered", "2026-06-05", "Approved", "Processing"),
    ("90000008", "Henry", "Gaming Mouse", "Shipped", "2026-06-17", "None", "None"),
    ("90000009", "Isabella", "Mechanical Keyboard", "Delivered", "2026-06-03", "Approved", "Completed"),
    ("90000010", "Jack", "Monitor", "Processing", "2026-06-19", "None", "None")
]

cursor.executemany(
    """
    INSERT INTO orders
    (
        order_id,
        customer_name,
        product,
        status,
        delivery_date,
        return_status,
        refund_status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    sample_orders
)

conn.commit()
conn.close()

print("10 orders inserted successfully.")