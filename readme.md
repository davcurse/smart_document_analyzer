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
2. Run the application with ```python3.11 test_main.py``` or python3.x version of your choice
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

- `test_main.py`: The main entry point of the application
- `file.py`: Contains functions for user registration, login, and file management
- `database.py`: Handles database initialization and creation of tables
- `fullclean_db.py`: Provides functions for clearing the database and deleting files
- `Database/database.db`: SQLite database file for storing user information and uploaded files
- `uploaded_files/`: Directory for storing all uploaded files

## Logging

The application logs various events and user actions to the `app.log` file. The log file includes timestamps, log levels, and log messages for tracking and debugging purposes.

## Example Use
<p align="center">
<img src="./images/2.png" width="80%">
</p>
<p align="center">
Cleaning and generating new database.
</p>
<p align="center">
<img src="./images/1.png" width="80%">
</p>
<p align="center">
Registration Prompt.
</p>
<p align="center">
<img src="./images/3.png" width="80%">
</p>
<p align="center">
Successful login and file manage options.
</p>
<p align="center">
<img src="./images/4.png" width="80%">
</p>
<p align="center">
Viewing files. (Textbooks have large word counts!)
</p>
<p align="center">
<img src="./images/5.png" width="80%">
</p>
<p align="center">
Deleting file clears it from the database for the logged in user and removes from stored directory.
</p>


## License

This project is licensed under the [MIT License](LICENSE).
