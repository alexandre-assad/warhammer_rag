
import os
from dotenv import load_dotenv
import google.generativeai as genai
import sqlite3

from infra.databases.database import execute_select

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

DICTIONARY_PATH = './database/doc/SQL_AGENT_DATA_DICTIONARY.md'

def generate_sql(query: str) -> dict:
    try:

        with open(DICTIONARY_PATH, "r", encoding="utf-8") as f:
            schema = f.read()
       
        sql_prompt = f"""You're an SQLite expert.
Here's the schema of my database :
{schema}

Translate this human query into a SQL Query : "{query}"
Return ONLY the SQL Query. No further explanation, no markdown span ```sql."""

        model = genai.GenerativeModel(model_name="gemini-3.5-flash")
        response = model.generate_content(sql_prompt)
        
        sql_query = response.text.strip().replace("```sql", "").replace("```", "").strip()
        print(f"Requête SQL générée : {sql_query}")
        
        rows = execute_select(sql_query)
        print(rows)
        
        if not rows:
            return {"sql_rows": ["No results from SQL Query."]}
            
        return {"sql_rows": rows}
        
    except Exception as e:
        print(f"Error in the SQL execution : {e}")
        return {"sql_rows": []}