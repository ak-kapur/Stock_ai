import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from agents import (
    ticker_extractor, news_retriever, price_retriever,
    news_analyst, price_analyst, financial_reporter, final_answer
)

st.set_page_config(page_title="StockWise AI", layout="centered")
st.title("📈 StockWise AI – LLM-powered Stock Advisor")

query = st.text_input("Ask about a stock:")
if query:
    tickers = ticker_extractor.extract_tickers(query)
    if not tickers:
        st.error("Could not extract a valid ticker. Try again.")
        st.stop()

    st.write(f"Identified Ticker(s): {tickers}")
    
    for ticker in tickers:
        st.subheader(f"📊 {ticker} Analysis")

        news = news_retriever.get_news_for_ticker(ticker)

        price_data = price_retriever.get_price_data(ticker)
        
        if "error" in price_data:
            st.error(f"Price retrieval failed: {price_data['error']}")
        else:
            st.write(f"Current price of {price_data['symbol']}: ${price_data['current_price']}")
            if "historical" in price_data and price_data["historical"]:
                price_points = ["Previous Close", "Open", "High", "Low", "Current"]
            price_values = price_data["historical"]

            fig = go.Figure()
            fig.add_trace(go.Scatter(
            x=price_points,
            y=price_values,
            mode='lines+markers',
            line=dict(color='royalblue', width=2),
            marker=dict(size=8),
            name='Price'
        ))

            fig.update_layout(
            title=f"{price_data['symbol']} Price Overview",
            xaxis_title="Price Points",
            yaxis_title="Price (USD)",
            template="plotly_white"
        )

            st.subheader("📉 Price Overview Chart")
            st.plotly_chart(fig, use_container_width=True)
        

        with st.spinner("Analyzing news..."):
            news_summary = news_analyst.analyze_news(news)
            st.success("News analyzed.")

        with st.spinner("Analyzing price..."):
            price_summary = price_analyst.analyze_price_data(price_data["historical"])
            st.success("Price analyzed.")

        with st.spinner("Generating financial report..."):
            summary = financial_reporter.generate_report(news_summary, price_summary)
            st.markdown(summary)

        with st.spinner("Generating advice..."):
            advice = final_answer.generate_advice(summary)
            st.markdown(f"### 💡 Final Advice:\n{advice}")
