import os
import re
import sqlite3
import psycopg2
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
SQLITE_PATH = BASE_DIR / "db.sqlite3"

def read_env(clave: str, default: str = "") -> str:
    if not ENV_PATH.exists():
        return default
    contenido = ENV_PATH.read_text(encoding="utf-8")
    patron = re.compile(rf"^{re.escape(clave)}\s*=\s*(.+)$", re.MULTILINE)
    match = patron.search(contenido)
    return match.group(1).strip() if match else default

def migrate():
    database_url = read_env("DATABASE_URL")
    if not database_url:
        print("Error: DATABASE_URL not found in .env")
        return
        
    print("Connecting to Neon Tech PostgreSQL...")
    pg_conn = psycopg2.connect(database_url)
    pg_cursor = pg_conn.cursor()
    
    print(f"Connecting to local SQLite database at {SQLITE_PATH}...")
    lite_conn = sqlite3.connect(str(SQLITE_PATH))
    lite_cursor = lite_conn.cursor()
    
    # Disable foreign key checks in SQLite
    lite_cursor.execute("PRAGMA foreign_keys = OFF;")
    lite_conn.commit()
    
    # Get all tables from SQLite (excluding system tables)
    lite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in lite_cursor.fetchall()]
    
    print(f"Found {len(tables)} tables to migrate.")
    
    for table in tables:
        print(f"Migrating table: {table}...")
        
        # 1. Clear local table
        lite_cursor.execute(f"DELETE FROM \"{table}\";")
        
        # 2. Get column names and records from PostgreSQL
        try:
            pg_cursor.execute(f"SELECT * FROM \"{table}\";")
        except Exception as e:
            print(f"  Warning: Table {table} does not exist in PostgreSQL or failed to read: {e}")
            pg_conn.rollback()
            continue
            
        columns = [desc[0] for desc in pg_cursor.description]
        rows = pg_cursor.fetchall()
        
        if not rows:
            print(f"  No records to copy.")
            lite_conn.commit()
            continue
            
        # 3. Build insert query
        col_names = ", ".join([f'"{col}"' for col in columns])
        placeholders = ", ".join(["?" for _ in columns])
        insert_query = f"INSERT INTO \"{table}\" ({col_names}) VALUES ({placeholders});"
        
        from decimal import Decimal

        # Convert values (handling bytes/memoryview/decimal/etc.)
        processed_rows = []
        for row in rows:
            processed_row = []
            for val in row:
                if isinstance(val, memoryview):
                    processed_row.append(val.tobytes())
                elif isinstance(val, Decimal):
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            processed_rows.append(processed_row)
            
        # 4. Bulk insert into SQLite
        try:
            lite_cursor.executemany(insert_query, processed_rows)
            print(f"  Successfully copied {len(rows)} rows.")
        except Exception as e:
            print(f"  Error inserting into {table}: {e}")
            # Try row by row for debugging if bulk fails
            for idx, r in enumerate(processed_rows):
                try:
                    lite_cursor.execute(insert_query, r)
                except Exception as row_error:
                    print(f"    Failed at row {idx}: {row_error}")
                    print(f"    Row data: {r}")
                    break
            
        lite_conn.commit()
        
    # Re-enable foreign key checks
    lite_cursor.execute("PRAGMA foreign_keys = ON;")
    lite_conn.commit()
    
    # Close connections
    pg_cursor.close()
    pg_conn.close()
    lite_cursor.close()
    lite_conn.close()
    
    print("\nMigration finished successfully!")

if __name__ == "__main__":
    migrate()
