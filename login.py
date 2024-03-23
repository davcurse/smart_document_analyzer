import sqlite3
import base64
from getpass import getpass

# Connect to the SQLite database (creates a new file if it doesn't exist)
conn = sqlite3.connect('./Database/database.db')
c = conn.cursor()

# Create a table to store the authentication if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS authentication
             (username TEXT UNIQUE, password TEXT)''')


def register_user():
    # Prompt user for username
    username = input("Enter a new username: ")

    # check if user exists
    c.execute("SELECT * FROM authentication WHERE username=?", (username,))
    existing_user = c.fetchone()
    if existing_user:
        print("Username already exists. Choose a different username or login.")
        conn.close()
        exit()

    # Prompt user for password and confirmation
    password = getpass("Enter a password: ")
    confirm_password = getpass("Confirm your password: ")
    if password == confirm_password:
        c.execute("INSERT INTO authentication (username, password)\
                   VALUES (?, ?)",
                  (username, password))
        conn.commit()
        print(f"New user '{username}' registered successfully.")
        print(f"You can now login as '{username}'.")
        conn.close()
        exit()
    else:
        print("Passwords do not match. Registration failed.")
        conn.close()
        exit()


def login_user():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")
    c.execute("SELECT * FROM authentication WHERE username=?", (username,))
    user = c.fetchone()
    if user and password == user[2]:
        print(f"Login successful for user '{username}'.")
        return user[0]  # Return the user ID
    else:
        print("Invalid username or password. Login failed.")
        conn.close()
        exit()


def upload_file(user_id):
    filename = input("Enter the file name: ")
    filetype = input("Enter the file type (e.g., pdf, jpg): ")
    filepath = input("Enter the file path: ")
    with open(filepath, 'rb') as file:
        filedata = file.read()
    c.execute("INSERT INTO files (user_id, filename, filetype, filedata)\
               VALUES (?, ?, ?, ?)",
              (user_id, filename, filetype, base64.b64encode(filedata)))
    conn.commit()
    print(f"File '{filename}' uploaded successfully.")


def main():
    while True:
        print("\nSelect an option:")
        print("1. Register a new user")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            register_user()
        elif choice == '2':
            user_id = login_user()
            if user_id:
                upload_file(user_id)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
            break

    # Close the database connection
    conn.close()


if __name__ == '__main__':
    main()
