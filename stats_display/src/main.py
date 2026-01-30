from fastapi import FastAPI
import psycopg2

app = FastAPI()

DB_CONFIG = {
    "dbname": "log_service",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def display_stats():
    try:
        db_connection = psycopg2.connect(**DB_CONFIG)
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM logs")
        rows = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM logs")
        total = cursor.fetchone()[0]

        cursor.close()
        return {
            "total_logs": total,
            "status_counts": {str(r[0]): r[1] for r in rows}
        }

    except Exception as e:
        print("Error fetching logs:", str(e))

    finally:
        if 'db_connection' in locals():
            db_connection.close()