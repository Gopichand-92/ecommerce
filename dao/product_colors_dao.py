import mysql.connector


def get_colors(product_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chandu@123$$$",
        database="empdb"
    )

    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT c.color_name
        FROM product_color pc
        JOIN color c
            ON pc.color_id = c.color_id
        WHERE pc.product_id = %s
    """

    cursor.execute(query, (product_id,))
    colors = cursor.fetchall()

    cursor.close()
    conn.close()

    return colors
