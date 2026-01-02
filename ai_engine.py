import requests


API_URL_SUMMARY = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
API_URL_SENTIMENT = "https://router.huggingface.co/hf-inference/models/distilbert-base-uncased-finetuned-sst-2-english"


HEADERS = {"Authorization": "Bearer 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"}

def summarize_text(text):
    payload = {"inputs": text, "parameters": {"max_length": 150, "min_length": 40}}
    try:
        response = requests.post(API_URL_SUMMARY, headers=HEADERS, json=payload)
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
        result = response.json()
        
        
        if isinstance(result, list) and len(result) > 0:
            
            top_mood = result[0][0] 
            label = top_mood['label'] 
            score = round(top_mood['score'] * 100, 1) 
            return f"{label} ({score}%)"
        elif "error" in result:
            return f"AI Error: {result['error']}"
        else:
            return "Unknown Mood"
    except Exception as e:
        return f"Code Crash: {str(e)}"