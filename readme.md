# Smart Document Analyzer

### EC530 Project2
#### David Li

An easy to use command-line based program to store, view, and manipulate documents with secure user authentication and history backtracking.

## Features

- User registration and login functionality
- File upload and management
- Word count for uploaded files (.txt, .doc, .docx, .pdf)
- Logging of user actions and application events
- Database management and file deletion options

## Requirements

- Python 3.x
- SQLite3
- PyPDF2
- python-docx

## Installation

1. Clone the repository
2. Run the application with ```python3.11 main_test.py```
3. Once logged in, you can:
- View uploaded files
- Upload new files
- Delete files
- Log out

4. The application supports the following command-line arguments:
- `-c`: Clean the database and delete all uploaded files
- `-g`: Generate a new database for testing
- `-r`: Clean and generate a new database

## File Structure

- `main_test.py`: The main entry point of the application
- `file.py`: Contains functions for user registration, login, and file management
- `database.py`: Handles database initialization and creation of tables
- `fullclean_db.py`: Provides functions for clearing the database and deleting files
- `Database/database.db`: SQLite database file for storing user information and uploaded files
- `uploaded_files/`: Directory for storing all uploaded files

## Logging

The application logs various events and user actions to the `app.log` file. The log file includes timestamps, log levels, and log messages for tracking and debugging purposes.


## License

This project is licensed under the [MIT License](LICENSE).