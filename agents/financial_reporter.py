from groq_client import chat_with_groq

def generate_report(news_analysis, price_analysis):
    prompt = [
        {"role": "system", "content": "Combine news and price analysis into a structured financial summary."},
        {"role": "user", "content": f"News Analysis:\n{news_analysis}\n\nPrice Analysis:\n{price_analysis}"}
    ]
    return chat_with_groq(prompt)
