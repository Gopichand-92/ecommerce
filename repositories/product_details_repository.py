import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chandu@123$$$",
        database="empdb"
    )


def get_product_details(product_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT
                p.product_id AS id,
                p.product_name AS name,
                p.product_price AS price,
                p.product_description AS description,
                p.product_image AS image
            FROM products p
            WHERE p.product_id = %s
        """

        cursor.execute(query, (product_id,))
        return cursor.fetchone()

    finally:
        cursor.close()
        conn.close()


def get_offers(product_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT
                ot.offer_type,
                o.discount_percentage,
                (p.product_price * o.discount_percentage / 100)
                    AS discount_amount
            FROM products p
            JOIN offer o
                ON p.product_id = o.product_id
            JOIN offer_type ot
                ON o.offer_type_id = ot.id
            WHERE p.product_id = %s
        """

        cursor.execute(query, (product_id,))
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def get_colors(product_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT c.color_name
            FROM product_color pc
            JOIN color c
                ON pc.color_id = c.color_id
            WHERE pc.product_id = %s
        """

        cursor.execute(query, (product_id,))
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


# if __name__ == "__main__":
#     result = get_product_details(1)
#     print("Product:", result)
#     print("Offers:", get_offers(1))
#     print("Colors:", get_colors(1))