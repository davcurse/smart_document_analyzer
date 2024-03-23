import sqlite3
from getpass import getpass

# Connect to the SQLite database (creates a new file if it doesn't exist)
conn = sqlite3.connect('./Database/database.db')
c = conn.cursor()

# Create a table to store the authentication if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS authentication
             (username TEXT UNIQUE, password TEXT)''')

# Prompt the user for a username
username = input("Enter your username: ")

# Check if the username already exists in the database
c.execute("SELECT * FROM authentication WHERE username=?", (username,))
existing_user = c.fetchone()

if existing_user:
    # If the username exists, prompt for the password and check if it matches
    password = getpass("Enter your password: ")
    if password == existing_user[2]:
        print(f"Login successful for user '{username}'!")
    else:
        print("Incorrect password. Login failed.")
else:
    # If the username doesn't exist, prompt for a new password
    password = getpass("Enter your password: ")
    c.execute("INSERT INTO authentication (username, password) VALUES (?, ?)",
              (username, password))
    conn.commit()
    print(f"New user '{username}' registered successfully!")

# Close the database connection
conn.close()
