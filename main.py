from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from models import User
from database import create_db_and_tables, get_session
from security import get_password_hash
from pydantic import BaseModel
from contextlib import asynccontextmanager
from ai_engine import summarize_text

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Secure AI Vault")

class UserCreate(BaseModel):
    username: str
    password: str

class NoteRequest(BaseModel):
    content: str

@app.get("/")
def home():
    return {"message": "AI System Active"}

@app.post("/signup")
def signup(user: UserCreate, session: Session = Depends(get_session)):
    hashed_pass = get_password_hash(user.password)
    new_user = User(username=user.username, password_hash=hashed_pass)
    session.add(new_user)
    session.commit()
    return {"message": "User Saved!", "user_id": new_user.id}

@app.post("/analyze_note")
def analyze_note(note: NoteRequest):
    summary = summarize_text(note.content)
    
    return {
        "original_length": len(note.content),
        "ai_summary": summary,
        "status": "Analyzed by AI"
    }