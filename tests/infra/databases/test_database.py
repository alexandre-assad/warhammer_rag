import pytest
import sqlite3
from infra.databases.database import execute_select

@pytest.fixture
def db_connection():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE users (id INTEGER, nom TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob')")
    conn.commit()
    
    yield conn
    conn.close()

def test_execute_select_valid(db_connection):
    query = "SELECT * FROM users"
    result = execute_select(query, conn=db_connection)
    
    assert "error" not in result
    assert result["columns"] == ["id", "nom"]
    assert len(result["data"]) == 2
    assert result["data"][0] == (1, 'Alice')

def test_execute_select_error(db_connection):
    query = "SELECT * FROM table_fantome"
    result = execute_select(query, conn=db_connection)
    
    assert "error" in result
    assert "Exec Error SQL " in result["error"]