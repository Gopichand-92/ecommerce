import mysql.connector
def search_products(category_name, max_price):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chandu@123$$$",
        database="empdb"
    )

    cursor = conn.cursor()
    query = """SELECT p.product_id, p.product_name, p.product_price, p.product_description, p.product_image 
    FROM products p JOIN category c ON p.category_id = c.category_id 
    WHERE c.category_name = %s AND p.product_price <= %s"""

    cursor.execute(query, (category_name, max_price))

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

