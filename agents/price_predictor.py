def predict_price(historical_prices, sentiment_score):
    """
    Predicts the next price based on basic sentiment-weighted logic.
    """
    if not historical_prices:
        return {
            "error": "No historical price data available."
        }

    last_price = historical_prices[-1]

    # Apply a sentiment-based adjustment (very simple logic)
    # Scale sentiment to a percent change, e.g., ±5%
    adjustment_factor = sentiment_score * 0.05
    predicted_price = last_price * (1 + adjustment_factor)

    return {
        "last_price": last_price,
        "predicted_price": round(predicted_price, 2),
        "sentiment_score": sentiment_score
    }
