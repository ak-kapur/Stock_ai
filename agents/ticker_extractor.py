import re
from groq_client import chat_with_groq

def extract_tickers(user_input):
    messages = [{
        "role": "system",
        "content": "You are a stock ticker extraction assistant. Extract ONLY valid stock ticker symbols from user queries."
    }, {
        "role": "user",
        "content": f"""Extract stock ticker symbols from this query and return ONLY a Python list format.

Examples:
- "Tell me about Apple" → ["AAPL"]
- "Compare Tesla and Microsoft" → ["TSLA", "MSFT"]
- "What's happening with NVDA?" → ["NVDA"]

Query: {user_input}

Return format: ["TICKER1", "TICKER2"]
If no tickers found, return: []"""
    }]
    
    response = chat_with_groq(messages, model="llama-3.3-70b-versatile")
    
    print(f"[DEBUG] Groq Response: {response}")  # Debug line
    
    if "Error" in response:
        print(f"[ERROR] Groq API failed: {response}")
        return []
    
    # Try to extract list from response
    try:
        # Look for ["..."] pattern
        import ast
        list_match = re.search(r'\[.*?\]', response)
        if list_match:
            tickers = ast.literal_eval(list_match.group())
            return tickers if isinstance(tickers, list) else []
    except Exception as e:
        print(f"[ERROR] Failed to parse: {e}")
    
    return []
