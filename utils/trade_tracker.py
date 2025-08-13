#!/usr/bin/env python3
"""
Trade Tracker Module
Manages trading positions and performance tracking
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta
import json
import os
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradeStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    PARTIAL = "partial"
    CANCELLED = "cancelled"

@dataclass
class Trade:
    """Trade data structure"""
    id: str
    exchange: str
    symbol: str
    side: str  # 'buy' or 'sell'
    entry_price: float
    quantity: float
    entry_time: datetime
    exit_price: Optional[float] = None
    exit_time: Optional[datetime] = None
    status: str = TradeStatus.OPEN.value
    pnl: float = 0.0
    pnl_percentage: float = 0.0
    commission: float = 0.0
    strategy: str = ""
    signal_data: Dict = None
    
    def to_dict(self) -> Dict:
        """Convert trade to dictionary"""
        data = asdict(self)
        # Convert datetime objects to ISO format
        if self.entry_time:
            data['entry_time'] = self.entry_time.isoformat()
        if self.exit_time:
            data['exit_time'] = self.exit_time.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Trade':
        """Create trade from dictionary"""
        # Convert ISO format back to datetime
        if 'entry_time' in data and isinstance(data['entry_time'], str):
            data['entry_time'] = datetime.fromisoformat(data['entry_time'])
        if 'exit_time' in data and isinstance(data['exit_time'], str):
            data['exit_time'] = datetime.fromisoformat(data['exit_time'])
        return cls(**data)

class TradeTracker:
    def __init__(self, config: Dict):
        """Initialize trade tracker"""
        self.config = config
        self.trades: List[Trade] = []
        self.open_positions: Dict[str, Trade] = {}
        self.closed_trades: List[Trade] = []
        self.data_file = "data/trades.json"
        
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Load existing trades
        self.load_trades()
        
        logger.info("Trade tracker initialized")
    
    def load_trades(self):
        """Load trades from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    
                # Load trades
                for trade_data in data.get('trades', []):
                    trade = Trade.from_dict(trade_data)
                    self.trades.append(trade)
                    
                    if trade.status == TradeStatus.OPEN.value:
                        self.open_positions[self.get_position_key(trade)] = trade
                    else:
                        self.closed_trades.append(trade)
                        
                logger.info(f"Loaded {len(self.trades)} trades from file")
                
        except Exception as e:
            logger.error(f"Error loading trades: {e}")
    
    def save_trades(self):
        """Save trades to file"""
        try:
            data = {
                'trades': [trade.to_dict() for trade in self.trades],
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Saved {len(self.trades)} trades to file")
            
        except Exception as e:
            logger.error(f"Error saving trades: {e}")
    
    def get_position_key(self, trade: Trade) -> str:
        """Get position key for tracking"""
        return f"{trade.exchange}_{trade.symbol}_{trade.side}"
    
    def open_position(self, exchange: str, symbol: str, side: str, 
                     entry_price: float, quantity: float, 
                     strategy: str = "", signal_data: Dict = None) -> Trade:
        """Open a new position"""
        try:
            # Generate unique trade ID
            trade_id = f"{exchange}_{symbol}_{side}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create new trade
            trade = Trade(
                id=trade_id,
                exchange=exchange,
                symbol=symbol,
                side=side,
                entry_price=entry_price,
                quantity=quantity,
                entry_time=datetime.now(),
                strategy=strategy,
                signal_data=signal_data or {}
            )
            
            # Add to tracking
            position_key = self.get_position_key(trade)
            self.open_positions[position_key] = trade
            self.trades.append(trade)
            
            # Save to file
            self.save_trades()
            
            logger.info(f"Opened position: {position_key} at ${entry_price}")
            return trade
            
        except Exception as e:
            logger.error(f"Error opening position: {e}")
            raise
    
    def close_position(self, exchange: str, symbol: str, side: str, 
                      exit_price: float, quantity: float = None) -> Optional[Trade]:
        """Close a position"""
        try:
            position_key = self.get_position_key(
                Trade(id="", exchange=exchange, symbol=symbol, side=side,
                     entry_price=0, quantity=0, entry_time=datetime.now())
            )
            
            if position_key not in self.open_positions:
                logger.warning(f"No open position found for {position_key}")
                return None
            
            trade = self.open_positions[position_key]
            
            # Update trade details
            trade.exit_price = exit_price
            trade.exit_time = datetime.now()
            trade.status = TradeStatus.CLOSED.value
            
            # Calculate PnL
            if trade.side == 'buy':
                trade.pnl = (exit_price - trade.entry_price) * trade.quantity
            else:  # sell
                trade.pnl = (trade.entry_price - exit_price) * trade.quantity
            
            # Calculate percentage PnL
            if trade.entry_price > 0:
                trade.pnl_percentage = (trade.pnl / (trade.entry_price * trade.quantity)) * 100
            
            # Calculate commission
            commission_rate = self.config.get('trading', {}).get('commission', 0.001)
            trade.commission = (trade.entry_price * trade.quantity * commission_rate) + \
                             (exit_price * trade.quantity * commission_rate)
            
            # Adjust PnL for commission
            trade.pnl -= trade.commission
            
            # Move to closed trades
            self.closed_trades.append(trade)
            del self.open_positions[position_key]
            
            # Save to file
            self.save_trades()
            
            logger.info(f"Closed position: {position_key} at ${exit_price}, PnL: ${trade.pnl:.2f}")
            return trade
            
        except Exception as e:
            logger.error(f"Error closing position: {e}")
            raise
    
    def update_position_price(self, exchange: str, symbol: str, side: str, 
                            current_price: float):
        """Update current price for open position"""
        try:
            position_key = self.get_position_key(
                Trade(id="", exchange=exchange, symbol=symbol, side=side,
                     entry_price=0, quantity=0, entry_time=datetime.now())
            )
            
            if position_key in self.open_positions:
                trade = self.open_positions[position_key]
                
                # Calculate unrealized PnL
                if trade.side == 'buy':
                    unrealized_pnl = (current_price - trade.entry_price) * trade.quantity
                else:  # sell
                    unrealized_pnl = (trade.entry_price - current_price) * trade.quantity
                
                trade.pnl = unrealized_pnl
                
                # Calculate percentage PnL
                if trade.entry_price > 0:
                    trade.pnl_percentage = (unrealized_pnl / (trade.entry_price * trade.quantity)) * 100
                
        except Exception as e:
            logger.error(f"Error updating position price: {e}")
    
    def get_position_summary(self) -> Dict:
        """Get summary of all positions"""
        try:
            total_pnl = sum(trade.pnl for trade in self.trades)
            open_pnl = sum(trade.pnl for trade in self.open_positions.values())
            closed_pnl = sum(trade.pnl for trade in self.closed_trades)
            
            winning_trades = [t for t in self.closed_trades if t.pnl > 0]
            losing_trades = [t for t in self.closed_trades if t.pnl < 0]
            
            return {
                'total_trades': len(self.trades),
                'open_positions': len(self.open_positions),
                'closed_trades': len(self.closed_trades),
                'total_pnl': total_pnl,
                'open_pnl': open_pnl,
                'closed_pnl': closed_pnl,
                'winning_trades': len(winning_trades),
                'losing_trades': len(losing_trades),
                'win_rate': len(winning_trades) / len(self.closed_trades) if self.closed_trades else 0,
                'avg_win': np.mean([t.pnl for t in winning_trades]) if winning_trades else 0,
                'avg_loss': np.mean([t.pnl for t in losing_trades]) if losing_trades else 0,
                'largest_win': max([t.pnl for t in winning_trades]) if winning_trades else 0,
                'largest_loss': min([t.pnl for t in losing_trades]) if losing_trades else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting position summary: {e}")
            return {}
    
    def get_trades_by_exchange(self, exchange: str) -> List[Trade]:
        """Get all trades for a specific exchange"""
        return [trade for trade in self.trades if trade.exchange == exchange]
    
    def get_trades_by_symbol(self, symbol: str) -> List[Trade]:
        """Get all trades for a specific symbol"""
        return [trade for trade in self.trades if trade.symbol == symbol]
    
    def get_trades_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Trade]:
        """Get trades within a date range"""
        return [trade for trade in self.trades 
                if start_date <= trade.entry_time <= end_date]
    
    def get_performance_metrics(self) -> Dict:
        """Get detailed performance metrics"""
        try:
            if not self.closed_trades:
                return {}
            
            # Calculate metrics
            pnl_values = [trade.pnl for trade in self.closed_trades]
            pnl_percentages = [trade.pnl_percentage for trade in self.closed_trades]
            
            metrics = {
                'total_return': sum(pnl_values),
                'total_return_percentage': sum(pnl_percentages),
                'average_return': np.mean(pnl_values),
                'average_return_percentage': np.mean(pnl_percentages),
                'volatility': np.std(pnl_values),
                'sharpe_ratio': np.mean(pnl_values) / np.std(pnl_values) if np.std(pnl_values) > 0 else 0,
                'max_drawdown': self.calculate_max_drawdown(),
                'profit_factor': self.calculate_profit_factor(),
                'calmar_ratio': self.calculate_calmar_ratio(),
                'win_rate': len([t for t in self.closed_trades if t.pnl > 0]) / len(self.closed_trades),
                'trade_count': len(self.closed_trades),
                'avg_trade_duration': self.calculate_avg_trade_duration()
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating performance metrics: {e}")
            return {}
    
    def calculate_max_drawdown(self) -> float:
        """Calculate maximum drawdown"""
        try:
            if not self.closed_trades:
                return 0.0
            
            # Calculate cumulative returns
            cumulative_pnl = 0
            peak = 0
            max_drawdown = 0
            
            for trade in self.closed_trades:
                cumulative_pnl += trade.pnl
                if cumulative_pnl > peak:
                    peak = cumulative_pnl
                
                drawdown = (peak - cumulative_pnl) / peak if peak > 0 else 0
                max_drawdown = max(max_drawdown, drawdown)
            
            return max_drawdown
            
        except Exception as e:
            logger.error(f"Error calculating max drawdown: {e}")
            return 0.0
    
    def calculate_profit_factor(self) -> float:
        """Calculate profit factor"""
        try:
            gross_profit = sum(trade.pnl for trade in self.closed_trades if trade.pnl > 0)
            gross_loss = abs(sum(trade.pnl for trade in self.closed_trades if trade.pnl < 0))
            
            return gross_profit / gross_loss if gross_loss > 0 else 0
            
        except Exception as e:
            logger.error(f"Error calculating profit factor: {e}")
            return 0.0
    
    def calculate_calmar_ratio(self) -> float:
        """Calculate Calmar ratio"""
        try:
            total_return = sum(trade.pnl for trade in self.closed_trades)
            max_drawdown = self.calculate_max_drawdown()
            
            return total_return / max_drawdown if max_drawdown > 0 else 0
            
        except Exception as e:
            logger.error(f"Error calculating Calmar ratio: {e}")
            return 0.0
    
    def calculate_avg_trade_duration(self) -> float:
        """Calculate average trade duration in hours"""
        try:
            durations = []
            for trade in self.closed_trades:
                if trade.entry_time and trade.exit_time:
                    duration = (trade.exit_time - trade.entry_time).total_seconds() / 3600
                    durations.append(duration)
            
            return np.mean(durations) if durations else 0
            
        except Exception as e:
            logger.error(f"Error calculating average trade duration: {e}")
            return 0.0
    
    def export_trades_to_csv(self, filename: str = None) -> str:
        """Export trades to CSV file"""
        try:
            if not filename:
                filename = f"trades_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Convert trades to DataFrame
            trades_data = []
            for trade in self.trades:
                trades_data.append(trade.to_dict())
            
            df = pd.DataFrame(trades_data)
            
            # Save to CSV
            filepath = os.path.join("data", filename)
            df.to_csv(filepath, index=False)
            
            logger.info(f"Exported {len(self.trades)} trades to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting trades: {e}")
            raise
    
    def clear_all_trades(self):
        """Clear all trades (use with caution)"""
        try:
            self.trades.clear()
            self.open_positions.clear()
            self.closed_trades.clear()
            
            # Save empty state
            self.save_trades()
            
            logger.info("All trades cleared")
            
        except Exception as e:
            logger.error(f"Error clearing trades: {e}")
            raise
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary for dashboard"""
        try:
            summary = self.get_position_summary()
            metrics = self.get_performance_metrics()
            
            return {
                **summary,
                **metrics,
                'last_update': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting performance summary: {e}")
            return {}
    
    def get_trades_dataframe(self) -> pd.DataFrame:
        """Get trades as DataFrame"""
        try:
            if not self.trades:
                return pd.DataFrame()
            
            trades_data = []
            for trade in self.trades:
                trades_data.append(trade.to_dict())
            
            return pd.DataFrame(trades_data)
            
        except Exception as e:
            logger.error(f"Error getting trades dataframe: {e}")
            return pd.DataFrame()
    
    def get_open_positions(self) -> Dict:
        """Get open positions dictionary"""
        try:
            return self.open_positions
            
        except Exception as e:
            logger.error(f"Error getting open positions: {e}")
            return {}
    
    def get_closed_trades(self) -> List[Trade]:
        """Get closed trades list"""
        try:
            return self.closed_trades
            
        except Exception as e:
            logger.error(f"Error getting closed trades: {e}")
            return []