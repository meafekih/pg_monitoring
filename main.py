import psycopg
import os

def get_connection_params():
    return {
        "host": os.environ.get("PGHOST", "172.18.0.2"),
        "port": int(os.environ.get("PGPORT", 6432)),
        "user": os.environ.get("PGUSER", "postgres"),
        "password": os.environ.get("PGPASSWORD", "admin"),
        "dbname": os.environ.get("PGDATABASE", "pagila"),
    }


def show_databases():
    params = get_connection_params()
    print("Connecting to PostgreSQL with:")
    print(f"  host={params['host']} port={params['port']} user={params['user']} dbname={params['dbname']}")

    with psycopg.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname"
            )
            rows = cur.fetchall()

    print("\nDatabases:")
    for row in rows:
        print(f" - {row[0]}")


if __name__ == "__main__":
    show_databases()
