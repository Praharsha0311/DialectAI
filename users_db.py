import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def init_user_db():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.database = DB_NAME
    cursor.execute("""
        CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);

        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
