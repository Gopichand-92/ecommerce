import mysql.connector
# database logic
def validate_user(user_name,password):
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chandu@123$$$",
    database="empdb"
)
    cursor = conn.cursor()
    query = "select * from Users where Username=%s and Password=%s"
    cursor.execute(query, (user_name ,password))
    result= cursor.fetchone()
    # print(result)
    cursor.close()
    conn.close()
    return result

# business logic 
def check_user_existance(user_name,password):
    result=validate_user(user_name,password)
    login_result=None
    if result==None:
        login_result="Invalid Username/password"
        # print("Invalid Username/password")
    else:
        login_result=" Login successful"
    return login_result

# def main():
#     result=check_user_existance('Ammadu','Suren@4321')
    
# main()