# 🚀 AlgoTradeHub - Comprehensive Trading Platform

A full-stack algorithmic trading platform with advanced backtesting, real-time trading, and modern web interface.

## 📋 Table of Contents

- [🎯 Features](#-features)
- [🛠️ Quick Start](#️-quick-start)
- [📦 Installation](#-installation)
- [🚀 Usage](#-usage)
- [📊 Components](#-components)
- [🔧 Configuration](#-configuration)
- [📱 Frontend](#-frontend)
- [🧪 Testing](#-testing)
- [📚 Documentation](#-documentation)

## 🎯 Features

### **Backend (Python)**
- ✅ **Multi-Exchange Support**: Binance, Kraken, Delta, and more via CCXT
- ✅ **Advanced Backtesting**: Multi-timeframe, multi-strategy, multi-asset analysis
- ✅ **Real-time Trading**: Live trading with risk management
- ✅ **Strategy Library**: 9+ built-in trading strategies
- ✅ **Data Acquisition**: Historical and real-time market data
- ✅ **Risk Management**: Portfolio heat, drawdown limits, position sizing
- ✅ **Web Dashboard**: Flask-based web interface
- ✅ **Batch Processing**: Parallel strategy testing

### **Frontend (Next.js)**
- ✅ **Modern UI**: Built with Next.js 14, TypeScript, and shadcn/ui
- ✅ **Responsive Design**: Works on desktop, tablet, and mobile
- ✅ **Real-time Charts**: Interactive portfolio and performance charts
- ✅ **Feature Browser**: Central hub for all trading tools
- ✅ **Comprehensive Backtesting**: Advanced multi-dimensional analysis interface
- ✅ **Dark/Light Mode**: User preference support
- ✅ **Live Updates**: Real-time data streaming

## 🛠️ Quick Start

### **Option 1: One-Click Setup (Recommended)**
```bash
python quick_start.py
```

### **Option 2: Step-by-Step Setup**

1. **Check System Requirements**:
   ```bash
   python test_all_systems.py
   ```

2. **Install Node.js** (for frontend):
   - Visit: https://nodejs.org/
   - Download LTS version
   - Install and restart terminal

3. **Setup Frontend**:
   ```bash
   python frontend_complete_setup.py
   ```

4. **Launch Applications**:
   ```bash
   # Backend
   python main.py
   
   # Web Dashboard
   python app.py
   
   # Frontend
   cd frontend && npm run dev
   ```

## 📦 Installation

### **Prerequisites**
- **Python 3.8+** (3.10+ recommended)
- **Node.js 18+** (for frontend)
- **Git** (for cloning)

### **Python Dependencies**
```bash
pip install -r requirements.txt
```

Key packages:
- `ccxt` - Cryptocurrency exchange integration
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `ta` - Technical analysis
- `flask` - Web framework
- `rich` - Terminal formatting
- `matplotlib` - Plotting
- `plotly` - Interactive charts

### **Frontend Dependencies**
```bash
cd frontend
npm install
```

Key packages:
- `next` - React framework
- `react` - UI library
- `tailwindcss` - CSS framework
- `shadcn/ui` - Component library
- `recharts` - Chart library
- `lucide-react` - Icons

## 🚀 Usage

### **Backend Applications**

#### **1. Main Trading System**
```bash
python main.py
```
- Interactive menu system
- Strategy selection
- Backtesting and live trading
- Real-time market scanning

#### **2. Web Dashboard**
```bash
python app.py
```
- Web interface at http://localhost:5000
- Portfolio management
- Real-time monitoring
- Trade history

#### **3. Batch Runner**
```bash
python crypto/scripts/batch_runner.py --auto
```
- Comprehensive strategy testing
- Multi-timeframe analysis
- Performance comparison

### **Frontend Application**

#### **Development Server**
```bash
cd frontend
npm run dev
```
- Available at http://localhost:3000
- Hot reload for development
- Modern React interface

#### **Production Build**
```bash
cd frontend
npm run build
npm run start
```

### **Key Pages**
- **Dashboard**: http://localhost:3000
- **Feature Browser**: http://localhost:3000/features
- **Comprehensive Backtesting**: http://localhost:3000/backtest/comprehensive

## 📊 Components

### **Core Modules**

#### **`crypto/` - Cryptocurrency Module**
- `data_acquisition.py` - Market data fetching
- `crypto_symbol_manager.py` - Symbol management
- `backtest_config.py` - Backtesting configuration
- `crypto_assets_manager.py` - Asset management

#### **`crypto/scripts/` - Trading Scripts**
- `batch_runner.py` - Advanced batch processing
- `interactive_crypto_demo.py` - Interactive demo
- `delta_backtest_strategies.py` - Delta Exchange integration

#### **`crypto/strategies/` - Trading Strategies**
- `rsi_macd_vwap_strategy.py` - RSI + MACD + VWAP
- `bb_rsi_strategy.py` - Bollinger Bands + RSI
- `macd_only_strategy.py` - MACD-only strategy
- `enhanced_multi_factor.py` - Multi-factor strategy
- And more...

#### **`utils/` - Utility Modules**
- `config_manager.py` - Configuration management
- `data_fetcher.py` - Data fetching utilities
- `risk_manager.py` - Risk management
- `trade_tracker.py` - Trade tracking

### **Main Applications**
- `main.py` - Main trading application
- `app.py` - Web dashboard
- `strategy.py` - Strategy engine
- `backtest.py` - Backtesting engine

## 🔧 Configuration

### **Main Configuration (`config.yaml`)**
```yaml
exchanges:
  binance:
    active: true
    sandbox: true
    symbols: ["BTC/USDT", "ETH/USDT"]
  
strategy:
  name: "rsi_strategy"
  parameters:
    rsi_period: 14
    overbought: 70
    oversold: 30

backtest:
  start_date: "2023-01-01"
  end_date: "2024-01-01"
  initial_capital: 10000
  commission: 0.001
```

### **Credentials (`config/credentials.yaml`)**
```yaml
exchanges:
  binance:
    api_key: "your_api_key"
    secret: "your_secret"
    sandbox: true
```

## 📱 Frontend

### **Technology Stack**
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui (Radix UI primitives)
- **Charts**: Recharts
- **Icons**: Lucide React

### **Key Features**
- **Responsive Design**: Mobile-first approach
- **Real-time Updates**: Live data streaming
- **Interactive Charts**: Portfolio performance, P&L tracking
- **Feature Browser**: Central hub for all tools
- **Comprehensive Backtesting**: Advanced analysis interface

### **Development**
```bash
cd frontend
npm run dev    # Development server
npm run build  # Production build
npm run lint   # Code linting
```

## 🧪 Testing

### **Comprehensive Test Suite**
```bash
python test_all_systems.py
```

Tests:
- ✅ Python environment
- ✅ Core imports (pandas, ccxt, etc.)
- ✅ Project structure
- ✅ Crypto module functionality
- ✅ Script imports
- ✅ Frontend setup
- ✅ Data acquisition

### **Frontend Testing**
```bash
python test_frontend_setup.py
```

### **Individual Component Tests**
```bash
# Test data acquisition
python test_data_acquisition.py

# Test batch runner
python test_batch_runner.py

# Test crypto module
python -c "import crypto; print('Success!')"
```

## 📚 Documentation

### **Available Scripts**

#### **Setup & Testing**
- `quick_start.py` - One-click setup and launch
- `test_all_systems.py` - Comprehensive system test
- `frontend_complete_setup.py` - Frontend setup
- `fix_frontend.py` - Frontend troubleshooting
- `check_nodejs.py` - Node.js installation check

#### **Trading & Analysis**
- `main.py` - Main trading application
- `app.py` - Web dashboard
- `crypto/scripts/batch_runner.py` - Batch processing
- `crypto/scripts/interactive_crypto_demo.py` - Interactive demo

### **Configuration Files**
- `config.yaml` - Main configuration
- `config/credentials.yaml` - API credentials
- `requirements.txt` - Python dependencies
- `frontend/package.json` - Frontend dependencies

### **Data Files**
- `crypto_assets.csv` - Cryptocurrency symbols
- `crypto/output/` - Backtest results
- `data/` - Historical data cache

## 🚀 Getting Started Checklist

1. **✅ Install Python 3.8+**
2. **✅ Install Node.js 18+** from https://nodejs.org/
3. **✅ Clone repository**
4. **✅ Run**: `python quick_start.py`
5. **✅ Follow the interactive setup**
6. **✅ Launch your preferred interface**

## 🆘 Troubleshooting

### **Common Issues**

#### **"Node.js not found"**
- Install Node.js from https://nodejs.org/
- Restart terminal after installation
- Run `node --version` to verify

#### **"Module not found" errors**
- Run `pip install -r requirements.txt`
- Check Python version: `python --version`

#### **Frontend build fails**
- Run `python fix_frontend.py`
- Try `npm install --legacy-peer-deps`

#### **Data fetching fails**
- Check internet connection
- Verify exchange APIs are accessible
- Try different exchanges

### **Getting Help**
1. Run `python test_all_systems.py` for diagnostics
2. Check the error messages carefully
3. Ensure all prerequisites are installed
4. Try the automated fix scripts

## 📄 License

This project is for educational and research purposes.

---

## 🎯 Quick Commands Reference

```bash
# Setup
python quick_start.py                    # One-click setup
python test_all_systems.py              # Test everything
python frontend_complete_setup.py       # Setup frontend

# Backend
python main.py                          # Main application
python app.py                           # Web dashboard
python crypto/scripts/batch_runner.py --auto  # Batch testing

# Frontend
cd frontend && npm run dev              # Development server
cd frontend && npm run build            # Production build

# Testing
python test_all_systems.py             # Full system test
python check_nodejs.py                 # Check Node.js
python fix_frontend.py                 # Fix frontend issues
```

**Ready to start trading? Run `python quick_start.py` and let's go! 🚀**