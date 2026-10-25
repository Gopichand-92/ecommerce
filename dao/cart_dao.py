import mysql.connector
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chandu@123$$$",
        database="empdb"
    )


def get_cart_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT cart_id FROM cart WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    if result:
        cart_id = result[0]
    else:
        query = "INSERT INTO cart (user_id) VALUES (%s)"
        cursor.execute(query, (user_id,))
        cart_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return cart_id


def get_cart_item(cart_id, product_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT cart_item_id, quantity
        FROM cart_item
        WHERE cart_id = %s AND product_id = %s
    """
    cursor.execute(query, (cart_id, product_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def update_cart_quantity(cart_item_id, quantity):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        UPDATE cart_item
        SET quantity = %s
        WHERE cart_item_id = %s
    """
    cursor.execute(query, (quantity, cart_item_id))
    conn.commit()
    cursor.close()
    conn.close()


def insert_cart_item(cart_id, product_id, quantity):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO cart_item (cart_id, product_id, quantity)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (cart_id, product_id, quantity))
    conn.commit()
    cursor.close()
    conn.close()
