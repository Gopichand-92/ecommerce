import mysql.connector
# database logic
def get_all_users():
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chandu@123$$$",
    database="empdb"
)
    cursor = conn.cursor()
    query = "SELECT id, Username, Email FROM Users"
    cursor.execute(query)
    result= cursor.fetchall()
    # print(result)
    cursor.close()
    conn.close()
    return result


# business logic 
# def check_users(user_name, email, password):
#     result = get_all_users()
#     if result:
#         return True
#     else:
#         return False


    
# def main():
#     result=check_users('Ammadu','Suren@gmail.com','Suren@4321')
#     print(result)

# main()



