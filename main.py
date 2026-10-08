
import mysql.connector
import re
import os
from dotenv import load_dotenv


load_dotenv()
try:
    db = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        connection_timeout=5,
        use_pure=True
    )

    print("CONNECTED")

except mysql.connector.Error as err:
    print("MYSQL ERROR:")
    print(err)

cursor = db.cursor()

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+1]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.search(pattern, email))

def validate_username(username):
    pattern = r'^[a-zA-Z0-9_.-]{8,}$'
    return bool(re.search(pattern, username))


# Get user_info


if __name__ == "__main__":
    while True:

        valid_email = False
        valid_username = False

        first_name = input("First name: ")
        last_name = input("Last name: ")

        sql = """
            INSERT INTO USER_INFO(first_name, last_name, status)
            VALUES(%s, %s, %s)
        """

        values = (first_name.title(), last_name.title(), "pending")

        cursor.execute(sql, values)

        db.commit()

        # Get the ID MySQL just created for this user
        user_id = cursor.lastrowid


        while not valid_username:
            print("Username must:")
            print("- Be at least 8 characters")
            print("- Contain only letters, numbers, _, ., or -")

            username = input("Username: ")

            if validate_username(username):
                sql = "SELECT user_id FROM user_info WHERE username = %s"
                values = (username,)

                cursor.execute(sql, values)

                user = cursor.fetchone()

                if user:
                    print("Username is already taken.")
                    valid_username = False
                else:
                    valid_username = True

                    sql = '''
                        UPDATE USER_INFO
                        SET username = %s
                        where user_id = %s 
                    '''

                    values = (username, user_id)
                    cursor.execute(sql, values)

            else:
                valid_username = False


        while not valid_email:
            email = input("Email: ")
            if validate_email(email):
                sql = "SELECT user_id FROM USER_INFO WHERE email = %s"
                values = (email,)

                cursor.execute(sql, values)

                user = cursor.fetchone()
                if user:
                    print(f"{email} is registered with another account")
                    valid_email = False
                else:
                    valid_email = True

                    sql = '''
                            UPDATE USER_INFO
                            SET EMAIL = %s
                            where user_id = %s
                        '''

                    values = (email, user_id)
                    cursor.execute(sql, values)
            else:
                valid_email = False

        sql = '''
                UPDATE USER_INFO
                SET status = %s
                where user_id = %s
              '''
        values = ("active", user_id)

        cursor.execute(sql, values)

        db.commit()

        print("Account created.")

