import requests
import os
import time


raw_token = os.environ.get("HF_TOKEN")
token = raw_token.strip() if raw_token else None
HEADERS = {"Authorization": f"Bearer {token}"}


def query_huggingface(payload, model_id):
    
    urls = [
        f"https://api-inference.huggingface.co/models/{model_id}",        
        f"https://router.huggingface.co/hf-inference/models/{model_id}", 
        f"https://router.huggingface.co/models/{model_id}"               
    ]
    
    last_error = "No URL worked"
    
    for url in urls:
        try:
            response = requests.post(url, headers=HEADERS, json=payload)
            
            
            if response.status_code == 200:
                return response.json()
            
            
            elif response.status_code == 503:
                time.sleep(2)
                response = requests.post(url, headers=HEADERS, json=payload)
                if response.status_code == 200:
                    return response.json()
            
            last_error = f"Error {response.status_code}: {response.text}"
            
        except Exception as e:
            last_error = str(e)
            continue 
            
    
    return {"error": last_error}

def summarize_text(text):
    payload = {"inputs": text, "parameters": {"max_length": 150, "min_length": 40}}
    
    result = query_huggingface(payload, "facebook/bart-large-cnn")
    
    if isinstance(result, list) and len(result) > 0:
        return result[0].get("summary_text", "Summary not found.")
    elif isinstance(result, dict) and "error" in result:
        return f"AI Error: {result['error']}"
    else:
        return "Unexpected AI response."

def detect_mood(text):
    payload = {"inputs": text}
    
    result = query_huggingface(payload, "distilbert-base-uncased-finetuned-sst-2-english")
    
    if isinstance(result, list) and len(result) > 0:
        if isinstance(result[0], list):
            top_mood = result[0][0]
        else:
            top_mood = result[0]
            
        label = top_mood['label'] 
        score = round(top_mood['score'] * 100, 1) 
        return f"{label} ({score}%)"
    elif isinstance(result, dict) and "error" in result:
        return f"AI Error: {result['error']}"
    else:
        return "Unknown Mood"