import mysql.connector
# database logic
def create_user(user_name,password,email):
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chandu@123$$$",
    database="empdb"
)
    cursor = conn.cursor()
    query = "INSERT INTO Users (Username, Email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_name, email, password))
    conn.commit()
    result= cursor.rowcount
    # print(result)
    cursor.close()
    conn.close()
    return result

#business logic

def check_user_creation(user_name,password,email):
    result=create_user(user_name,password,email)
    creation_result=None
    if result==1:
        creation_result=True
    else:
        creation_result=False
    return creation_result