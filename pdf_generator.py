from fpdf import FPDF
from datetime import datetime
import re

class StockReportPDF(FPDF):
    def header(self):
        """Automatic header for all pages"""
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'StockWise AI - Stock Analysis Report', 0, 0, 'R')
        self.ln(15)
    
    def footer(self):
        """Automatic footer for all pages"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


def sanitize_text(text):
    """
    Remove emojis and special unicode characters that cause PDF encoding errors
    """
    if not text:
        return ""
    
    # Remove emojis and special unicode characters
    # Keep only ASCII printable characters and common punctuation
    sanitized = re.sub(r'[^\x00-\x7F]+', ' ', str(text))
    
    # Remove multiple spaces
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    # Remove special markdown characters that might cause issues
    sanitized = sanitized.replace('*', '').replace('#', '').replace('_', '')
    
    return sanitized.strip()


def create_stock_report(ticker, price_data, prediction, news_analysis, price_analysis):
    """
    Create a professional PDF stock analysis report
    """
    pdf = StockReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Sanitize all text inputs
    ticker = sanitize_text(ticker)
    news_analysis = sanitize_text(news_analysis)
    price_analysis = sanitize_text(price_analysis)
    prediction_reasoning = sanitize_text(prediction.get('reasoning', ''))
    
    # Title
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 15, f'{ticker} Stock Analysis Report', ln=True, align='C')
    
    # Date
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 8, f'Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}', 
             ln=True, align='C')
    pdf.ln(10)
    
    # Executive Summary Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'EXECUTIVE SUMMARY', ln=True)
    pdf.set_draw_color(0, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Current Price Metrics Table
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Current Price Information:', ln=True)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    
    # Create price metrics table
    col_width = 90
    row_height = 7
    
    metrics = [
        ('Current Price:', f"${price_data['current_price']:.2f}"),
        ('Previous Close:', f"${price_data['previous_close']:.2f}"),
        ('Day High:', f"${price_data['high_price']:.2f}"),
        ('Day Low:', f"${price_data['low_price']:.2f}"),
        ('Opening Price:', f"${price_data['open_price']:.2f}"),
    ]
    
    for label, value in metrics:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(col_width, row_height, label, border=1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(col_width, row_height, value, border=1, ln=True)
    
    pdf.ln(8)
    
    # Price Prediction Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '7-DAY PRICE PREDICTION', ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    current_price = price_data['current_price']
    predicted_price = prediction['predicted_price']
    price_change = predicted_price - current_price
    pct_change = (price_change / current_price) * 100
    
    prediction_metrics = [
        ('Predicted Price (7 days):', f"${predicted_price:.2f}"),
        ('Current Price:', f"${current_price:.2f}"),
        ('Expected Change:', f"${price_change:+.2f} ({pct_change:+.2f}%)"),
        ('Confidence Level:', sanitize_text(prediction['confidence'].upper())),
    ]
    
    pdf.set_font('Arial', '', 10)
    for label, value in prediction_metrics:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(col_width, row_height, label, border=1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(col_width, row_height, str(value), border=1, ln=True)
    
    pdf.ln(5)
    
    # Prediction Reasoning
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 7, 'Prediction Analysis:', ln=True)
    pdf.set_font('Arial', '', 10)
    
    # Truncate and sanitize reasoning
    reasoning_text = prediction_reasoning[:400] if len(prediction_reasoning) > 400 else prediction_reasoning
    if reasoning_text:
        pdf.multi_cell(0, 5, reasoning_text)
    else:
        pdf.multi_cell(0, 5, 'Analysis based on historical trends and current market conditions.')
    pdf.ln(5)
    
    # News & Sentiment Analysis
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'NEWS & SENTIMENT ANALYSIS', ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 10)
    # Truncate if too long
    news_text = news_analysis[:800] if len(news_analysis) > 800 else news_analysis
    if news_text:
        pdf.multi_cell(0, 5, news_text)
    else:
        pdf.multi_cell(0, 5, 'Market sentiment analysis based on recent news and reports.')
    pdf.ln(5)
    
    # Price Trend Analysis
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'TECHNICAL PRICE ANALYSIS', ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 10)
    price_text = price_analysis[:600] if len(price_analysis) > 600 else price_analysis
    if price_text:
        pdf.multi_cell(0, 5, price_text)
    else:
        pdf.multi_cell(0, 5, 'Technical analysis based on historical price movements and trading patterns.')
    pdf.ln(8)
    
    # Investment Recommendation Box
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'INVESTMENT SUMMARY', ln=True, fill=True, align='C')
    pdf.ln(3)
    
    pdf.set_font('Arial', '', 10)
    
    # Determine recommendation based on prediction
    if pct_change > 5:
        recommendation = "POSITIVE OUTLOOK - Consider buying for potential gains"
    elif pct_change < -5:
        recommendation = "CAUTIOUS OUTLOOK - Monitor closely before investing"
    else:
        recommendation = "NEUTRAL OUTLOOK - Hold current positions"
    
    pdf.multi_cell(0, 5, recommendation, align='C')
    pdf.ln(10)
    
    # Disclaimer
    pdf.set_fill_color(255, 240, 240)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 8, 'IMPORTANT DISCLAIMER', ln=True, fill=True, align='C')
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 8)
    disclaimer = """This report is for informational purposes only and should not be considered financial advice. 
The predictions and analysis contained herein are based on historical data, current market sentiment, 
and algorithmic analysis. Past performance does not guarantee future results. Stock prices are subject 
to market volatility and unforeseen events. Always conduct your own research and consult with a licensed 
financial advisor before making investment decisions. StockWise AI and its creators are not responsible 
for any financial losses incurred based on this report."""
    
    pdf.multi_cell(0, 4, disclaimer)
    pdf.ln(5)
    
    # Footer info
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 5, 'Powered by StockWise AI - Intelligent Stock Analysis Platform', align='C')
    
    # Return PDF as bytes
    try:
        return pdf.output(dest='S').encode('latin-1')
    except Exception as e:
        print(f"[PDF Generation Error] {e}")
        # Create a simple error PDF
        error_pdf = FPDF()
        error_pdf.add_page()
        error_pdf.set_font('Arial', 'B', 16)
        error_pdf.cell(0, 10, 'PDF Generation Error', ln=True)
        error_pdf.set_font('Arial', '', 10)
        error_pdf.multi_cell(0, 5, 'Unable to generate full report. Please try again.')
        return error_pdf.output(dest='S').encode('latin-1')
