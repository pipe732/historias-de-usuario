import sqlite3
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SQLITE_DB_PATH = BASE_DIR / "db.sqlite3"
OUTPUT_SQL_PATH = BASE_DIR / "mine_inventory_dump.sql"

def sqlite_type_to_mysql(col_type: str, col_name: str, is_pk: bool, is_autoinc: bool) -> str:
    type_upper = col_type.upper().strip()
    
    if is_autoinc or (is_pk and ("INT" in type_upper or type_upper == "")):
        mysql_type = "INT NOT NULL AUTO_INCREMENT"
    elif "INT" in type_upper:
        mysql_type = "INT"
    elif "VARCHAR" in type_upper:
        mysql_type = col_type.upper()
    elif "TEXT" in type_upper or type_upper == "":
        mysql_type = "TEXT"
    elif "REAL" in type_upper or "FLOAT" in type_upper or "DOUBLE" in type_upper:
        mysql_type = "DOUBLE"
    elif "DECIMAL" in type_upper or "NUMERIC" in type_upper:
        mysql_type = type_upper
    elif "BOOL" in type_upper or "TINYINT" in type_upper:
        mysql_type = "TINYINT(1)"
    elif "DATETIME" in type_upper or "TIMESTAMP" in type_upper:
        mysql_type = "DATETIME"
    elif "DATE" in type_upper:
        mysql_type = "DATE"
    elif "TIME" in type_upper:
        mysql_type = "TIME"
    elif "BLOB" in type_upper:
        mysql_type = "LONGBLOB"
    else:
        mysql_type = "VARCHAR(255)"
        
    return mysql_type

def escape_sql_value(val):
    if val is None:
        return "NULL"
    elif isinstance(val, bool):
        return "1" if val else "0"
    elif isinstance(val, (int, float)):
        return str(val)
    elif isinstance(val, (bytes, bytearray, memoryview)):
        hex_str = bytes(val).hex()
        return f"X'{hex_str}'"
    else:
        val_str = str(val)
        val_str = val_str.replace("\\", "\\\\")
        val_str = val_str.replace("'", "''")
        val_str = val_str.replace("\0", "\\0")
        val_str = val_str.replace("\r", "\\r")
        val_str = val_str.replace("\n", "\\n")
        return f"'{val_str}'"

def export_sqlite_to_mysql():
    if not SQLITE_DB_PATH.exists():
        print(f"Error: Database file not found at {SQLITE_DB_PATH}")
        return

    print(f"Reading SQLite database: {SQLITE_DB_PATH}")
    conn = sqlite3.connect(str(SQLITE_DB_PATH))
    cursor = conn.cursor()

    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables_master = cursor.fetchall()

    with open(OUTPUT_SQL_PATH, "w", encoding="utf-8") as f:
        f.write("-- ========================================================\n")
        f.write("-- Exported from SQLite to MySQL Workbench (With Foreign Keys)\n")
        f.write("-- Database: mine_inventory\n")
        f.write("-- ========================================================\n\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n")
        f.write("SET NAMES utf8mb4;\n")
        f.write("SET TIME_ZONE = '+00:00';\n\n")
        f.write("CREATE DATABASE IF NOT EXISTS `mine_inventory` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;\n")
        f.write("USE `mine_inventory`;\n\n")

        for table_name, create_sql in tables_master:
            print(f"Processing table: {table_name}")
            
            f.write(f"-- --------------------------------------------------------\n")
            f.write(f"-- Table structure for `{table_name}`\n")
            f.write(f"-- --------------------------------------------------------\n")
            f.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")

            cursor.execute(f'PRAGMA table_info("{table_name}");')
            columns_info = cursor.fetchall()

            cursor.execute(f'PRAGMA foreign_key_list("{table_name}");')
            fk_info = cursor.fetchall()

            is_autoincrement = False
            if create_sql and "AUTOINCREMENT" in create_sql.upper():
                is_autoincrement = True

            col_defs = []
            pk_cols = []

            for col in columns_info:
                col_name = col[1]
                col_type = col[2]
                not_null = col[3]
                dflt_val = col[4]
                is_pk = (col[5] > 0)

                if is_pk:
                    pk_cols.append(col_name)

                col_is_autoinc = is_pk and len([c for c in columns_info if c[5] > 0]) == 1 and (is_autoincrement or "INT" in col_type.upper() or col_type == "")

                mysql_type = sqlite_type_to_mysql(col_type, col_name, is_pk, col_is_autoinc)

                col_clause = f"`{col_name}` {mysql_type}"

                if not_null and not col_is_autoinc:
                    col_clause += " NOT NULL"

                if dflt_val is not None:
                    dflt_clean = dflt_val.strip()
                    if dflt_clean.upper() in ["NULL", "CURRENT_TIMESTAMP"]:
                        col_clause += f" DEFAULT {dflt_clean.upper()}"
                    else:
                        col_clause += f" DEFAULT {dflt_clean}"

                col_defs.append(col_clause)

            if pk_cols:
                pk_str = ", ".join([f"`{c}`" for c in pk_cols])
                has_inline_pk = any("PRIMARY KEY" in cd for cd in col_defs)
                if not has_inline_pk:
                    col_defs.append(f"PRIMARY KEY ({pk_str})")

            # Add Foreign Key Constraints
            fk_count = 1
            for fk in fk_info:
                # fk: id, seq, table, from, to, on_update, on_delete, match
                from_col = fk[3]
                to_table = fk[2]
                to_col = fk[4]
                on_upd = fk[5] if fk[5] != "NO ACTION" else "CASCADE"
                on_del = fk[6] if fk[6] != "NO ACTION" else "RESTRICT"

                fk_constraint = f"CONSTRAINT `fk_{table_name}_{from_col}_{fk_count}` FOREIGN KEY (`{from_col}`) REFERENCES `{to_table}` (`{to_col}`) ON DELETE {on_del} ON UPDATE {on_upd}"
                col_defs.append(fk_constraint)
                fk_count += 1

            f.write(f"CREATE TABLE `{table_name}` (\n  " + ",\n  ".join(col_defs) + "\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;\n\n")

            # Dump Data
            cursor.execute(f'SELECT * FROM "{table_name}";')
            rows = cursor.fetchall()

            if rows:
                f.write(f"-- Data for `{table_name}` ({len(rows)} rows)\n")
                col_names_str = ", ".join([f"`{col[1]}`" for col in columns_info])
                
                chunk_size = 100
                for i in range(0, len(rows), chunk_size):
                    chunk = rows[i:i + chunk_size]
                    values_list = []
                    for row in chunk:
                        vals = ", ".join([escape_sql_value(v) for v in row])
                        values_list.append(f"({vals})")
                    
                    insert_stmt = f"INSERT INTO `{table_name}` ({col_names_str}) VALUES\n  " + ",\n  ".join(values_list) + ";\n"
                    f.write(insert_stmt)
                f.write("\n")

        f.write("SET FOREIGN_KEY_CHECKS = 1;\n")

    conn.close()
    print(f"\nSuccess! Exported MySQL SQL file WITH Foreign Keys generated at: {OUTPUT_SQL_PATH}")

if __name__ == "__main__":
    export_sqlite_to_mysql()
