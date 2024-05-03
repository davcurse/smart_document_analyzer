import logging
import sqlite3
import sys
# import pytest
from file import register_user, login_user, file_manage
from database import database_init
from fullclean_db import clear_database


db_file = './Database/database.db'


def main(db_file):
    # Clean the database and folders
    if "-c" in sys.argv:
        clear_database(db_file)
        sys.exit()

    # Generate new database
    if "-g" in sys.argv:
        database_init(db_file)
        sys.exit()

    # Clean and generate new database
    if "-r" in sys.argv:
        clear_database(db_file)
        database_init(db_file)
        sys.exit()

    if len(sys.argv) < 2:
        usage_msg = (
            "usage: smartdoc.py\n [-a=run program]\n [-c=clear database]\n "
            "[-g=generate database]\n [-r=clean and generate database]\n\n "
            "Make sure to generate database before clearing or running\
 program.\n"
        )
        sys.exit(usage_msg)

    if "-a" in sys.argv:
        logging.basicConfig(
            filename='app.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("Main application started.")

        conn = sqlite3.connect('./Database/database.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS data
                     (username TEXT UNIQUE, password TEXT)''')

        while True:
            print("\nSelect an option:")
            print("1. Register a new user")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice (1-3): ")
            if choice == '1':
                register_user(conn, c, 'INPUT', 'INPUT')
            elif choice == '2':
                user_id = login_user(conn, c, 'INPUT', 'INPUT')
                if user_id:
                    file_manage(user_id, conn, c)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

        if 'conn' in locals():
            conn.close()

        logging.info("File application exited.")


main(db_file)
