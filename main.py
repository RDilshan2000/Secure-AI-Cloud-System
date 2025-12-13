from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from models import User
from database import create_db_and_tables, get_session
from security import get_password_hash, verify_password
from auth import create_access_token, SECRET_KEY, ALGORITHM
from ai_engine import summarize_text
from pydantic import BaseModel
from contextlib import asynccontextmanager
from jose import jwt, JWTError

# App එක පටන් ගන්නකොට Database එක හදන කොටස
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Secure AI Vault")

# Login පාර
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Models ---
class UserCreate(BaseModel):
    username: str
    password: str

class NoteRequest(BaseModel):
    content: str

# --- The GUARD (මුරකරු) ---
# මේ කොටස අනිවාර්යයෙන්ම analyze_note එකට උඩින් තියෙන්න ඕන
async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Token එක ලිහා බලනවා
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # Database එකේ ඒ නම තියෙන කෙනෙක් ඉන්නවද බලනවා
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user

# --- Routes ---

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
    return {"message": "User Saved!", "user_id": new_user.id}

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

# ආරක්ෂිත AI කොටස (Protected Route)
@app.post("/analyze_note")
def analyze_note(note: NoteRequest, current_user: User = Depends(get_current_user)):
    summary = summarize_text(note.content)
    return {
        "user": current_user.username,
        "ai_summary": summary
    }