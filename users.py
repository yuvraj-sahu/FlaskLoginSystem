import sqlite3

connection, cursor = None, None
table_name = 'users'

# Helpful Functions
# These functions are not intended to be used by app.py.
# Also, these functions assume that a connection has already been established
# with the exception of the connect() function, which establishes a connection.

def connect():
    global connection, cursor
    connection = sqlite3.connect('users_database.db')
    cursor = connection.cursor()

def disconnect():
    global connection, cursor
    connection.close()
    connection, cursor = None, None

# Once the table has been created once, this function does not need to be called
# again in check_user and add_user (so you can remove it from these functions
# after this function has been called once).
def create_table():
    global connection, cursor
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
    global connection, cursor
    connect()
    create_table()

    result = cursor.execute(
    f"select * from {table_name} where username=? and password=?",
    [username, password]
    ).fetchall()

    disconnect()

    if result:
        return StatusConstants.successful
    return StatusConstants.user_not_found

def add_user(username, password):
    global connection, cursor
    connect()
    create_table()

    result = cursor.execute(
    f"select * from {table_name} where username=?",
    [username]
    ).fetchall()

    if result:
        disconnect()
        return StatusConstants.username_taken

    cursor.execute(
    f"insert into {table_name}(username, password) values(?, ?)",
    [username, password]
    )

    connection.commit()
    disconnect()

    return StatusConstants.successful

def delete_user(username, password):
    global connection, cursor
    connect()

    cursor.execute(
    f"delete from {table_name} where username=? and password=?",
    [username, password]
    )

    connection.commit()
    disconnect()
