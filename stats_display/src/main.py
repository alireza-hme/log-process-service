from fastapi import FastAPI
import psycopg2

app = FastAPI()

DB_CONFIG = {
    "dbname": "log-service",
    "user": "postgres",
    "password": "postgres",
    "host": "log-service-db",
    "port": 5432
}

def display_stats():
    try:
        db_connection = psycopg2.connect(**DB_CONFIG)
        cursor = db_connection.cursor()
        
        # Count logs by status code
        cursor.execute("SELECT status, COUNT(*) FROM logs GROUP BY status")
        rows = cursor.fetchall()

        # Create a dictionary with status counts
        status_counts = {str(row[0]): row[1] for row in rows}

        cursor.close()
        return {
            "total_logs": len(rows),
            "status_counts": status_counts
        }

    except Exception as e:
        print("Error fetching logs:", str(e))

    finally:
        if 'db_connection' in locals():
            db_connection.close()
            
@app.get("/stats_display")
async def get_stats():
    return display_stats()