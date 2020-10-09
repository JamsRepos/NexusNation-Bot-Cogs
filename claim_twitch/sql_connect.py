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
            result = cursor.fetchone()
            if result[0] != None:
                return result[0]
            else:
                return 0
    except Error as e:
        print("Error while connecting to MySQL", e)