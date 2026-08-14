# ============================================
# PORTFOLIO MANAGEMENT - VIRTUAL MONEY
# ============================================

import json
from datetime import datetime
import os

class Portfolio:
    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.holdings = {}  # symbol: {'quantity': int, 'avg_price': float}
        self.trade_history = []
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.load_state()
    
    def load_state(self):
        """Load portfolio state from file if exists"""
        try:
            if os.path.exists('portfolio_state.json'):
                with open('portfolio_state.json', 'r') as f:
                    state = json.load(f)
                    self.cash = state.get('cash', self.initial_capital)
                    self.holdings = state.get('holdings', {})
                    self.trade_history = state.get('trade_history', [])
                    self.total_trades = state.get('total_trades', 0)
                    self.winning_trades = state.get('winning_trades', 0)
                    self.losing_trades = state.get('losing_trades', 0)
        except:
            pass
    
    def save_state(self):
        """Save portfolio state to file"""
        state = {
            'cash': self.cash,
            'holdings': self.holdings,
            'trade_history': self.trade_history[-100:],  # Keep last 100 trades
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades
        }
        with open('portfolio_state.json', 'w') as f:
            json.dump(state, f)
    
    def buy(self, symbol, price, quantity=None, max_investment=2000):
        """Execute a virtual buy order"""
        if quantity is None:
            # Calculate quantity based on max investment
            quantity = int(max_investment / price)
        
        if quantity <= 0:
            return False, "Invalid quantity"
        
        total_cost = price * quantity
        
        if total_cost > self.cash:
            return False, f"Insufficient cash. Need ₹{total_cost:.2f}, have ₹{self.cash:.2f}"
        
        # Update holdings
        if symbol in self.holdings:
            old_qty = self.holdings[symbol]['quantity']
            old_avg = self.holdings[symbol]['avg_price']
            new_qty = old_qty + quantity
            new_avg = ((old_avg * old_qty) + (price * quantity)) / new_qty
            self.holdings[symbol] = {'quantity': new_qty, 'avg_price': new_avg}
        else:
            self.holdings[symbol] = {'quantity': quantity, 'avg_price': price}
        
        # Update cash
        self.cash -= total_cost
        
        # Record trade
        trade = {
            'type': 'BUY',
            'symbol': symbol,
            'price': price,
            'quantity': quantity,
            'total': total_cost,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.trade_history.append(trade)
        
        self.save_state()
        return True, f"Bought {quantity} shares of {symbol} at ₹{price:.2f}"
    
    def sell(self, symbol, price, quantity=None):
        """Execute a virtual sell order"""
        if symbol not in self.holdings:
            return False, f"No holdings for {symbol}"
        
        if quantity is None:
            quantity = self.holdings[symbol]['quantity']
        
        if quantity <= 0 or quantity > self.holdings[symbol]['quantity']:
            return False, "Invalid quantity"
        
        # Calculate profit/loss
        avg_price = self.holdings[symbol]['avg_price']
        total_sale = price * quantity
        profit_loss = (price - avg_price) * quantity
        
        # Update holdings
        remaining_qty = self.holdings[symbol]['quantity'] - quantity
        if remaining_qty <= 0:
            del self.holdings[symbol]
        else:
            self.holdings[symbol]['quantity'] = remaining_qty
        
        # Update cash
        self.cash += total_sale
        
        # Update trade statistics
        self.total_trades += 1
        if profit_loss > 0:
            self.winning_trades += 1
        else:
            self.losing_trades += 1
        
        # Record trade
        trade = {
            'type': 'SELL',
            'symbol': symbol,
            'price': price,
            'quantity': quantity,
            'total': total_sale,
            'profit_loss': profit_loss,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.trade_history.append(trade)
        
        self.save_state()
        return True, f"Sold {quantity} shares of {symbol} at ₹{price:.2f}, P&L: ₹{profit_loss:.2f}"
    
    def get_total_value(self, current_prices):
        """Calculate total portfolio value"""
        holdings_value = 0
        for symbol, data in self.holdings.items():
            if symbol in current_prices:
                holdings_value += data['quantity'] * current_prices[symbol]
        return self.cash + holdings_value
    
    def get_holdings_value(self, current_prices):
        """Calculate holdings value"""
        holdings_value = 0
        for symbol, data in self.holdings.items():
            if symbol in current_prices:
                holdings_value += data['quantity'] * current_prices[symbol]
        return holdings_value
    
    def get_profit_loss(self, current_prices):
        """Calculate total profit/loss"""
        total_value = self.get_total_value(current_prices)
        return total_value - self.initial_capital
    
    def get_win_rate(self):
        """Calculate win rate"""
        if self.total_trades == 0:
            return 0
        return (self.winning_trades / self.total_trades) * 100
    
    def get_summary(self, current_prices=None):
        """Get portfolio summary"""
        if current_prices is None:
            current_prices = {}
        
        total_value = self.get_total_value(current_prices)
        profit_loss = self.get_profit_loss(current_prices)
        
        return {
            'initial_capital': self.initial_capital,
            'cash': round(self.cash, 2),
            'holdings_value': round(self.get_holdings_value(current_prices), 2),
            'total_value': round(total_value, 2),
            'profit_loss': round(profit_loss, 2),
            'profit_loss_percent': round((profit_loss / self.initial_capital) * 100, 2),
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
            'win_rate': round(self.get_win_rate(), 2),
            'holdings': self.holdings,
            'recent_trades': self.trade_history[-10:]  # Last 10 trades
        }
