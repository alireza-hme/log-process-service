from fastapi import FastAPI
import asyncio
import os
import json
import random
import faker
from datetime import datetime
import httpx

app = FastAPI()

LOG_FILE_PATH = "/app/logs/logs.json"
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

fake = faker.Faker()

def generate_logs(count=20):
    logs = []
    for _ in range(count):
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "ip": fake.ipv4(),
            "user_agent": fake.user_agent(),
            "status": random.choice([200, 404, 500]),
            "message": fake.sentence()
        })

    with open(LOG_FILE_PATH, "a") as f:
        for log in logs:
            f.write(json.dumps(log) + "\n")

async def send_logs():
    if not os.path.exists(LOG_FILE_PATH):
        return

    try:
        with open(LOG_FILE_PATH, "r") as f:
            logs = [json.loads(line) for line in f if line.strip()]

        if not logs:
            return

        async with httpx.AsyncClient() as client:
            await client.post("http://log_process:5001/logs", json=logs)

        open(LOG_FILE_PATH, "w").close()

    except Exception as e:
        print("Send error:", e)

async def scheduler():
    while True:
        generate_logs()
        await send_logs()
        await asyncio.sleep(300)  # 5 minutes

@app.on_event("startup")
async def startup():
    asyncio.create_task(scheduler())
