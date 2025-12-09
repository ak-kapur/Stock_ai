from fpdf import FPDF
from datetime import datetime
import io

class StockReportPDF:
    def __init__(self, ticker, current_price, prediction):
        self.ticker = ticker
        self.current_price = current_price
        self.prediction = prediction
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=10)
    
    def add_header(self):
        """Add header with title and date"""
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 24)
        self.pdf.cell(0, 10, f"📈 {self.ticker} Stock Analysis Report", ln=True, align="C")
        
        self.pdf.set_font("Arial", "I", 10)
        self.pdf.cell(0, 5, f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                      ln=True, align="C")
        self.pdf.ln(10)
    
    def add_executive_summary(self, price_data, news_summary):
        """Add executive summary section"""
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, "Executive Summary", ln=True)
        self.pdf.set_line_width(0.5)
        self.pdf.line(10, self.pdf.get_y(), 200, self.pdf.get_y())
        self.pdf.ln(5)
        
        self.pdf.set_font("Arial", "", 11)
        
        # Current metrics
        summary_text = f"""
Current Price: ${price_data['current_price']:.2f}
Day High: ${price_data['high_price']:.2f}
Day Low: ${price_data['low_price']:.2f}
Previous Close: ${price_data['previous_close']:.2f}

Key Insights:
{news_summary[:300]}...
        """
        
        self.pdf.multi_cell(0, 6, summary_text.strip())
        self.pdf.ln(5)
    
    def add_price_section(self, price_data):
        """Add current price information"""
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "Current Price Information", ln=True)
        self.pdf.ln(3)
        
        # Create table
        self.pdf.set_font("Arial", "", 10)
        
        data = [
            ["Metric", "Value"],
            ["Current Price", f"${price_data['current_price']:.2f}"],
            ["High (Today)", f"${price_data['high_price']:.2f}"],
            ["Low (Today)", f"${price_data['low_price']:.2f}"],
            ["Open", f"${price_data['open_price']:.2f}"],
            ["Previous Close", f"${price_data['previous_close']:.2f}"],
        ]
        
        with self.pdf.table(
            borders_layout="MINIMAL",
            cell_fill_color=(200, 200, 200),
            cell_fill_mode="ROWS",
            line_height=7,
            text_align=("LEFT", "RIGHT"),
            width=160
        ) as table:
            for row in data:
                cells = table.row()
                for cell in row:
                    cells.cell(text=str(cell))
        
        self.pdf.ln(5)
    
    def add_prediction_section(self):
        """Add price prediction section"""
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "7-Day Price Prediction", ln=True)
        self.pdf.ln(3)
        
        self.pdf.set_font("Arial", "", 10)
        
        price_change = self.prediction['predicted_price'] - self.current_price
        pct_change = (price_change / self.current_price) * 100
        
        prediction_text = f"""
Predicted Price (7 days): ${self.prediction['predicted_price']:.2f}
Current Price: ${self.current_price:.2f}
Expected Change: ${price_change:+.2f} ({pct_change:+.2f}%)
Confidence Level: {self.prediction['confidence'].upper()}

Analysis:
{self.prediction['reasoning']}
        """
        
        self.pdf.multi_cell(0, 6, prediction_text.strip())
        self.pdf.ln(5)
    
    def add_analysis_section(self, news_analysis, price_analysis):
        """Add detailed analysis sections"""
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "News & Sentiment Analysis", ln=True)
        self.pdf.ln(3)
        
        self.pdf.set_font("Arial", "", 10)
        self.pdf.multi_cell(0, 6, news_analysis[:500] + "...")
        
        self.pdf.ln(5)
        
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "Price Trend Analysis", ln=True)
        self.pdf.ln(3)
        
        self.pdf.set_font("Arial", "", 10)
        self.pdf.multi_cell(0, 6, price_analysis[:500] + "...")
        
        self.pdf.ln(5)
    
    def add_footer(self):
        """Add footer with disclaimer"""
        self.pdf.set_font("Arial", "I", 8)
        self.pdf.ln(10)
        self.pdf.set_line_width(0.3)
        self.pdf.line(10, self.pdf.get_y(), 200, self.pdf.get_y())
        
        disclaimer = """⚠️ DISCLAIMER: This report is for informational purposes only and should not be considered 
financial advice. Past performance does not guarantee future results. Always consult with a licensed 
financial advisor before making investment decisions. The predictions made are based on historical data 
and current market sentiment and may not accurately reflect future price movements."""
        
        self.pdf.multi_cell(0, 3, disclaimer)
        self.pdf.cell(0, 5, "Powered by StockWise AI", align="C")
    
    def generate(self):
        """Generate and return PDF bytes"""
        pdf_buffer = io.BytesIO()
        # We'll save to file first, then read into buffer
        return self.pdf
    
    def get_pdf_bytes(self):
        """Return PDF as bytes for download"""
        return self.pdf.output(dest='S').encode('latin-1')


def create_stock_report(ticker, price_data, prediction, news_analysis, price_analysis):
    """
    Main function to create PDF report
    """
    report = StockReportPDF(
        ticker=ticker,
        current_price=price_data['current_price'],
        prediction=prediction
    )
    
    # Build PDF
    report.add_header()
    report.add_executive_summary(price_data, news_analysis)
    report.add_price_section(price_data)
    report.add_prediction_section()
    report.add_analysis_section(news_analysis, price_analysis)
    report.add_footer()
    
    # Return PDF bytes
    return report.get_pdf_bytes()
