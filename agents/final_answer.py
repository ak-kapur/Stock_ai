from groq_client import chat_with_groq

def generate_advice(financial_summary):
    prompt = [
        {"role": "system", "content": "Based on this summary, offer financial advice (buy/hold/sell)."},
        {"role": "user", "content": financial_summary}
    ]
    return chat_with_groq(prompt)
