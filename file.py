from getpass import getpass
import tkinter as tk
from tkinter import filedialog
import os
import shutil
import logging
import pypdf
import re
import docx


def register_user(conn, cursor, username, password):
    # Prompt user for username
    if username == 'INPUT':
        username = input("Enter a new username: ")

    # check if user exists
    cursor.execute("SELECT * FROM data WHERE username=?", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        print("Username already exists. Choose a different username or login.")
        conn.close()
        exit(0)

    # Prompt user for password and confirmation
    if password == 'INPUT':
        password = getpass("Enter a password: ")
        confirm_password = getpass("Confirm your password: ")
    else:
        confirm_password = password

    if password == confirm_password:
        cursor.execute("INSERT INTO data (username, password)\
                VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"New user '{username}' registered successfully.")
        print(f"You can now login as '{username}'.")
        logging.info(f"New user '{username}' registered successfully.")
        conn.close()
        exit(0)
    else:
        print("Passwords do not match. Registration failed.")
        conn.close()
        exit(0)


def login_user(conn, cursor, username, password):
    if username == 'INPUT':
        username = input("Enter your username: ")
    # check if user exists
    cursor.execute("SELECT * FROM data WHERE username= ? ", (username,))
    existing_user = cursor.fetchone()
    if not existing_user:
        print(f"Sorry, the user, '{username}' does not exist.")
        conn.close()
        exit(0)

    if password == 'INPUT':
        password = getpass("Enter your password: ")
    count = 1
    while existing_user and password != existing_user[2]:
        if count == 5:
            print("Login failed after 5 times.")
            conn.close()
            exit(0)
        print(f"Invalid password. Try again. Attempt: {count}")
        count += 1
        password = getpass("Enter your password: ")

    print(f"\nWelcome '{username}'.")
    logging.info(f"User '{username}' logged in successfully.")
    return existing_user[0]  # Return the user ID


def count_words(file_path):
    _, extension = os.path.splitext(file_path)
    if extension == '.pdf':
        with open(file_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            num_pages = len(reader.pages)
            text = ""
            for page in range(num_pages):
                text += reader.pages[page].extract_text()
        # Remove non-word characters and split the text into words
        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)
        return word_count
    elif extension == '.txt':
        with open(file_path, 'r') as file:
            content = file.read()
            words = re.findall(r'\b\w+\b', content)
            return len(words)
    elif extension in ['.doc', '.docx']:
        doc = docx.Document(file_path)
        word_count = 0
        for para in doc.paragraphs:
            word_count += len(re.findall(r'\b\w+\b', para.text))
        return word_count
    else:
        return 0


def file_manage(user_id, conn, cursor):
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
            cursor.execute("SELECT * FROM uploaded_files WHERE user_id=?",
                           (user_id,))
            files = cursor.fetchall()
            if files:
                print("Your files:")
                for file in files:
                    print(f"ID: {file[0]}, {file[2]}\n  Word Count: {file[5]}")
            else:
                print("You have no files.")

        elif choice == '2':
            # Upload a file
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            filepath = filedialog.askopenfilename(title="Select a file")
            if filepath:

                # Extract file name and extension
                filename = os.path.basename(filepath)
                filetype = os.path.splitext(filename)[1][1:]

                # Find the next available ID
                cursor.execute("SELECT MAX(id) FROM uploaded_files")
                max_id = cursor.fetchone()[0]
                next_id = max_id + 1 if max_id else 1

                # Create a folder to store the uploaded files
                upload_folder = "uploaded_files"
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                # Copy the uploaded file to the upload folder
                destination_path = os.path.join(upload_folder, filename)
                shutil.copy2(filepath, destination_path)

                # Count number of words in pdf
                word_count = count_words(filepath)

                # Insert uploaded folder into database
                cursor.execute(
                    "INSERT INTO uploaded_files "
                    "(id,user_id,file_name,file_type,file_path,word_count)"
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (next_id, user_id, filename, filetype, filepath,
                     word_count)
                )

                # Increment file count per user
                cursor.execute("UPDATE data SET files = files + 1"
                               " WHERE id = ?", (user_id,))

                conn.commit()
                print(f"File '{filename}' uploaded successfully.")
                logging.info(f"File '{filename}' uploaded successfully.")
            else:
                print("No file selected.")

        elif choice == '3':

            # Print user's files
            cursor.execute("SELECT * FROM uploaded_files WHERE user_id=?",
                           (user_id,))
            files = cursor.fetchall()
            if files:
                print("Your files:")
                for file in files:
                    print(f"ID: {file[0]}, {file[2]}")

                # Ask user which file to delete
                file_id = input("Enter the ID of the file to delete"
                                " (0 to cancel): ")
                if file_id != '0':
                    # Delete file form data base
                    cursor.execute(
                        "SELECT * FROM uploaded_files WHERE id=? AND\
                        user_id=?",
                        (file_id, user_id)
                    )
                    file = cursor.fetchone()
                    if file:
                        cursor.execute("DELETE FROM uploaded_files WHERE id=?",
                                       (file_id,))
                        cursor.execute("UPDATE data SET files = files - 1"
                                       " WHERE id = ?", (user_id,))

                        # Delete file from uploaded_files folder
                        file_path = "./uploaded_files/" + file[2]
                        if os.path.exists(file_path):
                            os.remove(file_path)

                        conn.commit()
                        print(f"File '{file[2]}' deleted successfully.")
                        logging.info(f"File '{file[2]}' deleted successfully.")
                    else:
                        print("File not found or you don't have permission "
                              "to delete it.")
                else:
                    print("Deletion cancelled.")
            else:
                print("\nYou have no files to delete.")

        elif choice == '4':
            cursor.execute("SELECT username FROM data WHERE id = ?",
                           (user_id,))
            username = cursor.fetchone()[0]
            print(f"'{username}' signed out.")
            conn.close()
            exit(0)

        else:
            print("Invalid choice. Please try again.")
