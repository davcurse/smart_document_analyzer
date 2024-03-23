import logging
import sqlite3
import sys
from file import register_user, login_user, file_manage
from database import database_init
from fullclean_db import clear_database


def main():
    db_file = './Database/database.db'

# Clean the database and folders
    if "-c" in sys.argv:
        clear_database(db_file)
        sys.exit()

# Generate new database
    if "-g" in sys.argv:
        # Generate new database for testing
        database_init(db_file)
        sys.exit()

# Clean and generate new database
    if "-r" in sys.argv:
        clear_database(db_file)
        database_init(db_file)
        sys.exit()

# Init main logging
    logging.basicConfig(filename='app.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Main application started.")

# Connect to the SQLite database (creates a new file if it doesn't exist)
    conn = sqlite3.connect('./Database/database.db')
    c = conn.cursor()

# Create a table to store user data if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS data
                 (username TEXT UNIQUE, password TEXT)''')

    while True:
        print("\nSelect an option:")
        print("1. Register a new user")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            register_user(conn, c)
        elif choice == '2':
            user_id = login_user(conn, c)
            if user_id:
                file_manage(user_id, conn, c)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

# Close the database connection
    if 'conn' in globals():
        conn.close()

    logging.info("File application exited.")


if __name__ == '__main__':
    main()
