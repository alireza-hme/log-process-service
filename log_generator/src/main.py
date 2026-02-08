from fastapi import FastAPI
import asyncio
import random
import faker
from datetime import datetime
import httpx

app = FastAPI()
fake = faker.Faker()

client: httpx.AsyncClient | None = None

async def generate_and_send():
    logs = []
    for _ in range(20):
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "ip": fake.ipv4(),
            "user_agent": fake.user_agent(),
            "status": random.choice([200, 404, 500]),
            "message": fake.sentence(),
            "response_time": random.randint(50, 2000),
        })

    try:
        resp = await client.post(
            "http://log-process-service:5001/logs",
            json=logs,
            headers={"Connection": "close"}  # Force spread traffic
        )
        resp.raise_for_status()
        print("Sent 20 logs")
    except Exception as e:
        print(f"Error: {e}")

async def scheduler():
    while True:
        await generate_and_send()
        await asyncio.sleep(1)

@app.on_event("startup")
async def startup():
    global client
    client = httpx.AsyncClient(timeout=httpx.Timeout(300.0))
    asyncio.create_task(scheduler())

@app.on_event("shutdown")
async def shutdown():
    if client:
        await client.aclose()
