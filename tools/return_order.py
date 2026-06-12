import sqlite3

DB_FILE = "orders.db"

def request_return(order_id):

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status, return_status
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
    return_status = result[1]

    if return_status == "Requested":

        conn.close()

        return {
            "success": False,
            "message": "Return request already exists."
        }

    if status != "Delivered":

        conn.close()

        return {
            "success": False,
            "message": "Return can only be requested after delivery."
        }

    cursor.execute(
        """
        UPDATE orders
        SET return_status = 'Requested'
        WHERE order_id = ?
        """,
        (order_id,)
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Return request submitted successfully."
    }