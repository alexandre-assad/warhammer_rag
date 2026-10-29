import sqlite3

conn = sqlite3.connect('file:database/wahadb.sqlite?mode=ro', uri=True, check_same_thread=False)

def execute_select(query: str, max_rows:int = 10, conn: sqlite3.Connection = conn) -> dict:
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchmany(max_rows)
        columns = [description[0] for description in cursor.description]
        
        return {
            "columns": columns,
            "data": rows
        }
        
    except sqlite3.Error as e:
        return {"error": f"Exec Error SQL : {str(e)}"}
    
