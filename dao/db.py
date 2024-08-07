import os
import mysql.connector

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')


def get_connection():
    con = mysql.connector.connect(
        host=host,
        port=db_port,
        user=user,
        password=password,
        database=db_name
    )
    return con
