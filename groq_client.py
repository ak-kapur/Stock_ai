

# GROQ_API_KEY = ""



import requests

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def chat_with_groq(messages, model="llama3-70b-8192"):
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
