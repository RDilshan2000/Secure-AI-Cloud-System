from fastapi import FastAPI, Depends
from sqlmodel import Session
from models import User
from database import create_db_and_tables, get_session, engine
from security import get_password_hash
from pydantic import BaseModel

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Secure AI Vault")

class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/signup")
def signup(user: UserCreate, session: Session = Depends(get_session)):
    
    hashed_pass = get_password_hash(user.password)
    
    new_user = User(username=user.username, password_hash=hashed_pass)
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return {"message": "User Saved to DB! ", "user_id": new_user.id}