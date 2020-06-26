import sqlite3

connection, cursor = None, None

def connect():
    connection = sqlite3.connect('users_database.db')
    cursor = connection.cursor()

def disconnect():
    connection.close()
    connection, cursor = None, None

# TODO: implement these methods

def check_user(username, password):
    pass

def add_user(username, password):
    pass
