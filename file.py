import sqlite3
from getpass import getpass
import tkinter as tk
from tkinter import filedialog
import os

# Connect to the SQLite database (creates a new file if it doesn't exist)
conn = sqlite3.connect('./Database/database.db')
c = conn.cursor()

# Create a table to store the authentication if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS data
             (username TEXT UNIQUE, password TEXT)''')


def register_user():
    # Prompt user for username
    username = input("Enter a new username: ")

    # check if user exists
    c.execute("SELECT * FROM data WHERE username=?", (username,))
    existing_user = c.fetchone()
    if existing_user:
        print("Username already exists. Choose a different username or login.")
        conn.close()
        exit()

    # Prompt user for password and confirmation
    password = getpass("Enter a password: ")
    confirm_password = getpass("Confirm your password: ")
    if password == confirm_password:
        c.execute("INSERT INTO data (username, password)\
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
    # check if user exists
    c.execute("SELECT * FROM data WHERE username=?", (username,))
    existing_user = c.fetchone()
    if not existing_user:
        print(f"Sorry, the user, '{username}' does not exist.")
        conn.close()
        exit()

    password = getpass("Enter your password: ")
    count = 1
    while existing_user and password != existing_user[2]:
        if count == 5:
            print("Login failed after 5 times.")
            conn.close()
            exit()
        print(f"Invalid password. Try again. Attempt: {count}")
        count += 1
        password = getpass("Enter your password: ")

    print(f"\nWelcome '{username}'.")
    return existing_user[0]  # Return the user ID


def file_manage(user_id):
    while True:
        print("_______________")
        print("\nSelect an option:")
        print("1. View files")
        print("2. Upload a file")
        print("3. Delete a file")
        print("4. Log out")
        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            # View files
            c.execute("SELECT * FROM uploaded_files WHERE user_id=?",
                      (user_id,))
            files = c.fetchall()
            if files:
                print("Your files:")
                for file in files:
                    print(f"ID: {file[0]}, {file[2]}")
            else:
                print("You have no files.")

        elif choice == '2':
            # Upload a file
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            filepath = filedialog.askopenfilename(title="Select a file")
            if filepath:
                filename = os.path.basename(filepath)
                # Extract file extension without the dot
                filetype = os.path.splitext(filename)[1][1:]

                # Find the next available ID
                c.execute("SELECT MAX(id) FROM uploaded_files")
                max_id = c.fetchone()[0]
                next_id = max_id + 1 if max_id else 1

                c.execute(
                    "INSERT INTO uploaded_files "
                    "(user_id, file_name, file_type, file_path) "
                    "VALUES (?, ?, ?, ?)",
                    (next_id, user_id, filename, filetype, filepath)
                )
                c.execute("UPDATE data SET files = files + 1"
                          " WHERE id = ?", (user_id,))
                conn.commit()
                print(f"File '{filename}' uploaded successfully.")
            else:
                print("No file selected.")

        elif choice == '3':
            c.execute("SELECT * FROM uploaded_files WHERE user_id=?",
                      (user_id,))
            files = c.fetchall()
            if files:
                print("Your files:")
                for file in files:
                    print(f"ID: {file[0]}, {file[2]}")
                # Delete a file
                file_id = input("Enter the ID of the file to delete"
                                " (0 to cancel): ")
                if file_id != '0':
                    c.execute(
                        "SELECT * FROM uploaded_files WHERE id=? AND\
                        user_id=?",
                        (file_id, user_id)
                    )
                    file = c.fetchone()
                    if file:
                        c.execute("DELETE FROM uploaded_files WHERE id=?",
                                  (file_id,))
                        c.execute("UPDATE data SET files = files - 1"
                                  " WHERE id = ?", (user_id,))
                        conn.commit()
                        print(f"File '{file[2]}' deleted successfully.")
                    else:
                        print("File not found or you don't have permission "
                              "to delete it.")
                else:
                    print("Deletion cancelled.")
            else:
                print("\nYou have no files to delete.")

        elif choice == '4':
            c.execute("SELECT username FROM data WHERE id = ?",
                      (user_id,))
            username = c.fetchone()[0]
            print(f"'{username}' signed out.")
            conn.close()
            exit()

        else:
            print("Invalid choice. Please try again.")


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
                file_manage(user_id)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

    # Close the database connection
    if conn:
        conn.close()


if __name__ == '__main__':
    main()
