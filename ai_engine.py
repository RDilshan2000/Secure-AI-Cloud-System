# UPDATE FORCE V1
import requests
import os

API_URL = "https://router.huggingface.co/models/facebook/bart-large-cnn"
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def summarize_text(text: str):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text})
        result = response.json()
        
        
        if isinstance(result, list):
            return result[0]['summary_text']
        
        
        if isinstance(result, dict) and "error" in result:
             return f"AI Says: {result['error']}"
             
        
        return f"Unknown Reply: {result}"
        
    except Exception as e:
        return f"System Error: {str(e)}"