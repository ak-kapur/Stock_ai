import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
from agents import (
    ticker_extractor, news_retriever, price_retriever,
    news_analyst, price_analyst, financial_reporter, final_answer, price_predictor
)

st.set_page_config(page_title="StockWise AI", layout="wide")
st.title("📈 StockWise AI – LLM-powered Stock Advisor")

query = st.text_input("Ask about a stock:", placeholder="e.g., Apple, TSLA, Microsoft stock")

if query:
    tickers = ticker_extractor.extract_tickers(query)
    
    if not tickers:
        st.error("Could not extract a valid ticker. Try again.")
        st.stop()

    st.write(f"**Identified Ticker(s):** {', '.join(tickers)}")
    
    for ticker in tickers:
        st.markdown("---")
        st.header(f" {ticker} Analysis")
        
        # Fetch all data
        with st.spinner(f"Fetching data for {ticker}..."):
            news = news_retriever.get_news_for_ticker(ticker)
            price_data = price_retriever.get_price_data(ticker)
            historical_data = price_retriever.get_historical_data(ticker, days=90)
        
        if "error" in price_data:
            st.error(f" Price retrieval failed: {price_data['error']}")
            continue
        
        # Display current price prominently
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Price", f"${price_data['current_price']:.2f}")
        with col2:
            change = price_data['current_price'] - price_data['previous_close']
            change_pct = (change / price_data['previous_close']) * 100
            st.metric("Change", f"${change:.2f}", f"{change_pct:+.2f}%")
        with col3:
            st.metric("High", f"${price_data['high_price']:.2f}")
        with col4:
            st.metric("Low", f"${price_data['low_price']:.2f}")
        
        # Historical Price Chart
        if "error" not in historical_data and historical_data.get('timestamps'):
            st.subheader(" Historical Price Chart (90 Days)")
            
            # Convert timestamps to datetime
            dates = [datetime.fromtimestamp(ts) for ts in historical_data['timestamps']]
            
            # Create subplots: Candlestick + Volume
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.05,
                subplot_titles=(f'{ticker} Price Movement', 'Trading Volume'),
                row_heights=[0.7, 0.3]
            )
            
            # Candlestick Chart
            fig.add_trace(
                go.Candlestick(
                    x=dates,
                    open=historical_data['open'],
                    high=historical_data['high'],
                    low=historical_data['low'],
                    close=historical_data['close'],
                    name='OHLC',
                    increasing_line_color='#26a69a',
                    decreasing_line_color='#ef5350',
                    increasing_fillcolor='#26a69a',
                    decreasing_fillcolor='#ef5350'
                ),
                row=1, col=1
            )
            
            # Volume bars with color coding
            colors = ['#26a69a' if historical_data['close'][i] >= historical_data['open'][i] 
                      else '#ef5350' for i in range(len(historical_data['close']))]
            
            fig.add_trace(
                go.Bar(
                    x=dates,
                    y=historical_data['volume'],
                    name='Volume',
                    marker_color=colors,
                    showlegend=False,
                    opacity=0.7
                ),
                row=2, col=1
            )
            
            # Update layout
            fig.update_layout(
                height=700,
                xaxis_rangeslider_visible=False,
                hovermode='x unified',
                template='plotly_white',
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            fig.update_yaxes(title_text="Price ($)", row=1, col=1)
            fig.update_yaxes(title_text="Volume", row=2, col=1)
            fig.update_xaxes(title_text="Date", row=2, col=1)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Alternative: Simple Line Chart (uncomment if you prefer)
            # st.subheader("📉 Price Trend")
            # line_fig = go.Figure()
            # line_fig.add_trace(go.Scatter(
            #     x=dates,
            #     y=historical_data['close'],
            #     mode='lines',
            #     name='Close Price',
            #     line=dict(color='#1f77b4', width=2),
            #     fill='tozeroy',
            #     fillcolor='rgba(31, 119, 180, 0.2)'
            # ))
            # line_fig.update_layout(
            #     title=f"{ticker} Closing Price Trend",
            #     xaxis_title="Date",
            #     yaxis_title="Price ($)",
            #     template="plotly_white",
            #     height=400,
            #     hovermode='x'
            # )
            # st.plotly_chart(line_fig, use_container_width=True)
        
        else:
            st.warning(" Historical data not available. Showing current price info only.")
            
            # Fallback to simple price overview
            if "historical" in price_data and price_data["historical"]:
                price_points = ["Previous Close", "Open", "High", "Low", "Current"]
                price_values = price_data["historical"]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=price_points,
                    y=price_values,
                    mode='lines+markers',
                    line=dict(color='royalblue', width=3),
                    marker=dict(size=10, color='royalblue'),
                    name='Price'
                ))
                
                fig.update_layout(
                    title=f"{ticker} Price Overview",
                    xaxis_title="Price Points",
                    yaxis_title="Price ($)",
                    template="plotly_white",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Analysis section
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            with st.spinner("📰 Analyzing news..."):
                news_summary = news_analyst.analyze_news(news)
                st.success(" News analyzed")
        
        with col_right:
            with st.spinner(" Analyzing price trends..."):
                if "error" not in historical_data and historical_data.get('close'):
                    price_summary = price_analyst.analyze_price_data(historical_data['close'])
                else:
                    price_summary = price_analyst.analyze_price_data(price_data["historical"])
                st.success(" Price analyzed")
        
        # Financial Report
        st.subheader("📄 Financial Summary Report")
        with st.spinner("Generating comprehensive report..."):
            summary = financial_reporter.generate_report(news_summary, price_summary)
            st.markdown(summary)
        
        # Price Prediction
        if "error" not in historical_data and historical_data.get('close'):
            st.subheader(" 7-Day Price Prediction")
            
            with st.spinner("Predicting future price using AI..."):
                prediction = price_predictor.predict_future_price(
                    historical_data, 
                    news_summary, 
                    ticker
                )
            
            pred_col1, pred_col2, pred_col3 = st.columns(3)
            
            with pred_col1:
                price_change = prediction['predicted_price'] - price_data['current_price']
                price_change_pct = (price_change / price_data['current_price']) * 100
                st.metric(
                    "Predicted Price (7 days)",
                    f"${prediction['predicted_price']:.2f}",
                    delta=f"{price_change_pct:+.2f}%"
                )
            
            with pred_col2:
                confidence_emoji = {
                    'low': '🟡',
                    'medium': '🟠', 
                    'high': '🟢'
                }.get(prediction['confidence'].lower(), '⚪')
                st.metric(
                    "Confidence Level", 
                    f"{confidence_emoji} {prediction['confidence'].upper()}"
                )
            
            with pred_col3:
                st.metric(
                    "Current Price", 
                    f"${price_data['current_price']:.2f}"
                )
            
            st.info(f"**💡 Prediction Reasoning:** {prediction['reasoning']}")
        
        # Final Investment Advice
        st.subheader("💡 Investment Recommendation")
        with st.spinner("Generating final investment advice..."):
            advice = final_answer.generate_advice(summary)
            st.markdown(advice)
        
        # Disclaimer
        st.caption("⚠️ **Disclaimer:** This analysis is for informational purposes only and should not be considered financial advice. Always consult with a licensed financial advisor before making investment decisions.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Powered by Groq AI, Finnhub, and NewsAPI | Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)
