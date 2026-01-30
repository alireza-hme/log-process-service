from fastapi import FastAPI
from psycopg2 import connect, OperationalError
from typing import List, Dict

app = FastAPI()

# Config
DB_CONFIG = {
    "dbname": "log-service",
    "password": "postgres",
    "host": "log-service-db",
    "user": "postgres",
    "port": 5432
}

def insert_logs(logs: List[Dict]):
    try:
        db_connection = connect(**DB_CONFIG)
        cursor = db_connection.cursor()
        cursor.executemany(""" 
            INSERT INTO logs(timestamp, ip, user_agent, status, message) 
                       VALUES(%s, %s, %s, %s, %s)
            """, [(log["timestamp"], log["ip"], log["user_agent"], log["status"], log["message"]) for log in logs])
        
        db_connection.commit()
        cursor.close()
        db_connection.close()
    except OperationalError as e:
        print("Database connection error:", e)

@app.post("/logs")
async def receive_logs(logs: List[Dict]):
    insert_logs(logs)
    return {"message": "Logs received"}
