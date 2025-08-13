# AlgoTrading Application

## Overview

This is a comprehensive algorithmic trading application built with Python and Flask. The system supports both backtesting and real-time trading across multiple cryptocurrency exchanges using the CCXT library. The application features a web interface for monitoring performance, configuring strategies, and analyzing trading results.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (July 16, 2025)

- ✓ Added 6 new trading strategies: SMA Crossover, EMA, Momentum, Volume Breakout, and Stochastic
- ✓ Created comprehensive configuration interface with exchange selection, trading pairs, and API credentials
- ✓ Added multi-select support for USDT trading pairs (20+ pairs available)
- ✓ Implemented demo mode for safe testing across all exchanges
- ✓ Added secure API credential management system
- ✓ Fixed missing TradeTracker methods for proper dashboard functionality
- ✓ Enhanced strategy configuration with risk management parameters
- ✓ **NEW: PostgreSQL Database Integration** - Added full database support with Flask-SQLAlchemy
- ✓ **NEW: Multi-select Strategy Configuration** - Strategies dropdown now supports multiple selection
- ✓ **NEW: Real-time Data Population** - All dropdowns now populated from database via API endpoints
- ✓ **NEW: Persistent Configuration Storage** - User configurations saved to database instead of files

## System Architecture

### Frontend Architecture
- **Web Framework**: Flask-based web application with server-side rendering
- **Templates**: Jinja2 templates for HTML rendering (dashboard, backtest, real-time trading pages)
- **Client-Side**: Bootstrap 5 for responsive UI, Plotly.js for interactive charts, Font Awesome for icons
- **Real-Time Updates**: JavaScript-based polling for live data updates and WebSocket-like functionality

### Backend Architecture
- **Core Framework**: Python Flask application serving as the main web server
- **Modular Design**: Separate modules for different functionalities (strategy, backtesting, data fetching, etc.)
- **Asynchronous Processing**: Uses asyncio for concurrent market data fetching and real-time scanning
- **Configuration Management**: YAML-based configuration system for exchanges, strategies, and application settings

### Data Storage Solutions
- **PostgreSQL Database**: Primary data storage for trades, strategies, exchanges, and configurations
- **Flask-SQLAlchemy ORM**: Database abstraction layer with model definitions and migrations
- **File-Based Storage**: Configuration files for credentials and application settings
- **In-Memory Caching**: Data caching for market information and performance metrics
- **Local Logging**: File-based logging system for application events and errors

## Key Components

### 1. Exchange Integration (`CCXT_ListofExchange.py`, `utils/data_fetcher.py`)
- **Purpose**: Manages connections to multiple cryptocurrency exchanges
- **Technology**: CCXT library for unified API access
- **Features**: Dynamic exchange listing, credential management, rate limiting
- **Supported Exchanges**: 100+ exchanges including Binance, Coinbase, Kraken, etc.

### 2. Trading Strategy Engine (`strategy.py`)
- **Purpose**: Implements various trading strategies with technical indicators
- **Features**: RSI-based strategies, moving averages, volume analysis
- **Extensibility**: Modular design allows for easy addition of new strategies
- **Technical Indicators**: Uses the `ta` library for technical analysis

### 3. Backtesting Engine (`backtest.py`)
- **Purpose**: Tests trading strategies against historical data
- **Features**: Performance metrics calculation, visualization of results
- **Metrics**: Sharpe ratio, drawdown analysis, win/loss ratios
- **Visualization**: Interactive charts using Plotly

### 4. Real-Time Scanner (`main.py`)
- **Purpose**: Monitors markets in real-time and generates trading signals
- **Features**: Multi-exchange scanning, signal generation, live trading capability
- **Architecture**: Event-driven with async processing for multiple exchanges
- **Risk Management**: Demo mode for safe testing before live trading

### 5. Configuration Management (`utils/config_manager.py`)
- **Purpose**: Centralizes all application configuration
- **Features**: YAML-based config, credential management, validation
- **Security**: Separate credentials file for sensitive information
- **Flexibility**: Easy toggling of exchanges and strategy parameters

### 6. Utility Modules (`utils/`)
- **Trade Tracker**: Manages trading positions and performance tracking
- **Metrics Calculator**: Computes comprehensive performance metrics
- **Visualization**: Creates charts and graphs for analysis
- **Data Fetcher**: Handles market data retrieval from exchanges

## Data Flow

1. **Configuration Loading**: Application loads settings from YAML files
2. **Exchange Initialization**: Connects to enabled exchanges using CCXT
3. **Market Data Fetching**: Retrieves real-time and historical price data
4. **Strategy Execution**: Applies trading logic to market data
5. **Signal Generation**: Creates buy/sell signals based on strategy conditions
6. **Trade Execution**: Places orders (live or demo mode)
7. **Performance Tracking**: Monitors and calculates trading metrics
8. **Visualization**: Displays results through web interface

## External Dependencies

### Core Libraries
- **CCXT**: Cryptocurrency exchange integration
- **Flask**: Web framework for the application
- **Pandas/NumPy**: Data manipulation and analysis
- **Plotly**: Interactive charting and visualization
- **PyYAML**: Configuration file parsing
- **TA-Lib**: Technical analysis indicators

### Frontend Dependencies
- **Bootstrap 5**: Responsive UI framework
- **Font Awesome**: Icon library
- **Plotly.js**: Client-side charting
- **JavaScript**: Real-time updates and interactivity

### Development Dependencies
- **Rich**: Enhanced console output for CLI tools
- **Logging**: Built-in Python logging for debugging
- **Asyncio**: Asynchronous programming support

## Deployment Strategy

### Local Development
- **Configuration**: Uses local YAML files for settings
- **Data Storage**: File-based storage for trades and logs
- **Security**: Sandbox mode enabled by default for all exchanges
- **Testing**: Demo mode for safe strategy testing

### Production Considerations
- **Environment Variables**: Sensitive data should be moved to environment variables
- **Database Migration**: Consider migrating from file-based to database storage
- **Containerization**: Application can be containerized with Docker
- **Monitoring**: Enhanced logging and monitoring for production use

### Security Features
- **API Key Management**: Secure storage of exchange credentials
- **Sandbox Mode**: Safe testing environment before live trading
- **Rate Limiting**: Built-in protection against API rate limits
- **Error Handling**: Comprehensive error handling and logging

The application is designed to be modular and extensible, allowing users to easily add new exchanges, strategies, and features while maintaining a clean separation of concerns between different components.