import finnhub
import streamlit as st
from datetime import datetime, timedelta

# Replace this with your actual API key

FINNHUB_API_KEY = st.secrets["FINNHUB_API_KEY"] 

# Setup client
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)


def get_historical_data(ticker, days=30):
    """
    Fetch historical OHLCV data for candlestick/line charts
    """
    try:
        # Calculate timestamps
        end_time = int(datetime.now().timestamp())
        start_time = int((datetime.now() - timedelta(days=days)).timestamp())
        
        # Fetch candles data (D = daily resolution)
        candles = finnhub_client.stock_candles(
            ticker, 
            'D',  # Daily resolution
            start_time, 
            end_time
        )
        
        if candles['s'] == 'ok':
            return {
                'timestamps': candles['t'],
                'open': candles['o'],
                'high': candles['h'],
                'low': candles['l'],
                'close': candles['c'],
                'volume': candles['v']
            }
        else:
            return {'error': 'No historical data available'}
            
    except Exception as e:
        print(f"[Historical Data Error] {e}")
        return {'error': str(e)}


def get_price_data(ticker):
    try:
        quote = finnhub_client.quote(ticker)

        if not quote or quote["c"] == 0:
            return {
                "error": "Price data unavailable or invalid ticker.",
                "historical": []
            }

        return {
    "symbol": ticker,  # Add this line
    "current_price": quote["c"],
    "high_price": quote["h"],
    "low_price": quote["l"],
    "open_price": quote["o"],
    "previous_close": quote["pc"],
    "historical": [quote["pc"], quote["o"], quote["h"], quote["l"], quote["c"]]
}

    except Exception as e:
        print(f"[Price Retriever Error] {e}")
        return {
            "error": "Failed to fetch price data.",
            "historical": []
        }
