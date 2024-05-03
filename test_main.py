from file import register_user, login_user
import sqlite3
from database import database_init
from fullclean_db import clear_database
import pytest

db_file = './Database/test_database.db'
database_init(db_file)
conn = sqlite3.connect('./Database/test_database.db')
c = conn.cursor()


def test_database_clear(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    clear_database(db_file)
    database_init(db_file)


def register_main():
    conn = sqlite3.connect('./Database/test_database.db')
    c = conn.cursor()

    # Test registering a new user
    username = 'testuser'
    password = 'testpassword'
    register_user(conn, c, username, password)

    # Check if the user was added to the database
    c.execute("SELECT * FROM data WHERE username=?", (username,))
    user = c.fetchone()
    assert user is not None
    assert user[1] == username


def login_main():
    conn = sqlite3.connect('./Database/test_database.db')
    c = conn.cursor()

    # Register a user for testing login
    username = 'testuser'
    password = 'testpassword'
    register_user(conn, c, username, password)

    # Test logging in with correct credentials
    user_id = login_user(conn, c, username, password)
    assert user_id is not None

    # Test logging in with incorrect password
    with pytest.raises(SystemExit):
        login_user(conn, c, username, 'wrongpassword')


def test_exit_register():
    with pytest.raises(SystemExit):
        register_main()


def test_exit_login():
    with pytest.raises(SystemExit):
        login_main()
