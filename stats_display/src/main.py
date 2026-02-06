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

        # Fetch logs to include in the response
        cursor.execute("SELECT timestamp, ip, user_agent, status, message FROM logs")
        rows = cursor.fetchall()

        logs_info = [
            {
                "timestamp": row[0],
                "ip": row[1],
                "user_agent": row[2],
                "status": row[3],
                "message": row[4]
            }
            for row in rows
        ]
        
        # Count logs by status code
        cursor.execute("SELECT status, COUNT(*) FROM logs GROUP BY status")
        rows = cursor.fetchall()

        # Create a dictionary with status counts
        status_counts = {str(row[0]): row[1] for row in rows}

        cursor.close()
        return {
            "total_logs": len(logs_info),  
            "status_counts": status_counts,
            "logs_info": logs_info
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if 'db_connection' in locals():
            db_connection.close()
            
@app.get("/stats-display")
async def get_stats():
    return display_stats()