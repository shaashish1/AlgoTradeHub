#!/usr/bin/env python3
"""
Risk Management Module
Advanced risk management features for algorithmic trading
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskManager:
    def __init__(self, config: Dict):
        """Initialize risk manager"""
        self.config = config
        self.max_portfolio_risk = config.get('max_portfolio_risk', 0.06)  # 6% max total risk
        self.max_position_size = config.get('max_position_size', 0.1)  # 10% per position
        self.max_correlation = config.get('max_correlation', 0.7)  # Max correlation between positions
        self.max_drawdown_limit = config.get('max_drawdown_limit', 0.15)  # 15% max drawdown
        
        # Performance tracking
        self.recent_trades = []
        self.portfolio_value_history = []
        self.open_positions = {}
        
        logger.info("Risk Manager initialized")
    
    def set_adaptive_stops(self, entry_price: float, atr: float, trend_strength: float, 
                          side: str = 'BUY') -> Tuple[float, float]:
        """Calculate adaptive stop loss and take profit levels"""
        try:
            if atr <= 0:
                atr = entry_price * 0.02  # 2% fallback
            
            # Base multipliers
            stop_multiplier = 2.0
            profit_multiplier = 4.0  # 1:2 risk/reward base
            
            # Adjust based on trend strength
            if trend_strength > 0.7:  # Strong trend
                stop_multiplier = 3.0  # Wider stops
                profit_multiplier = 6.0  # Higher targets
            elif trend_strength < 0.3:  # Weak trend
                stop_multiplier = 1.5  # Tighter stops
                profit_multiplier = 3.0  # Lower targets
            
            # Adjust based on volatility regime
            volatility_ratio = atr / entry_price
            
            if volatility_ratio > 0.05:  # High volatility
                stop_multiplier *= 1.5
                profit_multiplier *= 1.2
            elif volatility_ratio < 0.01:  # Low volatility
                stop_multiplier *= 0.8
                profit_multiplier *= 0.9
            
            # Calculate levels
            if side.upper() == 'BUY':
                stop_loss = entry_price - (stop_multiplier * atr)
                take_profit = entry_price + (profit_multiplier * atr)
            else:  # SELL
                stop_loss = entry_price + (stop_multiplier * atr)
                take_profit = entry_price - (profit_multiplier * atr)
            
            # Ensure reasonable bounds
            max_stop_distance = entry_price * 0.05  # 5% max stop
            min_stop_distance = entry_price * 0.005  # 0.5% min stop
            
            if side.upper() == 'BUY':
                stop_distance = entry_price - stop_loss
                stop_distance = max(min_stop_distance, min(stop_distance, max_stop_distance))
                stop_loss = entry_price - stop_distance
                
                # Ensure take profit maintains risk/reward ratio
                profit_distance = stop_distance * (profit_multiplier / stop_multiplier)
                take_profit = entry_price + profit_distance
            else:
                stop_distance = stop_loss - entry_price
                stop_distance = max(min_stop_distance, min(stop_distance, max_stop_distance))
                stop_loss = entry_price + stop_distance
                
                profit_distance = stop_distance * (profit_multiplier / stop_multiplier)
                take_profit = entry_price - profit_distance
            
            return stop_loss, take_profit
            
        except Exception as e:
            logger.error(f"Error calculating adaptive stops: {e}")
            # Fallback to simple percentage stops
            if side.upper() == 'BUY':
                return entry_price * 0.98, entry_price * 1.04  # 2% stop, 4% profit
            else:
                return entry_price * 1.02, entry_price * 0.96
    
    def calculate_trend_strength(self, df: pd.DataFrame) -> float:
        """Calculate trend strength indicator"""
        try:
            if len(df) < 20:
                return 0.5  # Neutral
            
            # Calculate multiple trend indicators
            close_prices = df['close'].values
            
            # 1. Price vs moving averages
            sma_20 = df['close'].rolling(20).mean().iloc[-1]
            sma_50 = df['close'].rolling(50).mean().iloc[-1] if len(df) >= 50 else sma_20
            current_price = close_prices[-1]
            
            ma_score = 0
            if current_price > sma_20 > sma_50:
                ma_score = 1.0  # Strong uptrend
            elif current_price < sma_20 < sma_50:
                ma_score = 1.0  # Strong downtrend
            elif current_price > sma_20:
                ma_score = 0.7  # Moderate uptrend
            elif current_price < sma_20:
                ma_score = 0.7  # Moderate downtrend
            else:
                ma_score = 0.3  # Sideways
            
            # 2. ADX-like calculation (simplified)
            high_low = df['high'] - df['low']
            high_close = abs(df['high'] - df['close'].shift(1))
            low_close = abs(df['low'] - df['close'].shift(1))
            
            true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            atr = true_range.rolling(14).mean().iloc[-1]
            
            price_change = abs(close_prices[-1] - close_prices[-14])
            directional_strength = price_change / (atr * 14) if atr > 0 else 0
            directional_strength = min(directional_strength, 1.0)
            
            # 3. Consecutive candles in same direction
            price_changes = np.diff(close_prices[-10:])  # Last 10 candles
            consecutive_score = 0
            
            if len(price_changes) > 0:
                positive_changes = sum(1 for change in price_changes if change > 0)
                negative_changes = sum(1 for change in price_changes if change < 0)
                
                if positive_changes >= 7:  # 7+ up candles
                    consecutive_score = 0.8
                elif negative_changes >= 7:  # 7+ down candles
                    consecutive_score = 0.8
                elif positive_changes >= 5 or negative_changes >= 5:
                    consecutive_score = 0.6
                else:
                    consecutive_score = 0.3
            
            # Combine scores
            trend_strength = (ma_score * 0.4 + directional_strength * 0.4 + consecutive_score * 0.2)
            return min(1.0, max(0.0, trend_strength))
            
        except Exception as e:
            logger.error(f"Error calculating trend strength: {e}")
            return 0.5
    
    def check_portfolio_heat(self, open_positions: Dict, new_trade_risk: float = 0) -> bool:
        """Check if portfolio risk is within limits"""
        try:
            total_risk = new_trade_risk
            
            # Calculate current portfolio risk
            for position_key, position in open_positions.items():
                # Calculate risk as distance to stop loss
                if hasattr(position, 'stop_loss') and hasattr(position, 'entry_price'):
                    if position.side.upper() == 'BUY':
                        risk_per_share = position.entry_price - position.stop_loss
                    else:
                        risk_per_share = position.stop_loss - position.entry_price
                    
                    position_risk = risk_per_share * position.quantity
                    total_risk += position_risk
            
            # Get current account balance
            account_balance = self.config.get('backtest', {}).get('initial_capital', 10000)
            
            # Check against maximum portfolio risk
            max_risk_amount = account_balance * self.max_portfolio_risk
            
            return total_risk <= max_risk_amount
            
        except Exception as e:
            logger.error(f"Error checking portfolio heat: {e}")
            return True  # Allow trade if error (conservative)
    
    def calculate_position_correlation(self, symbol1: str, symbol2: str, 
                                     lookback_days: int = 30) -> float:
        """Calculate correlation between two trading symbols"""
        try:
            # This would need historical price data for both symbols
            # For now, return a simplified correlation based on symbol similarity
            
            # Basic correlation rules
            if symbol1 == symbol2:
                return 1.0
            
            # Extract base currencies
            base1 = symbol1.split('/')[0] if '/' in symbol1 else symbol1[:3]
            base2 = symbol2.split('/')[0] if '/' in symbol2 else symbol2[:3]
            
            # High correlation pairs
            high_corr_pairs = [
                ('BTC', 'ETH'), ('ETH', 'BTC'),
                ('BTC', 'LTC'), ('LTC', 'BTC'),
                ('ETH', 'ETC'), ('ETC', 'ETH'),
            ]
            
            if (base1, base2) in high_corr_pairs:
                return 0.8
            
            # Same quote currency = moderate correlation
            quote1 = symbol1.split('/')[1] if '/' in symbol1 else 'USD'
            quote2 = symbol2.split('/')[1] if '/' in symbol2 else 'USD'
            
            if quote1 == quote2:
                return 0.4
            
            return 0.1  # Low correlation by default
            
        except Exception as e:
            logger.error(f"Error calculating correlation: {e}")
            return 0.0
    
    def check_position_correlation(self, new_symbol: str, existing_positions: Dict) -> bool:
        """Check if new position would create excessive correlation"""
        try:
            for position_key, position in existing_positions.items():
                existing_symbol = position.symbol if hasattr(position, 'symbol') else position_key.split('_')[1]
                
                correlation = self.calculate_position_correlation(new_symbol, existing_symbol)
                
                if correlation > self.max_correlation:
                    logger.warning(f"High correlation ({correlation:.2f}) between {new_symbol} and {existing_symbol}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking position correlation: {e}")
            return True  # Allow trade if error
    
    def calculate_current_drawdown(self, current_portfolio_value: float) -> float:
        """Calculate current drawdown from peak"""
        try:
            if not self.portfolio_value_history:
                return 0.0
            
            peak_value = max(self.portfolio_value_history)
            
            if peak_value <= 0:
                return 0.0
            
            drawdown = (peak_value - current_portfolio_value) / peak_value
            return max(0.0, drawdown)
            
        except Exception as e:
            logger.error(f"Error calculating drawdown: {e}")
            return 0.0
    
    def should_reduce_risk(self, current_portfolio_value: float) -> bool:
        """Determine if risk should be reduced due to drawdown"""
        try:
            current_drawdown = self.calculate_current_drawdown(current_portfolio_value)
            
            # Reduce risk if approaching maximum drawdown
            if current_drawdown > self.max_drawdown_limit * 0.8:  # 80% of max drawdown
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking risk reduction: {e}")
            return False
    
    def get_risk_adjusted_position_size(self, base_position_size: float, 
                                       current_portfolio_value: float) -> float:
        """Adjust position size based on current risk conditions"""
        try:
            # Start with base position size
            adjusted_size = base_position_size
            
            # Reduce size if high drawdown
            if self.should_reduce_risk(current_portfolio_value):
                current_drawdown = self.calculate_current_drawdown(current_portfolio_value)
                reduction_factor = 1.0 - (current_drawdown / self.max_drawdown_limit)
                adjusted_size *= max(0.1, reduction_factor)  # Minimum 10% of original size
            
            # Reduce size if too many open positions
            num_positions = len(self.open_positions)
            max_positions = self.config.get('max_positions', 5)
            
            if num_positions >= max_positions * 0.8:  # 80% of max positions
                position_factor = max_positions / (num_positions + 1)
                adjusted_size *= position_factor
            
            return adjusted_size
            
        except Exception as e:
            logger.error(f"Error adjusting position size: {e}")
            return base_position_size
    
    def update_portfolio_value(self, portfolio_value: float):
        """Update portfolio value history"""
        try:
            self.portfolio_value_history.append(portfolio_value)
            
            # Keep only last 1000 values to manage memory
            if len(self.portfolio_value_history) > 1000:
                self.portfolio_value_history = self.portfolio_value_history[-1000:]
                
        except Exception as e:
            logger.error(f"Error updating portfolio value: {e}")
    
    def add_trade(self, trade: Dict):
        """Add completed trade to history"""
        try:
            self.recent_trades.append(trade)
            
            # Keep only last 100 trades
            if len(self.recent_trades) > 100:
                self.recent_trades = self.recent_trades[-100:]
                
        except Exception as e:
            logger.error(f"Error adding trade: {e}")
    
    def get_risk_metrics(self) -> Dict:
        """Get current risk metrics"""
        try:
            if not self.portfolio_value_history:
                return {}
            
            current_value = self.portfolio_value_history[-1]
            peak_value = max(self.portfolio_value_history)
            current_drawdown = self.calculate_current_drawdown(current_value)
            
            # Calculate portfolio heat
            total_risk = 0
            for position in self.open_positions.values():
                if hasattr(position, 'risk_amount'):
                    total_risk += position.risk_amount
            
            account_balance = self.config.get('backtest', {}).get('initial_capital', 10000)
            portfolio_heat = (total_risk / account_balance) * 100 if account_balance > 0 else 0
            
            return {
                'current_drawdown': current_drawdown * 100,
                'max_drawdown_limit': self.max_drawdown_limit * 100,
                'portfolio_heat': portfolio_heat,
                'max_portfolio_risk': self.max_portfolio_risk * 100,
                'open_positions': len(self.open_positions),
                'max_positions': self.config.get('max_positions', 5),
                'peak_portfolio_value': peak_value,
                'current_portfolio_value': current_value
            }
            
        except Exception as e:
            logger.error(f"Error getting risk metrics: {e}")
            return {}
    
    def validate_trade(self, symbol: str, side: str, quantity: float, price: float,
                      stop_loss: float, take_profit: float) -> Tuple[bool, str]:
        """Validate if trade meets risk management criteria"""
        try:
            # Calculate trade risk
            if side.upper() == 'BUY':
                risk_per_share = price - stop_loss
            else:
                risk_per_share = stop_loss - price
            
            trade_risk = risk_per_share * quantity
            
            # Check portfolio heat
            if not self.check_portfolio_heat(self.open_positions, trade_risk):
                return False, "Portfolio risk limit exceeded"
            
            # Check position correlation
            if not self.check_position_correlation(symbol, self.open_positions):
                return False, "High correlation with existing positions"
            
            # Check position size limits
            account_balance = self.config.get('backtest', {}).get('initial_capital', 10000)
            position_value = quantity * price
            
            if position_value > account_balance * self.max_position_size:
                return False, "Position size exceeds maximum limit"
            
            # Check if risk/reward ratio is acceptable
            if side.upper() == 'BUY':
                reward_per_share = take_profit - price
            else:
                reward_per_share = price - take_profit
            
            if risk_per_share > 0:
                risk_reward_ratio = reward_per_share / risk_per_share
                if risk_reward_ratio < 1.5:  # Minimum 1.5:1 risk/reward
                    return False, "Risk/reward ratio too low"
            
            return True, "Trade validated"
            
        except Exception as e:
            logger.error(f"Error validating trade: {e}")
            return False, f"Validation error: {e}"