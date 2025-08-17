"""
Database initialization and utilities
"""

import os
from flask import Flask
from flask_migrate import Migrate
from models import db, Exchange, TradingPair, TradingStrategy, Trade, BacktestResult, Configuration

def init_database(app: Flask):
    """Initialize database with Flask app"""
    # Use existing config or set default SQLite database
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///algotrading.db')
    
    if not app.config.get('SQLALCHEMY_TRACK_MODIFICATIONS'):
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    return db, migrate

def populate_initial_data():
    """Populate initial data into database"""
    try:
        # Create exchanges
        exchanges_data = [
            {'name': 'binance', 'display_name': 'Binance', 'active': True, 'demo_mode': True},
            {'name': 'kraken', 'display_name': 'Kraken', 'active': True, 'demo_mode': True},
            {'name': 'coinbase', 'display_name': 'Coinbase Pro', 'active': True, 'demo_mode': True},
            {'name': 'bybit', 'display_name': 'Bybit', 'active': True, 'demo_mode': True},
            {'name': 'okx', 'display_name': 'OKX', 'active': True, 'demo_mode': True},
            {'name': 'kucoin', 'display_name': 'KuCoin', 'active': True, 'demo_mode': True},
            {'name': 'huobi', 'display_name': 'Huobi', 'active': True, 'demo_mode': True},
            {'name': 'bitget', 'display_name': 'Bitget', 'active': True, 'demo_mode': True},
            {'name': 'mexc', 'display_name': 'MEXC', 'active': True, 'demo_mode': True},
            {'name': 'bitfinex', 'display_name': 'Bitfinex', 'active': True, 'demo_mode': True},
        ]
        
        for exchange_data in exchanges_data:
            existing = Exchange.query.filter_by(name=exchange_data['name']).first()
            if not existing:
                exchange = Exchange(**exchange_data)
                db.session.add(exchange)
        
        # Create trading pairs
        trading_pairs_data = [
            {'symbol': 'BTC/USDT', 'base_asset': 'BTC', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'ETH/USDT', 'base_asset': 'ETH', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'BNB/USDT', 'base_asset': 'BNB', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'ADA/USDT', 'base_asset': 'ADA', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'SOL/USDT', 'base_asset': 'SOL', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'XRP/USDT', 'base_asset': 'XRP', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'DOT/USDT', 'base_asset': 'DOT', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'AVAX/USDT', 'base_asset': 'AVAX', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'LINK/USDT', 'base_asset': 'LINK', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'MATIC/USDT', 'base_asset': 'MATIC', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'UNI/USDT', 'base_asset': 'UNI', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'ATOM/USDT', 'base_asset': 'ATOM', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'ALGO/USDT', 'base_asset': 'ALGO', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'FTM/USDT', 'base_asset': 'FTM', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'NEAR/USDT', 'base_asset': 'NEAR', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'SAND/USDT', 'base_asset': 'SAND', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'MANA/USDT', 'base_asset': 'MANA', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'APE/USDT', 'base_asset': 'APE', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'CRV/USDT', 'base_asset': 'CRV', 'quote_asset': 'USDT', 'active': True},
            {'symbol': 'SUSHI/USDT', 'base_asset': 'SUSHI', 'quote_asset': 'USDT', 'active': True},
        ]
        
        for pair_data in trading_pairs_data:
            existing = TradingPair.query.filter_by(symbol=pair_data['symbol']).first()
            if not existing:
                pair = TradingPair(**pair_data)
                db.session.add(pair)
        
        # Create trading strategies
        strategies_data = [
            {
                'name': 'rsi_strategy',
                'display_name': 'RSI Strategy',
                'description': 'RSI-based strategy using overbought/oversold levels',
                'active': True,
                'parameters': {'rsi_period': 14, 'rsi_oversold': 30, 'rsi_overbought': 70},
                'risk_per_trade': 0.02,
                'max_positions': 5
            },
            {
                'name': 'macd_strategy',
                'display_name': 'MACD Strategy',
                'description': 'MACD-based strategy using signal line crossovers',
                'active': True,
                'parameters': {'fast_period': 12, 'slow_period': 26, 'signal_period': 9},
                'risk_per_trade': 0.02,
                'max_positions': 5
            },
            {
                'name': 'bollinger_strategy',
                'display_name': 'Bollinger Bands Strategy',
                'description': 'Bollinger Bands mean reversion strategy',
                'active': True,
                'parameters': {'period': 20, 'std_dev': 2},
                'risk_per_trade': 0.02,
                'max_positions': 5
            },
            {
                'name': 'multi_indicator_strategy',
                'display_name': 'Multi-Indicator Strategy',
                'description': 'Multi-indicator strategy combining RSI, MACD, and Bollinger Bands',
                'active': True,
                'parameters': {'require_signals': 2},
                'risk_per_trade': 0.02,
                'max_positions': 3
            },
            {
                'name': 'sma_crossover_strategy',
                'display_name': 'SMA Crossover Strategy',
                'description': 'Simple Moving Average crossover strategy (10/30 periods)',
                'active': True,
                'parameters': {'short_period': 10, 'long_period': 30},
                'risk_per_trade': 0.02,
                'max_positions': 5
            },
            {
                'name': 'ema_strategy',
                'display_name': 'EMA Strategy',
                'description': 'Exponential Moving Average trend following strategy',
                'active': True,
                'parameters': {'fast_period': 12, 'slow_period': 26},
                'risk_per_trade': 0.02,
                'max_positions': 5
            },
            {
                'name': 'momentum_strategy',
                'display_name': 'Momentum Strategy',
                'description': 'Momentum strategy using ROC and RSI indicators',
                'active': True,
                'parameters': {'roc_period': 10, 'rsi_period': 14, 'roc_threshold': 2},
                'risk_per_trade': 0.025,
                'max_positions': 4
            },
            {
                'name': 'volume_breakout_strategy',
                'display_name': 'Volume Breakout Strategy',
                'description': 'Volume breakout strategy for breakout trading',
                'active': True,
                'parameters': {'volume_period': 20, 'volume_multiplier': 1.5, 'price_threshold': 0.02},
                'risk_per_trade': 0.03,
                'max_positions': 3
            },
            {
                'name': 'stochastic_strategy',
                'display_name': 'Stochastic Strategy',
                'description': 'Stochastic oscillator strategy for reversal signals',
                'active': True,
                'parameters': {'k_period': 14, 'd_period': 3, 'oversold': 20, 'overbought': 80},
                'risk_per_trade': 0.02,
                'max_positions': 5
            }
        ]
        
        for strategy_data in strategies_data:
            existing = TradingStrategy.query.filter_by(name=strategy_data['name']).first()
            if not existing:
                strategy = TradingStrategy(**strategy_data)
                db.session.add(strategy)
        
        # Create initial configuration
        configs_data = [
            {
                'key': 'general_settings',
                'value': {
                    'scan_interval': 60,
                    'live_trading': False,
                    'demo_mode': True,
                    'max_concurrent_trades': 10
                },
                'description': 'General application settings'
            },
            {
                'key': 'active_exchanges',
                'value': ['binance', 'kraken'],
                'description': 'List of active exchanges'
            },
            {
                'key': 'active_trading_pairs',
                'value': ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'SOL/USDT'],
                'description': 'List of active trading pairs'
            },
            {
                'key': 'active_strategies',
                'value': ['rsi_strategy'],
                'description': 'List of active strategies'
            }
        ]
        
        for config_data in configs_data:
            existing = Configuration.query.filter_by(key=config_data['key']).first()
            if not existing:
                config = Configuration(**config_data)
                db.session.add(config)
        
        # Commit all changes
        db.session.commit()
        return True
        
    except Exception as e:
        db.session.rollback()
        raise e

def get_active_exchanges():
    """Get all active exchanges"""
    return Exchange.query.filter_by(active=True).all()

def get_active_trading_pairs():
    """Get all active trading pairs"""
    return TradingPair.query.filter_by(active=True).all()

def get_active_strategies():
    """Get all active strategies"""
    return TradingStrategy.query.filter_by(active=True).all()

def get_configuration(key):
    """Get configuration by key"""
    config = Configuration.query.filter_by(key=key).first()
    return config.value if config else None

def update_configuration(key, value, description=None):
    """Update configuration"""
    config = Configuration.query.filter_by(key=key).first()
    if config:
        config.value = value
        if description:
            config.description = description
    else:
        config = Configuration(key=key, value=value, description=description)
        db.session.add(config)
    
    db.session.commit()
    return config