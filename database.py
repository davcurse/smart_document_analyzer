import sqlite3

# Connect to the database (creates a new file if it doesn't exist)
conn = sqlite3.connect('./Database/database.db')
cursor = conn.cursor()

# Create the authentication table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS authentication (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Create the uploaded_files table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS uploaded_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT NOT NULL,
        file_type TEXT NOT NULL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")
