import mysql.connector
# database logic
def update_user(user_name, new_username):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chandu@123$$$",
        database="empdb"
    )
    cursor = conn.cursor()
    query = "UPDATE Users SET Username = %s WHERE Username = %s"
    cursor.execute(query, (new_username, user_name))
    conn.commit()
    result = cursor.rowcount
    cursor.close()
    conn.close()
    return result


#business logic

def check_user_update(user_name, new_username):
    result = update_user(user_name, new_username)
    update_result = None
    if result == 1:
        update_result = True
    else:
        update_result = False
    return update_result

# def main():
#     result = check_user_update('chandu123', 'chandu')
#     print(result)

# main()
