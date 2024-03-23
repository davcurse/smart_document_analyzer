import sqlite3
import os


def clear_database(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Get the list of table names in the database
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in c.fetchall()]

    verify = input("Are you sure you want to clean the database? (y/n) ")
    # Iterate over each table and delete all records
    if verify == 'y':
        for table in tables:
            c.execute(f"DELETE FROM {table}")
            if table != "sqlite_sequence":
                print(f"Cleared table: {table}")
        delete_file("./Database/database.db")
        print("Database cleared successfully.")
    else:
        print("Aborting full clean.")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    else:
        print(f"File '{file_path}' does not exist.")


# Specify the path to your SQLite database file
db_file = './Database/database.db'

# Call the function to clear the database
clear_database(db_file)
