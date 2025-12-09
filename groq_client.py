

# GROQ_API_KEY = ""



import requests
import streamlit as st


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    print(f"[DEBUG] API Key loaded: {GROQ_API_KEY[:10]}...")  # First 10 chars only
except Exception as e:
    print(f"[ERROR] Failed to load secrets: {e}")
    GROQ_API_KEY = None

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
def chat_with_groq(messages, model="llama-3.3-70b-versatile"):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.4
    }
    
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    
    try:
        res_json = response.json()
        if "choices" in res_json:
            return res_json["choices"][0]["message"]["content"]
        else:
            print("[Groq API Error] No 'choices' in response:", res_json)
            return "Error: Groq API did not return expected response."
    except Exception as e:
        print("[Groq API Exception]", e)
        return "Error: Failed to parse Groq response."
