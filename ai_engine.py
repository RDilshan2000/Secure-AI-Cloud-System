from transformers import pipeline

ai_summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text: str):
    result = ai_summarizer(text, max_length=60, min_length=10, do_sample=False)
    return result[0]['summary_text']