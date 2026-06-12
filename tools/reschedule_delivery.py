import sqlite3

DB_FILE = "orders.db"


def reschedule_delivery(order_id, new_date):

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

    status = result[0]

    # Business Rules

    if status == "Delivered":

        conn.close()

        return {
            "success": False,
            "message": "Delivery cannot be rescheduled because the order has already been delivered."
        }

    if status == "Cancelled":

        conn.close()

        return {
            "success": False,
            "message": "Delivery cannot be rescheduled because the order is cancelled."
        }

    cursor.execute(
        """
        UPDATE orders
        SET delivery_date = ?
        WHERE order_id = ?
        """,
        (new_date, order_id)
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": f"Delivery has been rescheduled to {new_date}."
    }