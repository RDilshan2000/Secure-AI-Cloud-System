from fastapi import FastAPI

#Create App
app = FastAPI(title="Secure AI Vault")

#Root Endpoint(Fist Loging see)
@app.get("/")
def home():
    return {
        "message": "Welcome to Secure AI Vault! 🚀",
        "status": "System Active",
        "version": "1.0"
    }

#Health Check (Cloud Imported)
@app.get("/health")
def health_check():
    return {"status": "Healthy", "cpu": "Normal"}