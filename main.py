import os
import psycopg


def load_dotenv(path=".env"):
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


def get_connection_params():
    load_dotenv()
    return {
        "host": os.environ.get("PGHOST"),
        "port": int(os.environ.get("PGPORT")),
        "user": os.environ.get("PGUSER"),
        "password": os.environ.get("PGPASSWORD"),
        "dbname": os.environ.get("PGDATABASE"),
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
