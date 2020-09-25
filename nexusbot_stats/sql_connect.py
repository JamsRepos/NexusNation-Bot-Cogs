import mysql.connector
from mysql.connector import Error

def connect(db, query):
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