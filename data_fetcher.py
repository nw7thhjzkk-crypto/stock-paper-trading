# ============================================
# DATA FETCHER - LIVE STOCK DATA FROM YAHOO FINANCE
# ============================================

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time

def fetch_stock_data(symbol, timeframe="5m", period="1d"):
    """
    Fetch stock data from Yahoo Finance
    
    Args:
        symbol: Stock symbol (e.g., RELIANCE.NS)
        timeframe: Time interval (1m, 5m, 15m, 1h, 1d)
        period: Data period (1d, 5d, 1mo, 3mo)
    
    Returns:
        DataFrame with OHLCV data or None if error
    """
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period, interval=timeframe)
        
        if data is not None and len(data) > 0:
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def fetch_multiple_stocks(symbols, timeframe="5m"):
    """
    Fetch data for multiple stocks
    
    Args:
        symbols: List of stock symbols
        timeframe: Time interval
    
    Returns:
        Dictionary: {symbol: DataFrame}
    """
    data_dict = {}
    failed_symbols = []
    
    for symbol in symbols:
        try:
            data = fetch_stock_data(symbol, timeframe)
            if data is not None and len(data) > 0:
                data_dict[symbol] = data
            else:
                failed_symbols.append(symbol)
        except:
            failed_symbols.append(symbol)
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
    
    return data_dict, failed_symbols

def get_current_prices(symbols):
    """
    Get current prices for multiple stocks quickly
    
    Args:
        symbols: List of stock symbols
    
    Returns:
        Dictionary: {symbol: current_price}
    """
    prices = {}
    
    try:
        for symbol in symbols:
            stock = yf.Ticker(symbol)
            history = stock.history(period="1d", interval="1m")
            
            if history is not None and len(history) > 0:
                prices[symbol] = history['Close'].iloc[-1]
            
            time.sleep(0.3)  # Rate limiting protection
    
    except Exception as e:
        print(f"Error fetching prices: {e}")
    
    return prices

def get_stock_info(symbol):
    """
    Get basic stock information
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        return {
            'symbol': symbol,
            'name': info.get('longName', symbol),
            'sector': info.get('sector', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'previous_close': info.get('previousClose', 0),
            'open': info.get('open', 0),
            'day_high': info.get('dayHigh', 0),
            'day_low': info.get('dayLow', 0)
        }
    except:
        return {
            'symbol': symbol,
            'name': symbol,
            'sector': 'N/A',
            'market_cap': 0,
            'previous_close': 0,
            'open': 0,
            'day_high': 0,
            'day_low': 0
        }

def get_market_status():
    """
    Check if Indian market is open
    Market hours: 9:15 AM - 3:30 PM IST (Mon-Fri)
    """
    now = datetime.now()
    
    # Check if weekday
    if now.weekday() >= 5:  # Saturday=5, Sunday=6
        return False, "Market closed (Weekend)"
    
    # Check market hours
    current_time = now.strftime("%H:%M")
    if "09:15" <= current_time <= "15:30":
        return True, "Market open"
    else:
        return False, f"Market closed (Time: {current_time} IST)"
