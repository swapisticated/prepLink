import mysql.connector as mc
import os

class MysqlLink:
    def __init__(self):
        self.connection = None
        self.database = "freedb_PL_database"
        self.connect_to_database()

    def connect_to_database(self):
        try:
            self.connection = mc.connect(
                user="freedb_swapisticated",
                password="4s@vjSxtm78yfz*",
                host="sql.freedb.tech",
                port=3306,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connected to the FreeDB database!")
        except mc.Error as e:
            print(f"Error connecting to the database: {e}")
            self.connection = None


    def table_creation(self):
        if self.connection:
            try:
                cursor = self.connection.cursor()  # Create cursor here
                # Create members table if it doesn't exist
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
                cursor.close()  # Close cursor after use
            except mc.Error as e:
                print(f"Error executing table creation query: {e}")

    def close_connection(self):
        if self.connection:
            if self.connection.is_connected():
                self.connection.close()
                print("Database connection closed.")
            else:
                print("Connection already closed.")





