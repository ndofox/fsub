# database.py
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                username VARCHAR(255),
                joined_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_subscribed TINYINT DEFAULT 0
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                file_id VARCHAR(255) PRIMARY KEY,
                user_id BIGINT,
                message_id BIGINT,
                upload_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def add_user(self, user_id, username):
        self.cursor.execute("""
            INSERT IGNORE INTO users (user_id, username)
            VALUES (%s, %s)
        """, (user_id, username))
        self.conn.commit()

    def check_subscription(self, user_id):
        self.cursor.execute("SELECT is_subscribed FROM users WHERE user_id = %s", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def update_subscription(self, user_id, status):
        self.cursor.execute("""
            UPDATE users SET is_subscribed = %s WHERE user_id = %s
        """, (status, user_id))
        self.conn.commit()

    def add_file(self, file_id, user_id, message_id):
        self.cursor.execute("""
            INSERT INTO files (file_id, user_id, message_id)
            VALUES (%s, %s, %s)
        """, (file_id, user_id, message_id))
        self.conn.commit()

    def close(self):
        self.conn.close()
