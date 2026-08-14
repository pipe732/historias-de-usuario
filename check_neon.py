import psycopg2

configs = ['postgres', 'neondb', 'mine_inventory']
host = 'ep-crimson-glitter-at1wc2qg-pooler.c-9.us-east-1.aws.neon.tech'
user = 'neondb_owner'
password = 'npg_3SWYcRrA5aTz'

print("Probando conexion a Neon Tech...")
for dbname in configs:
    try:
        conn = psycopg2.connect(
            host=host, port=5432, user=user, password=password,
            dbname=dbname, sslmode='require', connect_timeout=8,
        )
        print(f"[OK] Conectado a database: {dbname}")
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database WHERE datistemplate=false;")
        dbs = [r[0] for r in cur.fetchall()]
        print(f"  Databases disponibles: {dbs}")
        conn.close()
        break
    except Exception as e:
        print(f"[FAIL] {dbname}: {e}")
