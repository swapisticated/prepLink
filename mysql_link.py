import mysql.connector as mc
import os

class MysqlLink:
    def __init__(self):
        self.connection = None
        self.database = os.getenv("MYSQLDATABASE")  # Use env variable for database name
        self.connect_to_database()

    def connect_to_database(self):
        try:
            self.connection = mc.connect(
                user=os.getenv("MYSQLUSER"),
                password=os.getenv("MYSQLPASSWORD"),
                host=os.getenv("MYSQLHOST"),
                port=int(os.getenv("MYSQLPORT", 3306)),  # default to 3306 if not set
                database=self.database
            )
            if self.connection.is_connected():
                print("Connected to Railway MySQL database!")
        except mc.Error as e:
            print(f"Error connecting to the database: {e}")
            self.connection = None

    def table_creation(self):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                # Ensure the database and table exist
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
                cursor.execute(f"USE {self.database}")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS members (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100),
                        age INT,
                        gender VARCHAR(10),
                        membership_duration VARCHAR(50),
                        paid_fee INT,
                        phone_number VARCHAR(15)
                    );
                """)
                print("Table created successfully or already exists.")
                cursor.close()
            except mc.Error as e:
                print(f"Error executing table creation query: {e}")

    def close_connection(self):
        if self.connection:
            if self.connection.is_connected():
                self.connection.close()
                print("Database connection closed.")
            else:
                print("Connection already closed.")
