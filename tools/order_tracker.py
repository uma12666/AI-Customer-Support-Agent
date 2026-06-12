import sqlite3

DB_FILE = "orders.db"


def track_order(order_id):

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM orders
        WHERE order_id = ?
        """,
        (order_id,)
    )

    order = cursor.fetchone()

    conn.close()

    if order:

        return {
            "order_id": order[0],
            "customer_name": order[1],
            "product": order[2],
            "status": order[3],
            "delivery_date": order[4],
            "return_status": order[5],
            "refund_status": order[6]
        }

    return None


if __name__ == "__main__":

    result = track_order("87654321")

    print(result)