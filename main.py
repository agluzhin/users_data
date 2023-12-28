import pymysql

import string
import random

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    charset='utf8mb4',
    database='users',
)

# ===== Creating main table in database =====


def create_table():
    try:
        with connection.cursor() as cursor:
            create_data_query = '''
            CREATE TABLE users_data (
                id INT PRIMARY KEY, 
                login VARCHAR(32) NOT NULL, 
                password VARCHAR(64) NOT NULL, 
                age INT NOT NULL);
            '''
            cursor.execute(create_data_query)
            connection.commit()
    finally:
        connection.close()

# ===== Showing all information in created table =====


def show_users():
    try:
        with connection.cursor() as cursor:
            select_data_query = f'''
            SELECT * FROM users_data;
            '''
            cursor.execute(select_data_query)
            result = cursor.fetchall()
            print('#' * 20)
            for element in result:
                print(element)
            print('#' * 20)
    finally:
        connection.close()

# ===== Adding new user in table =====


def add_user(login, password, age):
    id = ''.join(
        random.choice(string.digits)
        for _ in range(4)
    )
    user = (id, login, password, age)
    try:
        with connection.cursor() as cursor:
            insert_data_query = f'''
            INSERT INTO users_data (id, login, password, age)
            VALUES (%s, %s, %s, %s);
            '''
            cursor.execute(insert_data_query, user)
            connection.commit()
            print('You are successfully signed up!')
    finally:
        connection.close()

# ===== Checking if the user is in the table =====


def check_user(login, password):
    try:
        with connection.cursor() as cursor:
            select_data_query = f'''
            SELECT * FROM users_data WHERE login = %s AND password = %s;
            '''
            cursor.execute(select_data_query, (login, password))
            query_result = cursor.fetchall()

            if len(query_result) == 0:
                print('Access denied. Try to sign up or check personal information.')
            else:
                print('Access allowed!')

    finally:
        connection.close()

# ===== Authorization or registration process =====


def main():
    print('Do you have an account in our system?')
    user_answer = input()
    if user_answer.strip().lower() == 'yes':
        print('Please, sign in to continue.')
        print('Enter your login:')
        login = input()
        print('Enter your password:')
        password = input()
        check_user(login, password)
    else:
        print('Enter your login:')
        login = input()
        print('Enter your password:')
        password = input()
        print('Enter your age:')
        age = int(input())
        add_user(login, password, age)


if __name__ == '__main__':
    main()
