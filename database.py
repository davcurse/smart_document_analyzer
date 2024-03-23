import sqlite3
import logging


def database_init(database_dir):

    # Logging init
    logging.basicConfig(filename='app.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Database application started.")

    # Connect to the database (creates a new file if it doesn't exist)
    conn = sqlite3.connect(database_dir)
    cursor = conn.cursor()

    # Create the authentication table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            files INTEGER DEFAULT 0
        )
    ''')

    # Create the uploaded_files table with a foreign key referencing
    # authentication table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uploaded_files (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            file_name TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_path TEXT NOT NULL,
            word_count INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES data (id)
        )
    ''')

    # Commit the changes and close the connection and end logging
    conn.commit()
    conn.close()
    print("Database and tables created successfully.")
    logging.info("Database application exited.")
