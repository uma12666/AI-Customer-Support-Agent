import sqlite3

DB_FILE = "orders.db"


def cancel_order(order_id):

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status
        FROM orders
        WHERE order_id = ?
        """,
        (order_id,)
    )

    result = cursor.fetchone()

    if not result:

        conn.close()

        return {
            "success": False,
            "message": "Order not found."
        }

    current_status = result[0]

    # Business Rules

    if current_status == "Cancelled":

        conn.close()

        return {
            "success": False,
            "message": "Order is already cancelled."
        }

    if current_status in ["Shipped", "Delivered"]:

        conn.close()

        return {
            "success": False,
            "message": f"Order cannot be cancelled because it is {current_status}."
        }

    cursor.execute(
        """
        UPDATE orders
        SET status = 'Cancelled'
        WHERE order_id = ?
        """,
        (order_id,)
    )

    conn.commit()

    conn.close()

    return {
        "success": True,
        "message": "Order cancelled successfully."
    }


if __name__ == "__main__":

    result = cancel_order("24362728")

    print(result)