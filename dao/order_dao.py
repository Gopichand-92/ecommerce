
import mysql.connector


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chandu@123$$$",
        database="empdb"
    )


# ==========================================
# GET CHECKOUT ITEMS
# ==========================================

def get_checkout_items(user_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch cart products for checkout
    query = """
        SELECT
            ci.product_id,
            ci.quantity,
            p.product_name,
            p.product_price,
            p.product_image
        FROM cart_item ci
        JOIN products p
        ON ci.product_id = p.product_id
        WHERE ci.user_id = %s
    """

    cursor.execute(query, (user_id,))
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


# ==========================================
# INSERT ORDER
# ==========================================

def insert_order(
    cursor,
    user_id,
    total_amount,
    delivery_address,
    payment_method,
    payment_status
):

    # Insert order information into orders table
    query = """
        INSERT INTO orders (
            user_id,
            total_amount,
            delivery_address,
            payment_method,
            payment_status,
            order_status
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            user_id,
            total_amount,
            delivery_address,
            payment_method,
            payment_status,
            "Placed"
        )
    )

    # Return newly generated order ID
    return cursor.lastrowid


# ==========================================
# INSERT ORDER ITEMS
# ==========================================

def insert_order_item(cursor, order_id, item):

    # Insert each purchased product into order_items
    query = """
        INSERT INTO order_items (
            order_id,
            product_id,
            product_name,
            product_price,
            product_image,
            quantity
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            order_id,
            item["product_id"],
            item["product_name"],
            item["product_price"],
            item["product_image"],
            item["quantity"]
        )
    )


# ==========================================
# DELETE CART ITEMS AFTER ORDER PLACEMENT
# ==========================================

def delete_cart_items(cursor, user_id):

    # Delete purchased products from the user's cart
    query = """
        DELETE FROM cart_item
        WHERE user_id = %s
    """

    cursor.execute(query, (user_id,))


# ==========================================
# GET USER ORDERS
# ==========================================

def get_user_orders(user_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch all orders belonging to the user
    query = """
        SELECT *
        FROM orders
        WHERE user_id = %s
        ORDER BY order_id DESC
    """

    cursor.execute(query, (user_id,))
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


# ==========================================
# GET ORDER DETAILS
# ==========================================

def get_order_details(order_id, user_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch order and purchased product details
    query = """
        SELECT
            o.order_id,
            o.total_amount,
            o.delivery_address,
            o.payment_method,
            o.payment_status,
            o.order_status,
            oi.product_id,
            oi.product_name,
            oi.product_price,
            oi.product_image,
            oi.quantity
        FROM orders o
        JOIN order_items oi
        ON o.order_id = oi.order_id
        WHERE o.order_id = %s
        AND o.user_id = %s
    """

    cursor.execute(query, (order_id, user_id))
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


# ==========================================
# CANCEL ORDER
# ==========================================

def cancel_order(order_id, user_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # Cancel only orders belonging to the user
        # and having the current status 'Placed'
        query = """
            UPDATE orders
            SET order_status = %s
            WHERE order_id = %s
            AND user_id = %s
            AND order_status = %s
        """

        cursor.execute(
            query,
            ("Cancelled", order_id, user_id, "Placed")
        )

        conn.commit()

        # Return affected rows
        return cursor.rowcount

    except Exception:

        conn.rollback()
        raise

    finally:

        cursor.close()
        conn.close()
