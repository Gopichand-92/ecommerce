
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
# GET EXISTING CART ITEM
# ==========================================

def get_cart_item(user_id, product_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        query = """
            SELECT cart_item_id, quantity
            FROM cart_item
            WHERE user_id = %s AND product_id = %s
        """

        cursor.execute(query, (user_id, product_id))

        return cursor.fetchone()

    finally:

        cursor.close()
        conn.close()


# ==========================================
# INSERT PRODUCT INTO CART
# ==========================================

def insert_cart_item(user_id, product_id, quantity):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        query = """
            INSERT INTO cart_item (user_id, product_id, quantity)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (user_id, product_id, quantity))

        conn.commit()

    except Exception:

        conn.rollback()
        raise

    finally:

        cursor.close()
        conn.close()


# ==========================================
# UPDATE CART ITEM QUANTITY
# ==========================================

def update_cart_quantity(cart_item_id, quantity):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        query = """
            UPDATE cart_item
            SET quantity = %s
            WHERE cart_item_id = %s
        """

        cursor.execute(query, (quantity, cart_item_id))

        conn.commit()

    except Exception:

        conn.rollback()
        raise

    finally:

        cursor.close()
        conn.close()


# ==========================================
# REMOVE CART ITEM
# ==========================================

def remove_cart_item(cart_item_id, user_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        query = """
            DELETE FROM cart_item
            WHERE cart_item_id = %s AND user_id = %s
        """

        cursor.execute(query, (cart_item_id, user_id))

        conn.commit()

        return cursor.rowcount

    except Exception:

        conn.rollback()
        raise

    finally:

        cursor.close()
        conn.close()


# ==========================================
# GET ALL CART ITEMS FOR A USER
# ==========================================

def get_user_cart(user_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        query = """
            SELECT
                ci.cart_item_id,
                ci.user_id,
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

        return cursor.fetchall()

    finally:

        cursor.close()
        conn.close()
