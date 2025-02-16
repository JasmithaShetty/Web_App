import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_database_user_name",  # Update this
        password="your_database_password",  # Update this
        database="your_databse_name"  # Update this
    )
