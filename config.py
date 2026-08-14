# ============================================
# PAPER TRADING CONFIGURATION
# ============================================

# Virtual Capital
INITIAL_CAPITAL = 10000  # ₹10,000

# Stock Universe - NIFTY 50
NIFTY_50_SYMBOLS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS",
    "LT.NS", "AXISBANK.NS", "BAJFINANCE.NS", "MARUTI.NS", "SUNPHARMA.NS",
    "TITAN.NS", "ULTRACEMCO.NS", "NESTLEIND.NS", "WIPRO.NS", "ADANIENT.NS",
    "NTPC.NS", "POWERGRID.NS", "M&M.NS", "TATAMOTORS.NS", "TATASTEEL.NS",
    "JSWSTEEL.NS", "TECHM.NS", "HCLTECH.NS", "ASIANPAINT.NS", "GRASIM.NS",
    "INDUSINDBK.NS", "BAJAJFINSV.NS", "HDFCLIFE.NS", "SBILIFE.NS", "DRREDDY.NS",
    "CIPLA.NS", "APOLLOHOSP.NS", "DIVISLAB.NS", "EICHERMOT.NS", "HEROMOTOCO.NS",
    "BRITANNIA.NS", "COALINDIA.NS", "ONGC.NS", "BPCL.NS", "HINDALCO.NS",
    "UPL.NS", "TATACONSUM.NS", "ADANIPORTS.NS", "BAJAJ-AUTO.NS", "SHRIRAMFIN.NS"
]

# Strategy Parameters
RSI_PERIOD = 14
RSI_OVERSOLD = 35  # Buy signal below this
RSI_OVERBOUGHT = 65  # Sell signal above this
MA_PERIOD = 20  # Moving average period

# Trading Settings
TIMEFRAME = "5m"  # 5-minute candles
UPDATE_INTERVAL = 5  # Seconds between updates
MAX_POSITION_SIZE = 2000  # Max ₹2000 per stock position

# Google Sheets (We'll fill this later)
GOOGLE_SHEETS_KEY = None  # Will be added after setup
