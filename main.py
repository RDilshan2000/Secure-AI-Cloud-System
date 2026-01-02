from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from models import User, ScanHistory
from database import create_db_and_tables, get_session
from security import get_password_hash, verify_password
from auth import create_access_token, SECRET_KEY, ALGORITHM
from ai_engine import summarize_text, detect_mood
from pydantic import BaseModel
from contextlib import asynccontextmanager
from jose import jwt, JWTError

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Secure AI Vault")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserCreate(BaseModel):
    username: str
    password: str

class AnalysisRequest(BaseModel):
    username: str
    text: str

async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user

@app.get("/")
def home():
    return {"message": "System Active 🧠"}



@app.post("/signup")
def signup(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    hashed_pass = get_password_hash(user.password)
    new_user = User(username=user.username, password_hash=hashed_pass)
    session.add(new_user)
    session.commit()
    return {"message": "User Saved!", "user_id": new_user.username}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users")
def get_all_users(session: Session = Depends(get_session)):
    
    users = session.exec(select(User)).all()
    return users

@app.delete("/users/{username}")
def delete_user(username: str, session: Session = Depends(get_session)):
    
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(user)
    session.commit()
    return {"message": f"User {username} deleted successfully"}



@app.post("/analyze")
@limiter.limit("5/minute") 
def analyze_text(request: Request, analysis_request: AnalysisRequest, session: Session = Depends(get_session)):
    summary = summarize_text(analysis_request.text)
    
    
    new_scan = ScanHistory(
        username=analysis_request.username,
        original_text=analysis_request.text,
        summary_text=summary
    )
    session.add(new_scan)
    session.commit()
    
    return {"summary": summary}

@app.post("/sentiment")
@limiter.limit("5/minute")
def analyze_sentiment(request: Request, analysis_request: AnalysisRequest, session: Session = Depends(get_session)):
    mood = detect_mood(analysis_request.text)
    
    new_scan = ScanHistory(
        username=analysis_request.username,
        original_text=analysis_request.text,
        summary_text=f"Mood Analysis: {mood}"
    )
    session.add(new_scan)
    session.commit()
    
    return {"result": mood}

@app.get("/history/{username}")
def get_history(username: str, session: Session = Depends(get_session)):
    statement = select(ScanHistory).where(ScanHistory.username == username)
    results = session.exec(statement).all()
    return results