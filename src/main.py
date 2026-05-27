from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from . import models
from .database import engine, sessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "EcoTrans Core Api"
)


class TechnicianTask(BaseModel):
    barcode: str
    technician_name: str
    is_hazardous: bool
    temperature_celsius: Optional[float] = None


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tasks/")
async def create_task(task: TechnicianTask, db: Session = Depends(get_db)):
    db_task = db.query(models.TaskDB).filter(models.TaskDB.barcode == task.barcode).first()
    if db_task:
        raise HTTPException(status_code=400, detail="Barcode already registered.")
    
    new_task = models.TaskDB(
        barcode = task.barcode,
        technician_name = task.technician_name,
        is_hazardous = task.is_hazardous,
        temperature_celsius = task.temperature_celsius
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return{"message": "Task saved to DB!", "task_id": new_task.id}


@app.get("/tasks/{barcode}")
async def get_task(barcode: str, db: Session = Depends(get_db)):
    db_task = db.query(models.TaskDB).filter(models.TaskDB.barcode == barcode).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found in DB.")
    return db_task
