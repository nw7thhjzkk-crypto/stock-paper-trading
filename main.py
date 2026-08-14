# ============================================
# MAIN FLASK APPLICATION - PAPER TRADING SYSTEM
# ============================================

from flask import Flask, render_template, jsonify, request
import threading
import time
from datetime import datetime
import json
import os

from config import *
from strategy import *
from portfolio import Portfolio
from data_fetcher import *
from sheets_integration import GoogleSheetsManager

app = Flask(__name__)

# Global variables
portfolio = Portfolio(INITIAL_CAPITAL)
sheets_manager = GoogleSheetsManager()
trading_active = False
trading_thread = None
last_signals = {}
last_update_time = None
current_prices = {}

def trading_loop():
    """Main trading loop that runs in background"""
    global trading_active, last_signals, last_update_time, current_prices

    while trading_active:
        try:
            # Fetch current prices for all stocks
            current_prices = get_current_prices(NIFTY_50_SYMBOLS)

            # Check each stock for signals
            for symbol in NIFTY_50_SYMBOLS:
                if not trading_active:
                    break

                # Fetch detailed data for signal generation
                data = fetch_stock_data(symbol, TIMEFRAME, period="1d")

                if data is not None and len(data) > 0:
                    signal_details = get_signal_details(
                        data,
                        RSI_PERIOD,
                        RSI_OVERSOLD,
                        RSI_OVERBOUGHT,
                        MA_PERIOD
                    )

                    if signal_details:
                        signal_details['symbol'] = symbol
                        last_signals[symbol] = signal_details

                        # Execute trades based on signal
                        if signal_details['signal'] == 'BUY':
                            # Check if we already have this stock
                            if symbol not in portfolio.holdings:
                                success, message = portfolio.buy(
                                    symbol,
                                    signal_details['price'],
                                    max_investment=MAX_POSITION_SIZE
                                )
                                if success:
                                    print(f"✅ {message}")
                                    sheets_manager.log_trade(portfolio.trade_history[-1])
                                    sheets_manager.log_signal(signal_details)

                        elif signal_details['signal'] == 'SELL':
                            # Check if we have this stock
                            if symbol in portfolio.holdings:
                                success, message = portfolio.sell(
                                    symbol,
                                    signal_details['price']
                                )
                                if success:
                                    print(f"💰 {message}")
                                    sheets_manager.log_trade(portfolio.trade_history[-1])
                                    sheets_manager.log_signal(signal_details)

                time.sleep(0.5)  # Delay between stocks

            # Update portfolio in Google Sheets
            portfolio_summary = portfolio.get_summary(current_prices)
            sheets_manager.update_portfolio(portfolio_summary)

            last_update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Wait for next update
            time.sleep(UPDATE_INTERVAL)

        except Exception as e:
            print(f"Error in trading loop: {e}")
            time.sleep(UPDATE_INTERVAL)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """API endpoint for current status"""
    portfolio_summary = portfolio.get_summary(current_prices)

    return jsonify({
        'trading_active': trading_active,
        'last_update': last_update_time,
        'portfolio': portfolio_summary,
        'signals': last_signals,
        'current_prices': current_prices,
        'market_status': get_market_status()
    })

@app.route('/api/start')
def start_trading():
    """Start paper trading"""
    global trading_active, trading_thread

    if not trading_active:
        trading_active = True
        trading_thread = threading.Thread(target=trading_loop)
        trading_thread.daemon = True
        trading_thread.start()

        return jsonify({'status': 'started', 'message': 'Paper trading started!'})
    else:
        return jsonify({'status': 'already_running', 'message': 'Trading already active'})

@app.route('/api/stop')
def stop_trading():
    """Stop paper trading"""
    global trading_active

    if trading_active:
        trading_active = False
        return jsonify({'status': 'stopped', 'message': 'Paper trading stopped!'})
    else:
        return jsonify({'status': 'not_running', 'message': 'Trading not active'})

@app.route('/api/reset')
def reset_portfolio():
    """Reset portfolio to initial state"""
    global portfolio

    portfolio = Portfolio(INITIAL_CAPITAL)
    return jsonify({'status': 'reset', 'message': 'Portfolio reset to ₹10,000'})

@app.route('/api/trades')
def get_trades():
    """Get trade history"""
    return jsonify(portfolio.trade_history)

@app.route('/api/portfolio')
def get_portfolio():
    """Get current portfolio"""
    return jsonify(portfolio.get_summary(current_prices))

@app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    # Create Google Sheets if connected
    if sheets_manager.is_connected:
        sheets_manager.create_spreadsheet()

    # Start Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
