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
    
    # Get all tables from SQLite (excluding system tables and session tables)
    SKIP_TABLES = {'django_session', 'django_migrations', 'django_content_type', 'auth_permission', 'auth_group', 'auth_group_permissions', 'auth_user_groups', 'auth_user_user_permissions'}
    lite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in lite_cursor.fetchall() if row[0] not in SKIP_TABLES]
    
    print(f"Found {len(tables)} tables to migrate (skipping session/auth tables).")
    
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
        
        import datetime
        from decimal import Decimal

        # Convert values (handling bytes/memoryview/decimal/time/date/etc.)
        processed_rows = []
        for row in rows:
            processed_row = []
            for val in row:
                if isinstance(val, memoryview):
                    processed_row.append(val.tobytes())
                elif isinstance(val, Decimal):
                    processed_row.append(float(val))
                elif isinstance(val, (datetime.time, datetime.date)):
                    processed_row.append(str(val))
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

def migrate_local_to_cloud():
    database_url = read_env("DATABASE_URL")
    if not database_url:
        print("Error: DATABASE_URL not found in .env")
        raise Exception("DATABASE_URL not found")
        
    print("Connecting to Neon Tech PostgreSQL...")
    pg_conn = psycopg2.connect(database_url)
    pg_cursor = pg_conn.cursor()
    
    print(f"Connecting to local SQLite database at {SQLITE_PATH}...")
    lite_conn = sqlite3.connect(str(SQLITE_PATH))
    lite_cursor = lite_conn.cursor()
    
    # Disable foreign key checks in PG for this session
    try:
        pg_cursor.execute("SET session_replication_role = 'replica';")
        pg_cursor.execute("ALTER TABLE devoluciones_devolucion ADD COLUMN IF NOT EXISTS estado_equipo VARCHAR(30) DEFAULT 'excelente';")
        pg_cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventario_movimientokardex (
                id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                tipo_movimiento varchar(20) NOT NULL,
                cantidad integer NOT NULL CHECK (cantidad >= 0),
                stock_anterior integer NOT NULL CHECK (stock_anterior >= 0),
                stock_nuevo integer NOT NULL CHECK (stock_nuevo >= 0),
                usuario_nombre varchar(150) NOT NULL,
                observaciones text NOT NULL,
                creado_en timestamp with time zone NOT NULL,
                producto_id bigint NOT NULL REFERENCES inventario_producto(id) ON DELETE CASCADE
            );
        """)
        pg_conn.commit()
    except Exception as e:
        print(f"Warning: Could not set session_replication_role or prep schema: {e}")
        pg_conn.rollback()

    SKIP_TABLES = {'django_session', 'django_migrations', 'django_content_type', 'auth_permission', 'auth_group', 'auth_group_permissions', 'auth_user_groups', 'auth_user_user_permissions'}
    lite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in lite_cursor.fetchall() if row[0] not in SKIP_TABLES]
    
    print(f"Found {len(tables)} tables to migrate to cloud (skipping session/auth tables).")
    
    for table in tables:
        print(f"Migrating table: {table}...")
        
        try:
            pg_cursor.execute(f'DELETE FROM "{table}";')
        except Exception as e:
            print(f"  Warning: Table {table} delete failed: {e}")
            pg_conn.rollback()
            continue
            
        lite_cursor.execute(f'SELECT * FROM "{table}";')
        columns = [desc[0] for desc in lite_cursor.description]
        rows = lite_cursor.fetchall()
        
        if not rows:
            print(f"  No records to copy.")
            continue
            
        col_names = ", ".join([f'"{col}"' for col in columns])
        placeholders = ", ".join(["%s" for _ in columns])
        insert_query = f'INSERT INTO "{table}" ({col_names}) VALUES ({placeholders});'
        
        try:
            pg_cursor.executemany(insert_query, rows)
            print(f"  Successfully copied {len(rows)} rows.")
        except Exception as e:
            print(f"  Error inserting into {table}: {e}")
            pg_conn.rollback()
            continue
            
    # Reset role
    try:
        pg_cursor.execute("SET session_replication_role = 'origin';")
    except Exception:
        pg_conn.rollback()
        
    pg_conn.commit()
    pg_cursor.close()
    pg_conn.close()
    lite_cursor.close()
    lite_conn.close()
    
    print("\nMigration to cloud finished successfully!")

if __name__ == "__main__":
    migrate()
    