from fastapi import FastAPI
from pydantic import BaseModel
from security import get_password_hash, verify_password 

app = FastAPI(title="Secure AI Vault")

# The model that describes what kind of data a user sends.
class UserSchema(BaseModel):
    username: str
    password: str

@app.get("/")
def home():
    return {"message": "System Active", "version": "2.0"}

# Where to create a new user (Signup)
@app.post("/signup")
def signup(user: UserSchema):
    # Here we don't take the password directly. We hash it.
    hashed_pass = get_password_hash(user.password)
    
    return {
        "username": user.username,
        "saved_password_hash": hashed_pass, # We can't seem to read this.
        "msg": "User created securely!"
    }