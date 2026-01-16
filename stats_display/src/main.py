import psycopg2
from datetime import datetime

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
        logs = cursor.fetchall()

        total_logs = len(logs)
        status_counts = {}

        for log in logs:
            status = log[3]  # Assuming status is the 4th column (index 3)
            status_counts[status] = status_counts.get(status, 0) + 1

        print(f"Total Logs: {total_logs}")
        print("Status Counts:")
        for status, count in status_counts.items():
            print(f"  {status}: {count}")

    except Exception as e:
        print("Error fetching logs:", e)
    finally:
        if 'db_connection' in locals():
            db_connection.close()