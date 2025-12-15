import requests
import os

API_URL = "https://router.huggingface.co/models/facebook/bart-large-cnn"
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def summarize_text(text: str):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text})
        
        
        if response.status_code != 200:
            
            return f"AI Error ({response.status_code}): {response.text}"
            
        
        result = response.json()
        
        if isinstance(result, list):
            return result[0]['summary_text']
        elif isinstance(result, dict) and 'error' in result:
             return f"AI Says: {result['error']}"
        else:
             return f"Unknown Reply: {result}"
             
    except Exception as e:
        return f"Code Crash: {str(e)}"