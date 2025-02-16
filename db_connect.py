import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Update this
        password="jasmitha01",  # Update this
        database="webapp"  # Update this
    )
