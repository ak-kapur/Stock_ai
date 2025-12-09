import pandas as pd

def analyze_price_data(hist_data):
    try:
        # Convert list to a pandas Series
        series = pd.Series(hist_data)

        # Use describe() for quick stats
        description = series.describe().to_string()

        # You can also calculate trends or percent changes here
        trend = "increasing" if series.iloc[-1] > series.iloc[0] else "decreasing"

        return f"""
📈 Price Trend: {trend}
📊 Summary Stats:
{description}
"""
    except Exception as e:
        return f"Error analyzing price data: {e}"
