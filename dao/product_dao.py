import mysql.connector


def get_products_with_offers(
    search_text,
    category_name,
    max_price
):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chandu@123$$$",
        database="empdb"
    )

    cursor = conn.cursor()

    query = """
        SELECT
            p.product_id,
            p.product_name,
            p.product_price,
            p.product_description,
            p.product_image,
            ot.offer_type,
            o.discount_percentage

        FROM products p

        JOIN category c
            ON p.category_id = c.category_id

        LEFT JOIN offer o
            ON p.product_id = o.product_id

        LEFT JOIN offer_type ot
            ON ot.id = o.offer_type_id

        WHERE p.product_price <= %s
    """

    params = [max_price]

    # Natural-language product search
    if search_text:

        query += """
            AND (
                p.product_name LIKE %s
                OR p.product_description LIKE %s
            )
        """

        search_value = "%" + search_text + "%"

        params.append(search_value)
        params.append(search_value)

    # Category button search
    if category_name:

        query += """
            AND c.category_name = %s
        """

        params.append(category_name)

    query += """
        ORDER BY p.product_id
    """

    cursor.execute(
        query,
        tuple(params)
    )

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result