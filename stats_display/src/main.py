from fastapi import FastAPI
import psycopg2
import time

app = FastAPI()

DB_CONFIG = {
    "dbname": "log-service",
    "user": "postgres",
    "password": "postgres",
    "host": "log-service-db",
    "port": 5432
}

def display_stats():
    start_time = time.time()
    try:
        db_connection = psycopg2.connect(**DB_CONFIG)
        cursor = db_connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM logs")
        total_logs = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM logs WHERE timestamp > NOW() - INTERVAL '30 seconds'")
        logs_last_30s = cursor.fetchone()[0]

        cursor.execute("SELECT status, COUNT(*) FROM logs GROUP BY status")
        rows = cursor.fetchall()
        status_counts = {str(row[0]): row[1] for row in rows}

        cursor.execute("""
            SELECT timestamp, ip, status, message
            FROM logs
            ORDER BY timestamp DESC
            LIMIT 10
        """)
        rows = cursor.fetchall()
        recent_logs = [{"timestamp": str(r[0]), "ip": r[1], "status": r[2], "message": r[3]} for r in rows]

        cursor.close()
        response_time_seconds = round(time.time() - start_time, 2)

        return {
            "logs_inserted_last_30s": logs_last_30s,
            "throughput_per_second": round(logs_last_30s / 30, 2),
            "response_time_seconds": response_time_seconds,
            "total_logs_in_db": total_logs,
            "status_counts": status_counts,
            "recent_10_logs": recent_logs
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'db_connection' in locals():
            db_connection.close()

@app.get("/stats-display")
async def get_stats():
    return display_stats()
