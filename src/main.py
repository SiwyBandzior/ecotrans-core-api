from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from . import models, auth
from .database import engine, sessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="EcoTrans Core API - Secured")

class TechnicianTask(BaseModel):
    barcode: str
    technician_name: str
    is_hazardous: bool
    temperature_celsius: Optional[float] = None

class UserCreate(BaseModel):
    username: str
    password: str


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(auth.oauth2_scheme), db: Session= Depends(get_db)):
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except auth.jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(models.UserDB).filter(models.UserDB.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.post("/register")
async def register_user(user:UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.UserDB).filter(models.UserDB.username == user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_pw = auth.get_password_hash(user.password)
    new_user = models.UserDB(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.UserDB).filter(models.UserDB.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/task/")
async def create_task(task: TechnicianTask, db: Session = Depends(get_db), current_user: models.UserDB = Depends(get_current_user)):
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
    return {"message": f"Task saved securely by {current_user.username}"}


@app.get("/tasks/{barcode}")
async def get_task(barcode: str, db: Session = Depends(get_db)):
    db_task = db.query(models.TaskDB).filter(models.TaskDB.barcode == barcode).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found in DB.")
    return db_task