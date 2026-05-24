from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title = "Logistics Core Api",
    description="Backend routing and fleet management system.",
    version="1.0.0"
)

db_tasks = {}

class TechnicianTask(BaseModel):
    barcode: str
    technician_name: str
    is_hazardous: bool
    temperature_celsius: Optional[float] = None

@app.get("/")
async def root():
    return{
        "service": "EcoTrans Core API",
        "status": "online"
    }

@app.get("/tasks/")
async def create_task(task: TechnicianTask):
    if task.barcode in db_tasks:
        raise HTTPException(status_code=400, detail="Barcode already registered in the system.")
    
    return {"message": "Task registered successfully", "data": task}


@app.get("/tasks/{barcode}")
async def get_task(barcode: str):
    if barcode not in db_tasks:
        raise HTTPException(status_code=404, detail="Task not found.")

    return db_tasks[barcode]
