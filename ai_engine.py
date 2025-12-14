import requests

# Hugging Face Public API
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

def summarize_text(text: str):
    try:
        
        response = requests.post(API_URL, json={"inputs": text})
        return response.json()[0]['summary_text']
    except:
        return "Error: Could not connect to AI Brain. Try again later."