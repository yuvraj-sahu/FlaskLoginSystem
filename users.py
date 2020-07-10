import sqlite3
from passlib.hash import pbkdf2_sha256

table_name = 'users'

# Helpful Functions
# These functions are not intended to be used by app.py.

def connect():
    connection = sqlite3.connect('users_database.db')
    cursor = connection.cursor()
    return connection, cursor

# Once the table has been created once, this function does not need to be called
# again in check_user and add_user (so you can remove it from these functions
# after this function has been called once).
def create_table(connection, cursor):
    cursor.execute(f"""create table if not exists {table_name}(
        "username" Text,
        "password" Text
    )""")
    connection.commit()

class Status:
    def __init__(self, is_successful, message):
        self.is_successful = is_successful
        self.message = message

    def __bool__(self):
        return self.is_successful

class StatusConstants:
    successful = Status(True, "")
    username_taken = Status(False, "This username has been taken.")
    user_not_found = Status(False, "The username and password do not match.")

def check_user(username, password):
    connection, cursor = connect()
    create_table(connection, cursor)

    result = cursor.execute(
    f"select * from {table_name} where username=?",
    [username]
    ).fetchall()

    connection.close()

    if not result:
        return StatusConstants.user_not_found

    db_password = result[0][1]
    if pbkdf2_sha256.verify(password, db_password):
        return StatusConstants.successful

    return StatusConstants.user_not_found

def add_user(username, password):
    connection, cursor = connect()
    create_table(connection, cursor)

    result = cursor.execute(
    f"select * from {table_name} where username=?",
    [username]
    ).fetchall()

    if result:
        connection.close()
        return StatusConstants.username_taken

    hashed_password = pbkdf2_sha256.hash(password)
    cursor.execute(
    f"insert into {table_name}(username, password) values(?, ?)",
    [username, hashed_password]
    )

    connection.commit()
    connection.close()

    return StatusConstants.successful

# This function just deletes the user based on their username (without checking
# for the password as well)
def delete_user(username):
    connection, cursor = connect()

    cursor.execute(
    f"delete from {table_name} where username=?",
    [username]
    )

    connection.commit()
    connection.close()
