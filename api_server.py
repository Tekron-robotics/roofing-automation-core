from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn

from src.automation_engine import engine

app = FastAPI(
    title="Tekron Robotics Roofing Automation API",
    description="Production API for the roofing automation engine.",
    version="1.0.0"
)

class Payload(BaseModel):
    task: str
    input: Dict[str, Any]

@app.post("/run")
def run_engine(payload: Payload):
    return engine.run(payload.dict())

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)
