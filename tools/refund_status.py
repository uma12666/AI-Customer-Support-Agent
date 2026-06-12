import sqlite3

DB_FILE = "orders.db"


def get_refund_status(order_id):

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT refund_status
        FROM orders
        WHERE order_id = ?
        """,
        (order_id,)
    )

    result = cursor.fetchone()

    conn.close()

    # Order not found
    if not result:

        return {
            "success": False,
            "message": "Order not found."
        }

    refund_status = result[0]

    # Better customer-friendly messages
    if refund_status == "None":

        refund_status = (
            "No refund has been initiated for this order."
        )

    elif refund_status == "Processing":

        refund_status = (
            "Your refund is currently being processed."
        )

    elif refund_status == "Completed":

        refund_status = (
            "Your refund has been completed successfully."
        )

    return {
        "success": True,
        "refund_status": refund_status
    }


# =====================================
# Test
# =====================================
if __name__ == "__main__":

    order_id = "90000007"

    result = get_refund_status(order_id)

    print(result)