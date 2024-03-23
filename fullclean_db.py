import sqlite3
import os
import logging


# Delete single selected file
def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    else:
        print(f"File '{file_path}' does not exist.")


# Delete all files in folder
def delete_all_files(folder_path):
    try:
        # Get a list of files in the folder
        files = os.listdir(folder_path)

        # Iterate over each file and delete it
        for file in files:
            file_path = os.path.join(folder_path, file)

            # Check if it's a file (not a directory)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")

        print("All files deleted successfully.")

    except OSError as error:
        print(f"Error deleting files: {error}")


# Clear database and delete all uploaded files
def clear_database(db_file):

    # Logging init
    logging.basicConfig(filename='app.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Fullclean application started.")

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
        delete_all_files("./uploaded_files")
        print("Database cleared successfully.")
    else:
        print("Aborting full clean.")

    # Commit the changes and close the connection end the logging
    conn.commit()
    conn.close()
    logging.info("Fullclean application exited.")
