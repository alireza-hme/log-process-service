from fastapi import FastAPI
from fastapi.background import BackgroundTasks
import asyncio
import os
import time
import random
import json
import faker
from datetime import datetime


app = FastAPI()

#Log file path
LOG_FILE_PATH = "/app/logs/logs.json"
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

def generate_logs(count=20):
    fake = faker.Faker()
    logs = []

    for _ in range(count):
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "ip": fake.ipv4(),
            "user_agent": fake.user_agent(),
            "status": random.choice([200, 500, 404]),
            "message": fake.sentence()
        })
    with open(LOG_FILE_PATH, "a") as file:
        json.dump(logs, file)
        file.write("\n")

def send_logs():
    try:
        with open(LOG_FILE_PATH, "r") as file:
            logs = [json.loads(line) for line in file]

        print("Sent Logs:", logs)
        open(LOG_FILE_PATH, "w").close()
    except Exception as e:
        print("Error Sending Logs:",e)


async def schedule_send_logs():
    while True:
        await asyncio.sleep(300) # 5 minutes
        send_logs()

@app.on_event("startup")
async def setup_periodic_task():
    # Run send_logs every 5 minutes
    asyncio.create_task(schedule_send_logs())