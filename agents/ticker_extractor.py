import re
from groq_client import chat_with_groq

def extract_tickers(user_input):
    messages = [{
        "role": "user",
        "content": (
            f"Extract the stock ticker symbols mentioned in the user input below. "
            f"Return a valid Python list of strings. If none found, return []. "
            f"User input: '{user_input}'"
        )
    }]
    
    response = chat_with_groq(messages)

    if "Error" in response:
        return []

    try:
        # Try to directly evaluate if it’s a clean list
        tickers = eval(response.strip())
        if isinstance(tickers, list):
            return tickers
    except:
        # Try to extract list from code block using regex
        matches = re.findall(r"\[['\"]?[A-Z]{1,5}['\"]?\]", response)
        if matches:
            try:
                tickers = eval(matches[0])
                return tickers if isinstance(tickers, list) else []
            except:
                return []

    print(f"[Ticker Extractor Error] Could not parse Groq response: {response}")
    return []
