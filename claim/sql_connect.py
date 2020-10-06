import mysql.connector
from mysql.connector import Error

def write(db, query):
    try:
        connection = mysql.connector.connect(
        host='localhost',
        database=db,
        user='webserver',
        password='')
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)

def read(db, query):
    try:
        connection = mysql.connector.connect(
        host='localhost',
        database=db,
        user='webserver',
        password='')
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            return cursor.fetchone()
    except Error as e:
        print("Error while connecting to MySQL", e)