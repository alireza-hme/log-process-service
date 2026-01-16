from fastapi import FastAPI, BackgroundTasks
import asyncio
import os
import json
import faker
from datetime import datetime
from psycopg2 import connect, OperationalError
from typing import List, Dict

app = FastAPI()

# Config
LOG_FILE_PATH = "/app/logs/logs.json"
DB_CONFIG = {
    "dbname": "log_service",
    "password": "postgres",
    "host": "localhost",
    "user": "postgres",
    "port": 5432
}

os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)


def insert_logs_into_db(logs: List[Dict]):
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
    insert_logs_into_db(logs)
    return {"message": "Logs received"}
