import mysql.connector
# database logic
def delete_user(user_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chandu@123$$$",
        database="empdb"
    )
    cursor = conn.cursor()
    query = "DELETE FROM Users WHERE Username = %s"
    cursor.execute(query, (user_name,))
    conn.commit()
    result = cursor.rowcount
    cursor.close()
    conn.close()
    return result

#business logic

def check_user_deletion(user_name):
    result = delete_user(user_name)
    deletion_result = None
    if result == 1:
        deletion_result = True
    else:
        deletion_result = False
    return deletion_result
