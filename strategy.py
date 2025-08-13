#!/usr/bin/env python3
"""
Trading Strategy Module
Implements various trading strategies for backtesting and live trading
"""

import pandas as pd
import numpy as np
import ta
from typing import Dict, Optional, List
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradingStrategy:
    def __init__(self, config: Dict):
        """Initialize trading strategy"""
        self.config = config
        self.strategy_config = config.get('strategy', {})
        self.strategy_name = self.strategy_config.get('name', 'rsi_strategy')
        self.parameters = self.strategy_config.get('parameters', {})
        
        # Default parameters
        self.rsi_period = self.parameters.get('rsi_period', 14)
        self.rsi_overbought = self.parameters.get('rsi_overbought', 70)
        self.rsi_oversold = self.parameters.get('rsi_oversold', 30)
        self.sma_period = self.parameters.get('sma_period', 20)
        self.volume_threshold = self.parameters.get('volume_threshold', 1000000)
        
        logger.info(f"Initialized {self.strategy_name} strategy")
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators"""
        try:
            # Make a copy to avoid modifying original data
            data = df.copy()
            
            # RSI
            data['rsi'] = ta.momentum.RSIIndicator(
                close=data['close'], 
                window=self.rsi_period
            ).rsi()
            
            # Simple Moving Average
            data['sma'] = ta.trend.SMAIndicator(
                close=data['close'],
                window=self.sma_period
            ).sma_indicator()
            
            # Exponential Moving Average
            data['ema'] = ta.trend.EMAIndicator(
                close=data['close'],
                window=self.sma_period
            ).ema_indicator()
            
            # Bollinger Bands
            bb_indicator = ta.volatility.BollingerBands(
                close=data['close'],
                window=20,
                window_dev=2
            )
            data['bb_upper'] = bb_indicator.bollinger_hband()
            data['bb_lower'] = bb_indicator.bollinger_lband()
            data['bb_middle'] = bb_indicator.bollinger_mavg()
            
            # MACD
            macd_indicator = ta.trend.MACD(
                close=data['close'],
                window_slow=26,
                window_fast=12,
                window_sign=9
            )
            data['macd'] = macd_indicator.macd()
            data['macd_signal'] = macd_indicator.macd_signal()
            data['macd_histogram'] = macd_indicator.macd_diff()
            
            # Volume indicators
            data['volume_sma'] = data['volume'].rolling(window=20).mean()
            
            # Stochastic Oscillator
            stoch_indicator = ta.momentum.StochasticOscillator(
                high=data['high'],
                low=data['low'],
                close=data['close'],
                window=14,
                smooth_window=3
            )
            data['stoch_k'] = stoch_indicator.stoch()
            data['stoch_d'] = stoch_indicator.stoch_signal()
            
            # Average True Range (ATR)
            data['atr'] = ta.volatility.AverageTrueRange(
                high=data['high'],
                low=data['low'],
                close=data['close'],
                window=14
            ).average_true_range()
            
            return data
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return df
    
    def rsi_strategy(self, df: pd.DataFrame) -> Optional[Dict]:
        """RSI-based trading strategy"""
        try:
            if len(df) < self.rsi_period:
                return None
            
            # Get latest values
            latest = df.iloc[-1]
            previous = df.iloc[-2]
            
            current_rsi = latest['rsi']
            previous_rsi = previous['rsi']
            current_price = latest['close']
            current_volume = latest['volume']
            
            # Check for valid RSI values
            if pd.isna(current_rsi) or pd.isna(previous_rsi):
                return None
            
            # Buy signal: RSI crosses above oversold level
            if (previous_rsi <= self.rsi_oversold and 
                current_rsi > self.rsi_oversold and 
                current_volume > self.volume_threshold):
                
                return {
                    'action': 'BUY',
                    'price': current_price,
                    'timestamp': latest.name,
                    'rsi': current_rsi,
                    'volume': current_volume,
                    'signal_strength': min(100, (self.rsi_oversold - previous_rsi) * 2)
                }
            
            # Sell signal: RSI crosses below overbought level
            elif (previous_rsi >= self.rsi_overbought and 
                  current_rsi < self.rsi_overbought):
                
                return {
                    'action': 'SELL',
                    'price': current_price,
                    'timestamp': latest.name,
                    'rsi': current_rsi,
                    'volume': current_volume,
                    'signal_strength': min(100, (previous_rsi - self.rsi_overbought) * 2)
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error in RSI strategy: {e}")
            return None
    
    def macd_strategy(self, df: pd.DataFrame) -> Optional[Dict]:
        """MACD-based trading strategy"""
        try:
            if len(df) < 26:  # Need at least 26 periods for MACD
                return None
            
            # Get latest values
            latest = df.iloc[-1]
            previous = df.iloc[-2]
            
            current_macd = latest['macd']
            current_signal = latest['macd_signal']
            previous_macd = previous['macd']
            previous_signal = previous['macd_signal']
            
            current_price = latest['close']
            current_volume = latest['volume']
            
            # Check for valid MACD values
            if pd.isna(current_macd) or pd.isna(current_signal):
                return None
            
            # Buy signal: MACD crosses above signal line
            if (previous_macd <= previous_signal and 
                current_macd > current_signal and
                current_volume > self.volume_threshold):
                
                return {
                    'action': 'BUY',
                    'price': current_price,
                    'timestamp': latest.name,
                    'macd': current_macd,
                    'macd_signal': current_signal,
                    'volume': current_volume,
                    'signal_strength': min(100, abs(current_macd - current_signal) * 100)
                }
            
            # Sell signal: MACD crosses below signal line
            elif (previous_macd >= previous_signal and 
                  current_macd < current_signal):
                
                return {
                    'action': 'SELL',
                    'price': current_price,
                    'timestamp': latest.name,
                    'macd': current_macd,
                    'macd_signal': current_signal,
                    'volume': current_volume,
                    'signal_strength': min(100, abs(current_macd - current_signal) * 100)
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error in MACD strategy: {e}")
            return None
    
    def bollinger_strategy(self, df: pd.DataFrame) -> Optional[Dict]:
        """Bollinger Bands strategy"""
        try:
            if len(df) < 20:  # Need at least 20 periods for Bollinger Bands
                return None
            
            # Get latest values
            latest = df.iloc[-1]
            previous = df.iloc[-2]
            
            current_price = latest['close']
            current_volume = latest['volume']
            bb_upper = latest['bb_upper']
            bb_lower = latest['bb_lower']
            bb_middle = latest['bb_middle']
            
            previous_price = previous['close']
            
            # Check for valid Bollinger values
            if pd.isna(bb_upper) or pd.isna(bb_lower) or pd.isna(bb_middle):
                return None
            
            # Buy signal: Price touches lower band and bounces
            if (previous_price <= bb_lower and 
                current_price > bb_lower and
                current_volume > self.volume_threshold):
                
                return {
                    'action': 'BUY',
                    'price': current_price,
                    'timestamp': latest.name,
                    'bb_position': (current_price - bb_lower) / (bb_upper - bb_lower),
                    'volume': current_volume,
                    'signal_strength': min(100, (bb_middle - current_price) / (bb_middle - bb_lower) * 100)
                }
            
            # Sell signal: Price touches upper band
            elif (previous_price >= bb_upper and 
                  current_price < bb_upper):
                
                return {
                    'action': 'SELL',
                    'price': current_price,
                    'timestamp': latest.name,
                    'bb_position': (current_price - bb_lower) / (bb_upper - bb_lower),
                    'volume': current_volume,
                    'signal_strength': min(100, (current_price - bb_middle) / (bb_upper - bb_middle) * 100)
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error in Bollinger strategy: {e}")
            return None
    
    def multi_indicator_strategy(self, df: pd.DataFrame) -> Optional[Dict]:
        """Multi-indicator strategy combining RSI, MACD, and Bollinger Bands"""
        try:
            if len(df) < 26:  # Need at least 26 periods for all indicators
                return None
            
            # Get individual strategy signals
            rsi_signal = self.rsi_strategy(df)
            macd_signal = self.macd_strategy(df)
            bb_signal = self.bollinger_strategy(df)
            
            # Count signals
            buy_signals = sum([1 for signal in [rsi_signal, macd_signal, bb_signal] 
                              if signal and signal['action'] == 'BUY'])
            sell_signals = sum([1 for signal in [rsi_signal, macd_signal, bb_signal] 
                               if signal and signal['action'] == 'SELL'])
            
            latest = df.iloc[-1]
            current_price = latest['close']
            current_volume = latest['volume']
            
            # Require at least 2 indicators to agree
            if buy_signals >= 2:
                # Calculate combined signal strength
                strengths = [signal['signal_strength'] for signal in [rsi_signal, macd_signal, bb_signal] 
                            if signal and signal['action'] == 'BUY']
                avg_strength = np.mean(strengths) if strengths else 50
                
                return {
                    'action': 'BUY',
                    'price': current_price,
                    'timestamp': latest.name,
                    'volume': current_volume,
                    'signal_strength': avg_strength,
                    'indicators_count': buy_signals,
                    'rsi_signal': rsi_signal is not None and rsi_signal['action'] == 'BUY',
                    'macd_signal': macd_signal is not None and macd_signal['action'] == 'BUY',
                    'bb_signal': bb_signal is not None and bb_signal['action'] == 'BUY'
                }
            
            elif sell_signals >= 2:
                # Calculate combined signal strength
                strengths = [signal['signal_strength'] for signal in [rsi_signal, macd_signal, bb_signal] 
                            if signal and signal['action'] == 'SELL']
                avg_strength = np.mean(strengths) if strengths else 50
                
                return {
                    'action': 'SELL',
                    'price': current_price,
                    'timestamp': latest.name,
                    'volume': current_volume,
                    'signal_strength': avg_strength,
                    'indicators_count': sell_signals,
                    'rsi_signal': rsi_signal is not None and rsi_signal['action'] == 'SELL',
                    'macd_signal': macd_signal is not None and macd_signal['action'] == 'SELL',
                    'bb_signal': bb_signal is not None and bb_signal['action'] == 'SELL'
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error in multi-indicator strategy: {e}")
            return None
    
    def sma_crossover_strategy(self, df: pd.DataFrame) -> Optional[Dict]:
        """Simple Moving Average Crossover Strategy"""
        try:
            if len(df) < 50:
                return None
            
            # Calculate SMAs
            df['sma_short'] = ta.trend.sma_indicator(df['close'], window=10)
            df['sma_long'] = ta.trend.sma_indicator(df['close'], window=30)
            
            # Get current and previous values
            current_short = df['sma_short'].iloc[-1]
            current_long = df['sma_long'].iloc[-1]
            prev_short = df['sma_short'].iloc[-2]
            prev_long = df['sma_long'].iloc[-2]
            
            latest = df.iloc[-1]
            current_price = latest['close']
            current_volume = latest['volume']
            
            # Check for crossover
            if prev_short <= prev_long and current_short > current_long:
                return {
                    'action': 'BUY',
                    'price': current_price,
                    'timestamp': latest.name,
                    'volume': current_volume,
                    'signal_strength': min(100, (current_short - current_long) / current_long * 100),
                    'sma_short': current_short,
                    'sma_long': current_long
                }
            elif prev_short >= prev_long and current_short < current_long:
                return {
                    'action': 'SELL',
                    'price': current_price,
                    'timestamp': latest.name,
                    'volume': current_volume,
                    'signal_strength': min(100, (current_long - current_short) / current_short * 100),
                    'sma_short': current_short,
                    'sma_long': current_long
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error in SMA crossover strategy: {e}")
            return None
    
    def ema_strategy(self, df: pd.DataFrame) -> Optional[Dict]:
        """Exponential Moving Average Strategy"""
        try:
            if len(df) < 26:
                return None
            
            # Calculate EMAs
            df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=12)
            df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=26)
            
            latest = df.iloc[-1]
            current_price = latest['close']
            current_volume = latest['volume']
            ema_fast = latest['ema_fast']
            ema_slow = latest['ema_slow']
            
            # Check for trend signals
            if current_price > ema_fast > ema_slow:
                return {
                    'action': 'BUY',
                    'price': current_price,
                    'timestamp': latest.name,
                    'volume': current_volume,
                    'signal_strength': min(100, (current_price - ema_fast) / ema_fast * 100),
                    'ema_fast': ema_fast,
                    'ema_slow': ema_slow
                }
            elif current_price < ema_fast < ema_slow:
                return {
                    'action': 'SELL',
                    'price': current_price,
                    'timestamp': latest.name,
                    'volume': current_volume,
                    'signal_strength': min(100, (ema_fast - current_price) / current_price * 100),
                    'ema_fast': ema_fast,
                    'ema_slow': ema_slow
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error in EMA strategy: {e}")
            return None
    
    def momentum_strategy(self, df: pd.DataFrame) -> Optional[Dict]:
        """Momentum Strategy using ROC and RSI"""
        try:
            if len(df) < 20:
                return None
            
            # Calculate indicators
            df['roc'] = ta.momentum.roc(df['close'], window=10)
            df['rsi'] = ta.momentum.rsi(df['close'], window=14)
            
            latest = df.iloc[-1]
            current_price = latest['close']
            current_volume = latest['volume']
            current_roc = latest['roc']
            current_rsi = latest['rsi']
            
            # Strong momentum buy signal
            if current_roc > 2 and current_rsi < 70:
                return {
                    'action': 'BUY',
                    'price': current_price,
                    'timestamp': latest.name,
                    'volume': current_volume,
                    'signal_strength': min(100, current_roc * 10),
                    'roc': current_roc,
                    'rsi': current_rsi
                }
            # Strong momentum sell signal
            elif current_roc < -2 and current_rsi > 30:
                return {
                    'action': 'SELL',
                    'price': current_price,
                    'timestamp': latest.name,
                    'volume': current_volume,
                    'signal_strength': min(100, abs(current_roc) * 10),
                    'roc': current_roc,
                    'rsi': current_rsi
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error in momentum strategy: {e}")
            return None
    
    def volume_breakout_strategy(self, df: pd.DataFrame) -> Optional[Dict]:
        """Volume Breakout Strategy"""
        try:
            if len(df) < 20:
                return None
            
            # Calculate volume and price indicators
            df['volume_sma'] = df['volume'].rolling(window=20).mean()
            df['price_sma'] = ta.trend.sma_indicator(df['close'], window=20)
            
            latest = df.iloc[-1]
            current_price = latest['close']
            current_volume = latest['volume']
            avg_volume = latest['volume_sma']
            price_sma = latest['price_sma']
            
            # High volume breakout above resistance
            if current_volume > 1.5 * avg_volume and current_price > price_sma * 1.02:
                return {
                    'action': 'BUY',
                    'price': current_price,
                    'timestamp': latest.name,
                    'volume': current_volume,
                    'signal_strength': min(100, (current_volume / avg_volume - 1) * 50),
                    'volume_ratio': current_volume / avg_volume,
                    'price_vs_sma': (current_price - price_sma) / price_sma * 100
                }
            # High volume breakdown below support
            elif current_volume > 1.5 * avg_volume and current_price < price_sma * 0.98:
                return {
                    'action': 'SELL',
                    'price': current_price,
                    'timestamp': latest.name,
                    'volume': current_volume,
                    'signal_strength': min(100, (current_volume / avg_volume - 1) * 50),
                    'volume_ratio': current_volume / avg_volume,
                    'price_vs_sma': (current_price - price_sma) / price_sma * 100
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error in volume breakout strategy: {e}")
            return None
    
    def stochastic_strategy(self, df: pd.DataFrame) -> Optional[Dict]:
        """Stochastic Oscillator Strategy"""
        try:
            if len(df) < 14:
                return None
            
            # Calculate Stochastic oscillator
            df['stoch_k'] = ta.momentum.stoch(df['high'], df['low'], df['close'], window=14, smooth_window=3)
            df['stoch_d'] = ta.momentum.stoch_signal(df['high'], df['low'], df['close'], window=14, smooth_window=3)
            
            latest = df.iloc[-1]
            previous = df.iloc[-2]
            current_price = latest['close']
            current_volume = latest['volume']
            current_k = latest['stoch_k']
            current_d = latest['stoch_d']
            prev_k = previous['stoch_k']
            prev_d = previous['stoch_d']
            
            # Buy signal: K crosses above D in oversold territory
            if current_k > current_d and prev_k <= prev_d and current_k < 20:
                return {
                    'action': 'BUY',
                    'price': current_price,
                    'timestamp': latest.name,
                    'volume': current_volume,
                    'signal_strength': min(100, (20 - current_k) * 5),
                    'stoch_k': current_k,
                    'stoch_d': current_d
                }
            # Sell signal: K crosses below D in overbought territory
            elif current_k < current_d and prev_k >= prev_d and current_k > 80:
                return {
                    'action': 'SELL',
                    'price': current_price,
                    'timestamp': latest.name,
                    'volume': current_volume,
                    'signal_strength': min(100, (current_k - 80) * 5),
                    'stoch_k': current_k,
                    'stoch_d': current_d
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error in stochastic strategy: {e}")
            return None
    
    def generate_signal(self, df: pd.DataFrame, symbol: str, exchange: str) -> Optional[Dict]:
        """Generate trading signal based on configured strategy"""
        try:
            # Calculate indicators
            data_with_indicators = self.calculate_indicators(df)
            
            # Generate signal based on strategy
            signal = None
            
            if self.strategy_name == 'rsi_strategy':
                signal = self.rsi_strategy(data_with_indicators)
            elif self.strategy_name == 'macd_strategy':
                signal = self.macd_strategy(data_with_indicators)
            elif self.strategy_name == 'bollinger_strategy':
                signal = self.bollinger_strategy(data_with_indicators)
            elif self.strategy_name == 'multi_indicator_strategy':
                signal = self.multi_indicator_strategy(data_with_indicators)
            elif self.strategy_name == 'sma_crossover_strategy':
                signal = self.sma_crossover_strategy(data_with_indicators)
            elif self.strategy_name == 'ema_strategy':
                signal = self.ema_strategy(data_with_indicators)
            elif self.strategy_name == 'momentum_strategy':
                signal = self.momentum_strategy(data_with_indicators)
            elif self.strategy_name == 'volume_breakout_strategy':
                signal = self.volume_breakout_strategy(data_with_indicators)
            elif self.strategy_name == 'stochastic_strategy':
                signal = self.stochastic_strategy(data_with_indicators)
            else:
                # Default to RSI strategy
                signal = self.rsi_strategy(data_with_indicators)
            
            # Add symbol and exchange to signal
            if signal:
                signal['symbol'] = symbol
                signal['exchange'] = exchange
                signal['strategy'] = self.strategy_name
                
                # Calculate position size based on risk management
                signal['quantity'] = self.calculate_position_size(
                    signal['price'], 
                    data_with_indicators.iloc[-1].get('atr', 0)
                )
            
            return signal
            
        except Exception as e:
            logger.error(f"Error generating signal: {e}")
            return None
    
    def calculate_position_size(self, price: float, atr: float, account_balance: float = None) -> float:
        """Calculate dynamic position size based on advanced risk management"""
        try:
            # Get current account balance
            if account_balance is None:
                account_balance = self.config.get('backtest', {}).get('initial_capital', 10000)
            
            # Dynamic risk per trade based on recent performance
            base_risk = self.config.get('risk_per_trade', 0.01)  # 1% base risk
            risk_per_trade = self.adjust_risk_based_on_performance(base_risk)
            
            # Calculate risk amount
            risk_amount = account_balance * risk_per_trade
            
            # Dynamic stop loss based on volatility
            stop_loss_distance = self.calculate_dynamic_stop_distance(price, atr)
            
            # Kelly Criterion adjustment (simplified)
            win_rate = self.get_recent_win_rate()
            avg_win = self.get_average_win()
            avg_loss = self.get_average_loss()
            
            if avg_loss > 0 and win_rate > 0:
                kelly_fraction = (win_rate * avg_win - (1 - win_rate) * avg_loss) / avg_win
                kelly_fraction = max(0, min(kelly_fraction, 0.25))  # Cap at 25%
                risk_per_trade = min(risk_per_trade, kelly_fraction)
            
            # Calculate position size
            position_size = (account_balance * risk_per_trade) / stop_loss_distance
            
            # Apply maximum position size limit (10% of account)
            max_position_value = account_balance * 0.1
            max_quantity = max_position_value / price
            
            # Convert to number of shares/units
            quantity = position_size / price
            quantity = min(quantity, max_quantity)
            
            return max(0.001, quantity)  # Minimum quantity
            
        except Exception as e:
            logger.error(f"Error calculating dynamic position size: {e}")
            return 0.1  # Default quantity
    
    def adjust_risk_based_on_performance(self, base_risk: float) -> float:
        """Adjust risk based on recent trading performance"""
        try:
            # Get recent performance metrics
            recent_trades = getattr(self, 'recent_trades', [])
            if len(recent_trades) < 5:
                return base_risk
            
            # Calculate recent Sharpe ratio
            recent_returns = [trade.get('pnl_pct', 0) for trade in recent_trades[-10:]]
            if not recent_returns:
                return base_risk
            
            avg_return = np.mean(recent_returns)
            std_return = np.std(recent_returns)
            
            if std_return > 0:
                sharpe_ratio = avg_return / std_return
                
                # Adjust risk based on performance
                if sharpe_ratio > 1.0:  # Good performance
                    return min(base_risk * 1.5, 0.03)  # Increase risk up to 3%
                elif sharpe_ratio < -0.5:  # Poor performance
                    return max(base_risk * 0.5, 0.005)  # Reduce risk to 0.5%
            
            return base_risk
            
        except Exception as e:
            logger.error(f"Error adjusting risk: {e}")
            return base_risk
    
    def calculate_dynamic_stop_distance(self, price: float, atr: float) -> float:
        """Calculate dynamic stop loss distance based on volatility"""
        try:
            if atr <= 0:
                return price * 0.02  # 2% fallback
            
            # Base stop distance on ATR
            atr_multiplier = 2.0
            
            # Adjust multiplier based on volatility regime
            volatility_ratio = atr / price
            
            if volatility_ratio > 0.05:  # High volatility
                atr_multiplier = 3.0  # Wider stops
            elif volatility_ratio < 0.01:  # Low volatility
                atr_multiplier = 1.5  # Tighter stops
            
            stop_distance = atr_multiplier * atr
            
            # Ensure reasonable bounds (0.5% to 5% of price)
            min_stop = price * 0.005
            max_stop = price * 0.05
            
            return max(min_stop, min(stop_distance, max_stop))
            
        except Exception as e:
            logger.error(f"Error calculating stop distance: {e}")
            return price * 0.02
    
    def get_recent_win_rate(self) -> float:
        """Get recent win rate for Kelly Criterion"""
        try:
            recent_trades = getattr(self, 'recent_trades', [])
            if len(recent_trades) < 5:
                return 0.5  # Default 50%
            
            winning_trades = [t for t in recent_trades[-20:] if t.get('pnl', 0) > 0]
            return len(winning_trades) / min(len(recent_trades), 20)
            
        except Exception as e:
            logger.error(f"Error calculating win rate: {e}")
            return 0.5
    
    def get_average_win(self) -> float:
        """Get average winning trade percentage"""
        try:
            recent_trades = getattr(self, 'recent_trades', [])
            winning_trades = [t.get('pnl_pct', 0) for t in recent_trades[-20:] if t.get('pnl_pct', 0) > 0]
            
            return np.mean(winning_trades) if winning_trades else 0.02
            
        except Exception as e:
            logger.error(f"Error calculating average win: {e}")
            return 0.02
    
    def get_average_loss(self) -> float:
        """Get average losing trade percentage"""
        try:
            recent_trades = getattr(self, 'recent_trades', [])
            losing_trades = [abs(t.get('pnl_pct', 0)) for t in recent_trades[-20:] if t.get('pnl_pct', 0) < 0]
            
            return np.mean(losing_trades) if losing_trades else 0.015
            
        except Exception as e:
            logger.error(f"Error calculating average loss: {e}")
            return 0.015
    
    def get_strategy_description(self) -> str:
        """Get description of current strategy"""
        descriptions = {
            'rsi_strategy': f"RSI Strategy (Period: {self.rsi_period}, Oversold: {self.rsi_oversold}, Overbought: {self.rsi_overbought})",
            'macd_strategy': "MACD Strategy (12,26,9) - Buy on MACD crossover above signal line",
            'bollinger_strategy': "Bollinger Bands Strategy - Buy on lower band bounce, sell on upper band touch",
            'multi_indicator_strategy': "Multi-Indicator Strategy - Requires 2+ indicators to agree (RSI + MACD + Bollinger)",
            'sma_crossover_strategy': "SMA Crossover Strategy (10/30) - Golden/Death cross signals",
            'ema_strategy': "EMA Strategy (12/26) - Exponential moving average trend following",
            'momentum_strategy': "Momentum Strategy - ROC and RSI based momentum trading",
            'volume_breakout_strategy': "Volume Breakout Strategy - High volume breakout/breakdown signals",
            'stochastic_strategy': "Stochastic Strategy - Oscillator based reversal signals"
        }
        
        return descriptions.get(self.strategy_name, "Unknown Strategy")
    
    def validate_strategy_config(self) -> bool:
        """Validate strategy configuration"""
        try:
            # Check required parameters
            if self.strategy_name == 'rsi_strategy':
                return (self.rsi_period > 0 and 
                       0 < self.rsi_oversold < self.rsi_overbought < 100)
            
            elif self.strategy_name in ['macd_strategy', 'bollinger_strategy', 'multi_indicator_strategy']:
                return True  # These strategies use default parameters
            
            return False
            
        except Exception as e:
            logger.error(f"Error validating strategy config: {e}")
            return False
