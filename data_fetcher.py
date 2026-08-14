# ============================================
# DATA FETCHER - OPTIMIZED BATCH FETCHING
# ============================================

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import threading
from functools import lru_cache

# Cache for stock data to avoid re-fetching every cycle
_data_cache = {}
_cache_lock = threading.Lock()
_cache_ttl = 60  # seconds


def fetch_stock_data(symbol, timeframe="5m", period="1d"):
    """
    Fetch stock data from Yahoo Finance with caching
    """
    cache_key = f"{symbol}_{timeframe}_{period}"

    # Check cache first
    with _cache_lock:
        if cache_key in _data_cache:
            cached_time, cached_data = _data_cache[cache_key]
            if time.time() - cached_time < _cache_ttl:
                return cached_data

    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period, interval=timeframe)

        if data is not None and len(data) > 0:
            # Update cache
            with _cache_lock:
                _data_cache[cache_key] = (time.time(), data)
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None


def get_current_prices(symbols):
    """
    Get current prices for multiple stocks using BATCH download (single API call)
    MUCH faster than fetching one by one
    """
    prices = {}

    if not symbols:
        return prices

    try:
        # Use yfinance batch download - fetches all tickers in ONE API call
        # This is dramatically faster than individual Ticker calls
        tickers_str = " ".join(symbols)
        data = yf.download(
            tickers=tickers_str,
            period="1d",
            interval="1m",
            group_by='ticker',
            progress=False,
            threads=True  # Use threading for even faster fetching
        )

        if data is not None and len(data) > 0:
            if len(symbols) == 1:
                # Single ticker returns flat DataFrame
                symbol = symbols[0]
                if 'Close' in data.columns and len(data) > 0:
                    prices[symbol] = float(data['Close'].iloc[-1])
            else:
                # Multiple tickers returns MultiIndex DataFrame
                for symbol in symbols:
                    try:
                        if symbol in data.columns.get_level_values(0):
                            close_prices = data[symbol]['Close'].dropna()
                            if len(close_prices) > 0:
                                prices[symbol] = float(close_prices.iloc[-1])
                    except Exception:
                        pass  # Skip symbols that failed

    except Exception as e:
        print(f"Error in batch price fetch: {e}")
        # Fallback: try individual fetches for missing symbols
        for symbol in symbols:
            if symbol not in prices:
                try:
                    stock = yf.Ticker(symbol)
                    hist = stock.history(period="1d", interval="1m")
                    if hist is not None and len(hist) > 0:
                        prices[symbol] = float(hist['Close'].iloc[-1])
                        time.sleep(0.1)
                except Exception:
                    pass

    return prices


def get_stock_info(symbol):
    """Get basic stock information"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.fast_info  # fast_info is much quicker than .info

        return {
            'symbol': symbol,
            'name': getattr(info, 'longName', symbol),
            'sector': getattr(info, 'sector', 'N/A'),
            'market_cap': getattr(info, 'marketCap', 0),
            'previous_close': getattr(info, 'previousClose', 0),
            'open': getattr(info, 'open', 0),
            'day_high': getattr(info, 'dayHigh', 0),
            'day_low': getattr(info, 'dayLow', 0)
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
