import mysql.connector
# database logic
def find_Username_by_email(Email):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chandu@123$$$",
        database="empdb"
    )
    cursor = conn.cursor()
    query = "SELECT Username FROM Users WHERE Email = %s"
    cursor.execute(query, (Email ,))
    result = cursor.fetchone()
    # print(result[0])
    cursor.close()
    conn.close()
    if result is None:
        return None
    else:
        return result[0]



#business logic 

def check_email_existance(Email):
    result=find_Username_by_email(Email)
    if result is None:
        return "Invalid email"
    else:
        return result


# def main():
#     result=check_email_existance('chandu@gmail.com')
#     print(result)
# main()