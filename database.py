import sqlite3

# Connect to the database (creates a new file if it doesn't exist)
conn = sqlite3.connect('./Database/database.db')
cursor = conn.cursor()

# Create the authentication table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        files INTEGER DEFAULT 0
    )
''')

# Create the uploaded_files table with a foreign key referencing
# authentication table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS uploaded_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        file_name TEXT NOT NULL,
        file_type TEXT NOT NULL,
        file_path TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES data (id)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")
