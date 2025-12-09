import numpy as np
from groq_client import chat_with_groq

def predict_future_price(historical_data, news_sentiment, ticker):
    """
    Predict future price using LLM analysis + simple momentum
    """
    try:
        close_prices = historical_data['close']
        
        # Calculate momentum indicators
        recent_trend = (close_prices[-1] - close_prices[-7]) / close_prices[-7] * 100
        volatility = np.std(close_prices[-30:])
        current_price = close_prices[-1]
        
        # Use LLM for prediction reasoning
        prompt = [{
            "role": "system",
            "content": "You are a financial analyst predicting stock prices."
        }, {
            "role": "user",
            "content": f"""Analyze {ticker} stock:
            
Current Price: ${current_price:.2f}
7-day Trend: {recent_trend:+.2f}%
30-day Volatility: ${volatility:.2f}
News Sentiment: {news_sentiment}

Predict the price in 7 days. Consider:
1. Recent momentum
2. News sentiment
3. Market volatility

Return ONLY a JSON: {{"predicted_price": <number>, "confidence": "<low/medium/high>", "reasoning": "<brief>"}}"""
        }]
        
        response = chat_with_groq(prompt, model="llama-3.3-70b-versatile")
        
        # Parse LLM response
        import json
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            prediction = json.loads(json_match.group())
            return prediction
        else:
            # Fallback to simple momentum-based prediction
            predicted_price = current_price * (1 + recent_trend/100 * 0.5)
            return {
                "predicted_price": round(predicted_price, 2),
                "confidence": "medium",
                "reasoning": "Based on recent momentum and volatility"
            }
            
    except Exception as e:
        print(f"[Prediction Error] {e}")
        return {
            "predicted_price": close_prices[-1],
            "confidence": "low",
            "reasoning": "Insufficient data for prediction"
        }
