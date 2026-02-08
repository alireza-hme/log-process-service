from fastapi import FastAPI, HTTPException
from psycopg2 import connect, OperationalError
from typing import List, Dict
import time

app = FastAPI()

DB_CONFIG = {
    "dbname": "log-service",
    "password": "postgres",
    "host": "log-service-db",
    "user": "postgres",
    "port": 5432
}

processing = False  # Global flag to track if processing

def insert_logs(logs: List[Dict]):
    try:
        db_connection = connect(**DB_CONFIG)
        cursor = db_connection.cursor()
        cursor.executemany("""
            INSERT INTO logs(timestamp, ip, user_agent, status, message, response_time)
            VALUES (NOW(), %s, %s, %s, %s, %s)
        """, [(log["ip"], log["user_agent"], log["status"], log["message"], log["response_time"]) for log in logs])
        db_connection.commit()
        cursor.close()
        db_connection.close()
    except OperationalError as e:
        print("Database error:", e)

@app.post("/logs")
async def receive_logs(logs: List[Dict]):
    global processing
    
    # Reject if already processing (creates clear bottleneck)
    if processing:
        raise HTTPException(status_code=503, detail="Server busy, try again later")
    
    processing = True
    try:
        time.sleep(5)  # 5 second bottleneck
        insert_logs(logs)
        return {"message": f"Inserted {len(logs)} logs"}
    finally:
        processing = False