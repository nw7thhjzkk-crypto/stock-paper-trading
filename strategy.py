# ============================================
# TRADING STRATEGY - RSI + MOVING AVERAGE
# ============================================

import pandas as pd
import numpy as np

def calculate_rsi(data, period=14):
    """Calculate RSI indicator"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_ma(data, period=20):
    """Calculate Moving Average"""
    return data['Close'].rolling(window=period).mean()

def generate_signal(data, rsi_period=14, rsi_oversold=35, rsi_overbought=65, ma_period=20):
    """
    Generate buy/sell signals based on RSI + MA strategy
    
    BUY Signal: RSI < Oversold AND Price > MA
    SELL Signal: RSI > Overbought OR Price < MA
    
    Returns: 'BUY', 'SELL', or 'HOLD'
    """
    if data is None or len(data) < max(rsi_period, ma_period) + 1:
        return 'HOLD'
    
    # Calculate indicators
    rsi = calculate_rsi(data, rsi_period)
    ma = calculate_ma(data, ma_period)
    
    # Get latest values
    current_rsi = rsi.iloc[-1]
    current_ma = ma.iloc[-1]
    current_price = data['Close'].iloc[-1]
    
    # Generate signal
    if current_rsi < rsi_oversold and current_price > current_ma:
        return 'BUY'
    elif current_rsi > rsi_overbought or current_price < current_ma:
        return 'SELL'
    else:
        return 'HOLD'

def get_signal_details(data, rsi_period=14, rsi_oversold=35, rsi_overbought=65, ma_period=20):
    """
    Get detailed signal information for dashboard display
    """
    if data is None or len(data) < max(rsi_period, ma_period) + 1:
        return None
    
    rsi = calculate_rsi(data, rsi_period)
    ma = calculate_ma(data, ma_period)
    
    current_rsi = rsi.iloc[-1]
    current_ma = ma.iloc[-1]
    current_price = data['Close'].iloc[-1]
    previous_price = data['Close'].iloc[-2]
    
    signal = generate_signal(data, rsi_period, rsi_oversold, rsi_overbought, ma_period)
    
    return {
        'price': round(current_price, 2),
        'rsi': round(current_rsi, 2),
        'ma': round(current_ma, 2),
        'signal': signal,
        'change_percent': round(((current_price - previous_price) / previous_price) * 100, 2)
    }
