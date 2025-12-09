import finnhub
import streamlit as st
from datetime import datetime, timedelta

# Get API key from Streamlit secrets
FINNHUB_API_KEY = st.secrets["FINNHUB_API_KEY"]

# Setup client
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)


def get_historical_data(ticker, days=90):
    """
    Fetch historical data with fallback to yfinance
    """
    # Try Finnhub first
    try:
        end_time = int(datetime.now().timestamp())
        start_time = int((datetime.now() - timedelta(days=days)).timestamp())
        
        candles = finnhub_client.stock_candles(ticker, 'D', start_time, end_time)
        
        if candles and candles.get('s') == 'ok' and candles.get('t'):
            print(f"[Success] Finnhub provided data for {ticker}")
            return {
                'timestamps': candles['t'],
                'open': candles['o'],
                'high': candles['h'],
                'low': candles['l'],
                'close': candles['c'],
                'volume': candles['v']
            }
        else:
            print(f"[Finnhub] No data returned: {candles}")
    except Exception as e:
        print(f"[Finnhub Error] {ticker}: {e}")
    
    # Fallback to Yahoo Finance (FREE and reliable)
    print(f"[Fallback] Using Yahoo Finance for {ticker}")
    try:
        import yfinance as yf
        
        stock = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        hist = stock.history(start=start_date, end=end_date)
        
        if not hist.empty:
            timestamps = [int(dt.timestamp()) for dt in hist.index]
            print(f"[Success] Yahoo Finance provided {len(timestamps)} days of data")
            return {
                'timestamps': timestamps,
                'open': hist['Open'].tolist(),
                'high': hist['High'].tolist(),
                'low': hist['Low'].tolist(),
                'close': hist['Close'].tolist(),
                'volume': hist['Volume'].tolist()
            }
        else:
            print(f"[YFinance] No data available for {ticker}")
    except ImportError:
        print("[Error] yfinance not installed. Run: pip install yfinance")
    except Exception as e:
        print(f"[YFinance Error] {ticker}: {e}")
    
    # If both fail, return error
    return {
        'error': "Historical data unavailable from all sources",
        'timestamps': []
    }


def get_price_data(ticker):
    """
    Get current price quote data (Finnhub works fine for this)
    """
    try:
        quote = finnhub_client.quote(ticker)

        if not quote or quote.get("c", 0) == 0:
            return {
                "error": "Price data unavailable or invalid ticker.",
                "historical": []
            }

        return {
            "symbol": ticker,
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
            "error": f"Failed to fetch price data: {str(e)}",
            "historical": []
        }
