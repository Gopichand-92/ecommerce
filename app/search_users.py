import mysql.connector
# database logic
def search_users(username):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chandu@123$$$",
        database="empdb"
    )
    cursor = conn.cursor()
    query = " SELECT id, Username, Email FROM Users WHERE Username LIKE CONCAT('%', %s, '%') "
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result