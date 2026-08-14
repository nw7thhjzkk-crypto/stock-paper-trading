# ============================================
# GOOGLE SHEETS INTEGRATION
# ============================================

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import os

class GoogleSheetsManager:
    def __init__(self):
        self.client = None
        self.spreadsheet = None
        self.is_connected = False
        self.setup_connection()
    
    def setup_connection(self):
        """Setup Google Sheets connection using service account"""
        try:
            # Check if credentials file exists
            if os.path.exists('google_credentials.json'):
                scopes = [
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ]
                
                credentials = Credentials.from_service_account_file(
                    'google_credentials.json',
                    scopes=scopes
                )
                
                self.client = gspread.authorize(credentials)
                self.is_connected = True
                print("✅ Google Sheets connected")
            else:
                print("⚠️ Google Sheets credentials not found. Will work without Sheets sync.")
        except Exception as e:
            print(f"⚠️ Google Sheets connection failed: {e}")
            self.is_connected = False
    
    def create_spreadsheet(self, title="Paper Trading Dashboard"):
        """Create a new spreadsheet"""
        if not self.is_connected:
            return None
        
        try:
            self.spreadsheet = self.client.create(title)
            
            # Create worksheets
            worksheet1 = self.spreadsheet.get_worksheet(0)
            worksheet1.update_title("Live Signals")
            
            worksheet2 = self.spreadsheet.add_worksheet(title="Trade History", rows=1000, cols=10)
            worksheet3 = self.spreadsheet.add_worksheet(title="Portfolio", rows=100, cols=10)
            worksheet4 = self.spreadsheet.add_worksheet(title="Performance", rows=100, cols=10)
            
            # Setup headers
            self.setup_headers()
            
            return self.spreadsheet
        except Exception as e:
            print(f"Error creating spreadsheet: {e}")
            return None
    
    def setup_headers(self):
        """Setup worksheet headers"""
        if not self.is_connected or not self.spreadsheet:
            return
        
        try:
            # Live Signals headers
            signals_ws = self.spreadsheet.worksheet("Live Signals")
            signals_headers = ["Timestamp", "Symbol", "Price", "RSI", "MA", "Signal", "Change %"]
            signals_ws.insert_row(signals_headers, 1)
            
            # Trade History headers
            trades_ws = self.spreadsheet.worksheet("Trade History")
            trades_headers = ["Timestamp", "Type", "Symbol", "Price", "Quantity", "Total", "P&L"]
            trades_ws.insert_row(trades_headers, 1)
            
            # Portfolio headers
            portfolio_ws = self.spreadsheet.worksheet("Portfolio")
            portfolio_headers = ["Timestamp", "Cash", "Holdings Value", "Total Value", "P&L", "P&L %", "Win Rate"]
            portfolio_ws.insert_row(portfolio_headers, 1)
            
            # Performance headers
            perf_ws = self.spreadsheet.worksheet("Performance")
            perf_headers = ["Metric", "Value"]
            perf_ws.insert_row(perf_headers, 1)
            
        except Exception as e:
            print(f"Error setting up headers: {e}")
    
    def log_signal(self, signal_data):
        """Log a trading signal to Google Sheets"""
        if not self.is_connected or not self.spreadsheet:
            return
        
        try:
            signals_ws = self.spreadsheet.worksheet("Live Signals")
            row = [
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                signal_data.get('symbol', ''),
                signal_data.get('price', 0),
                signal_data.get('rsi', 0),
                signal_data.get('ma', 0),
                signal_data.get('signal', ''),
                signal_data.get('change_percent', 0)
            ]
            signals_ws.append_row(row)
        except Exception as e:
            print(f"Error logging signal: {e}")
    
    def log_trade(self, trade_data):
        """Log a trade to Google Sheets"""
        if not self.is_connected or not self.spreadsheet:
            return
        
        try:
            trades_ws = self.spreadsheet.worksheet("Trade History")
            row = [
                trade_data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                trade_data.get('type', ''),
                trade_data.get('symbol', ''),
                trade_data.get('price', 0),
                trade_data.get('quantity', 0),
                trade_data.get('total', 0),
                trade_data.get('profit_loss', 0)
            ]
            trades_ws.append_row(row)
        except Exception as e:
            print(f"Error logging trade: {e}")
    
    def update_portfolio(self, portfolio_summary):
        """Update portfolio data in Google Sheets"""
        if not self.is_connected or not self.spreadsheet:
            return
        
        try:
            portfolio_ws = self.spreadsheet.worksheet("Portfolio")
            row = [
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                portfolio_summary.get('cash', 0),
                portfolio_summary.get('holdings_value', 0),
                portfolio_summary.get('total_value', 0),
                portfolio_summary.get('profit_loss', 0),
                portfolio_summary.get('profit_loss_percent', 0),
                portfolio_summary.get('win_rate', 0)
            ]
            portfolio_ws.append_row(row)
        except Exception as e:
            print(f"Error updating portfolio: {e}")
    
    def update_performance(self, metrics):
        """Update performance metrics"""
        if not self.is_connected or not self.spreadsheet:
            return
        
        try:
            perf_ws = self.spreadsheet.worksheet("Performance")
            perf_ws.clear()
            perf_ws.insert_row(["Metric", "Value"], 1)
            
            for key, value in metrics.items():
                perf_ws.append_row([key, value])
        except Exception as e:
            print(f"Error updating performance: {e}")
