import mysql.connector
from mysql.connector import Error
import credutil

# SQL Start
def connect():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=credutil.db_addr,
            user=credutil.db_user,
            passwd=credutil.db_pass,
            database=credutil.db_binid
       )
        print("[INFO] MySQL Database connection successful")
    except Error as err:
        print(f"[ERROR] '{err}'")

    return connection

def read(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def update(connection, command):
    cursor = connection.cursor()
    cursor.execute(command)
    connection.commit()
