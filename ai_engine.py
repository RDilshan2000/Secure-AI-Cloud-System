import requests
import os

# Hugging Face URL
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def summarize_text(text: str):
    
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text})
        return response.json()[0]['summary_text']
    except Exception as e:
        return f"Error: Could not connect to AI Brain. ({str(e)})"