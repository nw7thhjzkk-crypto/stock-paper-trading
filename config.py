# ============================================
# PAPER TRADING CONFIGURATION - OPTIMIZED
# ============================================

# Virtual Capital
INITIAL_CAPITAL = 10000  # ₹10,000

# Stock Universe - TOP 20 MOST LIQUID NIFTY STOCKS
# Reduced from 50 to 20 for much faster API calls and better performance
# These are the most liquid, highest-volume stocks in NIFTY 50
NIFTY_50_SYMBOLS = [
    "RELIANCE.NS",   # Reliance Industries
    "TCS.NS",        # Tata Consultancy Services
    "HDFCBANK.NS",   # HDFC Bank
    "INFY.NS",       # Infosys
    "ICICIBANK.NS",  # ICICI Bank
    "HINDUNILVR.NS", # Hindustan Unilever
    "ITC.NS",        # ITC Limited
    "SBIN.NS",       # State Bank of India
    "BHARTIARTL.NS", # Bharti Airtel
    "KOTAKBANK.NS",  # Kotak Mahindra Bank
    "LT.NS",         # Larsen & Toubro
    "AXISBANK.NS",   # Axis Bank
    "BAJFINANCE.NS", # Bajaj Finance
    "MARUTI.NS",     # Maruti Suzuki
    "SUNPHARMA.NS",  # Sun Pharmaceutical
    "TITAN.NS",      # Titan Company
    "ULTRACEMCO.NS", # UltraTech Cement
    "NESTLEIND.NS",  # Nestle India
    "TATAMOTORS.NS", # Tata Motors
    "ASIANPAINT.NS", # Asian Paints
]

# Strategy Parameters
RSI_PERIOD = 14
RSI_OVERSOLD = 35      # Buy signal below this
RSI_OVERBOUGHT = 65   # Sell signal above this
MA_PERIOD = 20        # Moving average period

# Trading Settings
TIMEFRAME = "5m"      # 5-minute candles
UPDATE_INTERVAL = 10  # Seconds between updates (increased from 5 to reduce API load)
MAX_POSITION_SIZE = 2000  # Max ₹2000 per stock position

# Google Sheets (We'll fill this later)
GOOGLE_SHEETS_KEY = None  # Will be added after setup
