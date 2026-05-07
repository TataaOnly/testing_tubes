import sys
import os
import sqlite3
import re

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_connection(monkeypatch):
    """Fixture to set up and tear down an in-memory SQLite database."""
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name

    # Apply the schema to the in-memory database
    with open('simrs.sql', 'r') as f:
        sql_script = f.read()
    
    # Filter out MySQL-specific commands
    sql_script = '\n'.join(line for line in sql_script.splitlines() if not line.strip().startswith(('SET', 'FOREIGN_KEY_CHECKS', 'DEFAULT CHARSET', 'START TRANSACTION', 'COMMIT')))
    
    # Replace backticks with double quotes for SQLite compatibility
    sql_script = sql_script.replace('`', '"')
    sql_script = sql_script.replace("\\'", "''")
    
    # Replace enum with TEXT for SQLite compatibility
    sql_script = re.sub(r"enum\([^)]+\)", "TEXT", sql_script, flags=re.IGNORECASE)
    
    # SQLite doesn't support ENGINE=InnoDB...
    sql_script = re.sub(r"\)\s*ENGINE=[^;]+;", ");", sql_script, flags=re.IGNORECASE)
    
    # SQLite doesn't support ALTER TABLE with MODIFY/AUTO_INCREMENT
    sql_script = re.sub(r"ALTER TABLE.*?;\n?", "", sql_script, flags=re.DOTALL | re.IGNORECASE)
    
    # SQLite uses CURRENT_TIMESTAMP without parentheses
    sql_script = re.sub(r"current_timestamp\(\)", "CURRENT_TIMESTAMP", sql_script, flags=re.IGNORECASE)

    conn.executescript(sql_script)
    conn.commit()
    
    class MockMySQLCursor:
        def __init__(self, cursor, dictionary=False):
            self.cursor = cursor
            self.dictionary = dictionary

        def execute(self, query, params=()):
            sqlite_query = query.replace('%s', '?')
            self.cursor.execute(sqlite_query, params)

        def fetchone(self):
            row = self.cursor.fetchone()
            if not row: return None
            if self.dictionary:
                return dict(row)
            return tuple(row)

        def fetchall(self):
            rows = self.cursor.fetchall()
            if self.dictionary:
                return [dict(row) for row in rows]
            return [tuple(row) for row in rows]

        @property
        def lastrowid(self):
            return self.cursor.lastrowid

        def close(self):
            self.cursor.close()

    class MockMySQLConnection:
        def __init__(self, conn):
            self.conn = conn

        def cursor(self, dictionary=False):
            if dictionary:
                self.conn.row_factory = sqlite3.Row
            else:
                self.conn.row_factory = None
            return MockMySQLCursor(self.conn.cursor(), dictionary=dictionary)

        def commit(self):
            self.conn.commit()

        def rollback(self):
            self.conn.rollback()

        def close(self):
            self.conn.close()

        def is_connected(self):
            return True

    mock_conn = MockMySQLConnection(conn)
    
    # Monkeypatch get_db_connection to return the in-memory connection
    monkeypatch.setattr('simrs_core.get_db_connection', lambda: mock_conn, raising=False)
    monkeypatch.setattr('simrs_test.billing.get_db_connection', lambda: mock_conn, raising=False)
    monkeypatch.setattr('app.get_db_connection', lambda: mock_conn, raising=False)
    monkeypatch.setattr('simrs_test.user.get_db_connection', lambda: mock_conn, raising=False)
    monkeypatch.setattr('routes.admin_routes.get_db_connection', lambda: mock_conn, raising=False)
    monkeypatch.setattr('routes.cashier_routes.get_db_connection', lambda: mock_conn, raising=False)
    monkeypatch.setattr('routes.receptionist_routes.get_db_connection', lambda: mock_conn, raising=False)
    monkeypatch.setattr('routes.doctor_routes.get_db_connection', lambda: mock_conn, raising=False)
    monkeypatch.setattr('routes.pharmacist_routes.get_db_connection', lambda: mock_conn, raising=False)

    yield mock_conn
    
    conn.close()
