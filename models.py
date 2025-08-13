"""
Database Models for AlgoTrading Application
"""

from datetime import datetime
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
db = SQLAlchemy()

class TradeStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    PARTIAL = "partial"
    CANCELLED = "cancelled"

class Exchange(db.Model):
    __tablename__ = 'exchanges'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    demo_mode = Column(Boolean, default=True)
    api_key = Column(String(500))
    api_secret = Column(String(500))
    api_passphrase = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trades = relationship("Trade", back_populates="exchange_obj")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'active': self.active,
            'demo_mode': self.demo_mode,
            'has_credentials': bool(self.api_key and self.api_secret),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TradingPair(db.Model):
    __tablename__ = 'trading_pairs'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), unique=True, nullable=False)
    base_asset = Column(String(10), nullable=False)
    quote_asset = Column(String(10), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    trades = relationship("Trade", back_populates="trading_pair_obj")
    
    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'base_asset': self.base_asset,
            'quote_asset': self.quote_asset,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class TradingStrategy(db.Model):
    __tablename__ = 'trading_strategies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(200), nullable=False)
    description = Column(Text)
    active = Column(Boolean, default=True)
    parameters = Column(JSON)
    risk_per_trade = Column(Float, default=0.02)
    max_positions = Column(Integer, default=5)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trades = relationship("Trade", back_populates="strategy_obj")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'active': self.active,
            'parameters': self.parameters,
            'risk_per_trade': self.risk_per_trade,
            'max_positions': self.max_positions,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Trade(db.Model):
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True)
    trade_id = Column(String(100), unique=True, nullable=False)
    exchange_id = Column(Integer, ForeignKey('exchanges.id'), nullable=False)
    trading_pair_id = Column(Integer, ForeignKey('trading_pairs.id'), nullable=False)
    strategy_id = Column(Integer, ForeignKey('trading_strategies.id'), nullable=False)
    
    side = Column(String(10), nullable=False)  # 'BUY' or 'SELL'
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float)
    quantity = Column(Float, nullable=False)
    
    entry_time = Column(DateTime, nullable=False)
    exit_time = Column(DateTime)
    
    status = Column(String(20), default=TradeStatus.OPEN.value)
    pnl = Column(Float, default=0.0)
    pnl_percentage = Column(Float, default=0.0)
    commission = Column(Float, default=0.0)
    
    signal_data = Column(JSON)
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    exchange_obj = relationship("Exchange", back_populates="trades")
    trading_pair_obj = relationship("TradingPair", back_populates="trades")
    strategy_obj = relationship("TradingStrategy", back_populates="trades")
    
    def to_dict(self):
        return {
            'id': self.id,
            'trade_id': self.trade_id,
            'exchange': self.exchange_obj.name if self.exchange_obj else None,
            'trading_pair': self.trading_pair_obj.symbol if self.trading_pair_obj else None,
            'strategy': self.strategy_obj.name if self.strategy_obj else None,
            'side': self.side,
            'entry_price': self.entry_price,
            'exit_price': self.exit_price,
            'quantity': self.quantity,
            'entry_time': self.entry_time.isoformat() if self.entry_time else None,
            'exit_time': self.exit_time.isoformat() if self.exit_time else None,
            'status': self.status,
            'pnl': self.pnl,
            'pnl_percentage': self.pnl_percentage,
            'commission': self.commission,
            'signal_data': self.signal_data,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class BacktestResult(db.Model):
    __tablename__ = 'backtest_results'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    exchange_id = Column(Integer, ForeignKey('exchanges.id'), nullable=False)
    trading_pair_id = Column(Integer, ForeignKey('trading_pairs.id'), nullable=False)
    strategy_id = Column(Integer, ForeignKey('trading_strategies.id'), nullable=False)
    
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    initial_capital = Column(Float, nullable=False)
    final_capital = Column(Float, nullable=False)
    
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)
    
    total_pnl = Column(Float, default=0.0)
    total_pnl_percentage = Column(Float, default=0.0)
    max_drawdown = Column(Float, default=0.0)
    sharpe_ratio = Column(Float)
    
    results_data = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    exchange_obj = relationship("Exchange")
    trading_pair_obj = relationship("TradingPair")
    strategy_obj = relationship("TradingStrategy")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'exchange': self.exchange_obj.name if self.exchange_obj else None,
            'trading_pair': self.trading_pair_obj.symbol if self.trading_pair_obj else None,
            'strategy': self.strategy_obj.name if self.strategy_obj else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'initial_capital': self.initial_capital,
            'final_capital': self.final_capital,
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
            'win_rate': self.win_rate,
            'total_pnl': self.total_pnl,
            'total_pnl_percentage': self.total_pnl_percentage,
            'max_drawdown': self.max_drawdown,
            'sharpe_ratio': self.sharpe_ratio,
            'results_data': self.results_data,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Configuration(db.Model):
    __tablename__ = 'configurations'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(JSON)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }