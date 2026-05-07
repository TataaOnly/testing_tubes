import pytest
import sqlite3
from simrs_test.user import create_user, get_user_by_username, update_user_role

@pytest.fixture(scope='module')
def db_connection():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.commit()
    
    # Monkeypatch the original connection function to use the in-memory database
    original_connect = sqlite3.connect
    sqlite3.connect = lambda db_name: conn
    
    yield conn
    
    # Restore the original connect function
    sqlite3.connect = original_connect
    conn.close()

def test_create_user(db_connection):
    create_user('testuser', 'password123', 'admin', conn=db_connection)
    user = get_user_by_username('testuser', conn=db_connection)
    assert user is not None
    assert user['username'] == 'testuser'
    assert user['role'] == 'admin'

def test_get_user_by_username(db_connection):
    create_user('testuser2', 'password123', 'doctor', conn=db_connection)
    user = get_user_by_username('testuser2', conn=db_connection)
    assert user is not None
    assert user['username'] == 'testuser2'

def test_update_user_role(db_connection):
    create_user('testuser3', 'password123', 'receptionist', conn=db_connection)
    update_user_role('testuser3', 'cashier', conn=db_connection)
    updated_user = get_user_by_username('testuser3', conn=db_connection)
    assert updated_user['role'] == 'cashier'

def test_get_nonexistent_user(db_connection):
    user = get_user_by_username('nonexistent', conn=db_connection)
    assert user is None
