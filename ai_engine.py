import requests
import os


API_URL_SUMMARY = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
API_URL_SENTIMENT = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"


raw_token = os.environ.get("HF_TOKEN")
token = raw_token.strip() if raw_token else None
HEADERS = {"Authorization": f"Bearer {token}"}

def summarize_text(text):
    payload = {"inputs": text, "parameters": {"max_length": 150, "min_length": 40}}
    try:
        response = requests.post(API_URL_SUMMARY, headers=HEADERS, json=payload)
        
        
        if response.status_code != 200:
            return f"AI Error ({response.status_code}): {response.text}"
            
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("summary_text", "Summary not found.")
        elif "error" in result:
            return f"AI Error: {result['error']}"
        else:
            return "Unexpected AI response."
    except Exception as e:
        return f"Code Crash: {str(e)}"

def detect_mood(text):
    payload = {"inputs": text}
    try:
        response = requests.post(API_URL_SENTIMENT, headers=HEADERS, json=payload)
        
        
        if response.status_code != 200:
            return f"AI Error ({response.status_code}): {response.text}"

        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], list): 
                top_mood = result[0][0]
            else:
                top_mood = result[0]
                
            label = top_mood['label'] 
            score = round(top_mood['score'] * 100, 1) 
            return f"{label} ({score}%)"
        elif "error" in result:
            return f"AI Error: {result['error']}"
        else:
            return "Unknown Mood"
    except Exception as e:
        return f"Code Crash: {str(e)}"