#!/usr/bin/env python3
"""
AlgoTrading Web Application
Flask web interface for the algorithmic trading system
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import asyncio
import json
import os
import logging
from datetime import datetime, timedelta
import threading
import time
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import yaml
import requests
import subprocess
from threading import Thread

# Next.js frontend configuration
NEXTJS_URL = 'http://localhost:3000'
nextjs_process = None

def start_nextjs_server():
    """Start Next.js development server"""
    global nextjs_process
    try:
        import os
        import subprocess
        
        # Change to frontend directory and start Next.js
        frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
        nextjs_process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.info("Next.js server started")
        return True
    except Exception as e:
        logger.error(f"Failed to start Next.js server: {e}")
        return False

def proxy_to_nextjs(path=''):
    """Proxy requests to Next.js server"""
    try:
        url = f"{NEXTJS_URL}/{path}"
        
        # Forward the request to Next.js
        if request.method == 'GET':
            response = requests.get(url, params=request.args)
        elif request.method == 'POST':
            response = requests.post(url, json=request.get_json(), params=request.args)
        else:
            response = requests.request(request.method, url, 
                                      data=request.get_data(), 
                                      headers=dict(request.headers))
        
        # Return the response from Next.js
        return response.content, response.status_code, dict(response.headers)
        
    except Exception as e:
        logger.error(f"Error proxying to Next.js: {e}")
        return f"Error connecting to frontend: {e}", 500

# Import our modules
from utils.config_manager import ConfigManager
from utils.data_fetcher import DataFetcher
from utils.trade_tracker import TradeTracker
from utils.metrics_calculator import MetricsCalculator
from utils.visualization import Visualizer
from strategy import TradingStrategy
from backtest import BacktestEngine
# from main import RealTimeScanner  # Temporarily disabled

# Import database modules
from database import init_database, populate_initial_data, get_active_exchanges, get_active_trading_pairs, get_active_strategies, get_configuration, update_configuration
from models import db, Exchange, TradingPair, TradingStrategy as DbTradingStrategy, Trade, BacktestResult, Configuration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('webapp.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///algotrading.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Global variables
config_manager = None
trade_tracker = None
visualizer = None
metrics_calculator = None
scanner = None
scanner_thread = None
scanner_running = False

def initialize_app():
    """Initialize the application components"""
    global config_manager, trade_tracker, visualizer, metrics_calculator
    
    try:
        # Initialize database
        db_instance, migrate = init_database(app)
        
        # Create tables and populate initial data
        with app.app_context():
            db.create_all()
            populate_initial_data()
        
        # Initialize managers
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        trade_tracker = TradeTracker(config)
        visualizer = Visualizer()
        metrics_calculator = MetricsCalculator()
        
        logger.info("Application initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing application: {e}")
        raise

def run_scanner_async():
    """Run the scanner in a separate thread"""
    global scanner, scanner_running
    
    try:
        scanner_running = True
        # Placeholder for scanner functionality
        logger.info("Scanner started (placeholder)")
        time.sleep(1)  # Simulate scanner work
        
    except Exception as e:
        logger.error(f"Error in scanner thread: {e}")
    finally:
        scanner_running = False

# Routes for Next.js frontend integration
@app.route('/')
@app.route('/dashboard')
@app.route('/exchanges')
@app.route('/trading')
@app.route('/portfolio')
@app.route('/backtest')
@app.route('/features')
@app.route('/settings')
@app.route('/test')
def serve_nextjs_frontend():
    """Serve Next.js frontend through Flask"""
    return proxy_to_nextjs()

@app.route('/_next/<path:path>')
def serve_nextjs_assets(path):
    """Serve Next.js static assets"""
    return proxy_to_nextjs(f'_next/{path}')

@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_api_routes(path):
    """Proxy API routes to existing Flask endpoints or Next.js"""
    # Check if this is a Flask API route we want to handle
    flask_routes = [
        'backtest', 'run_backtest', 'scanner/start', 'scanner/stop', 
        'start_scanner', 'stop_scanner', 'get_performance', 'get_trades',
        'positions', 'get_positions', 'signals', 'config', 'get_config',
        'update_config', 'get_chart_data', 'get_metrics', 'export_data',
        'exchange/configure', 'exchange/test'
    ]
    
    # If it's a Flask route, handle it normally
    for route in flask_routes:
        if path.startswith(route):
            # Let Flask handle this route normally
            return None
    
    # Otherwise, proxy to Next.js
    return proxy_to_nextjs(f'api/{path}')

# Legacy route for old dashboard (keep for backward compatibility)
@app.route('/legacy')
def legacy_index():
    """Legacy dashboard page"""
    try:
        config = config_manager.load_config()
        
        # Get performance summary
        performance = trade_tracker.get_performance_summary()
        
        # Get active exchanges
        active_exchanges = config_manager.get_active_exchanges()
        
        # Get recent trades
        recent_trades = trade_tracker.get_closed_trades()[-10:]  # Last 10 trades
        
        # Get open positions
        open_positions = trade_tracker.get_open_positions()
        
        # Get config summary
        config_summary = config_manager.get_config_summary()
        
        return render_template('index.html',
                             performance=performance,
                             active_exchanges=active_exchanges,
                             recent_trades=recent_trades,
                             open_positions=open_positions,
                             config_summary=config_summary,
                             scanner_running=scanner_running)
        
    except Exception as e:
        logger.error(f"Error in legacy index route: {e}")
        flash(f"Error loading dashboard: {e}", 'error')
        return render_template('index.html', 
                             performance={}, 
                             active_exchanges={},
                             recent_trades=[],
                             open_positions={},
                             config_summary={},
                             scanner_running=False)

@app.route('/backtest')
def backtest_page():
    """Backtest page"""
    try:
        config = config_manager.load_config()
        
        # Get available exchanges and symbols
        exchanges = config.get('exchanges', {})
        available_exchanges = [(name, conf) for name, conf in exchanges.items() if conf.get('active', False)]
        
        return render_template('backtest.html',
                             exchanges=available_exchanges,
                             backtest_config=config.get('backtest', {}))
        
    except Exception as e:
        logger.error(f"Error in backtest route: {e}")
        flash(f"Error loading backtest page: {e}", 'error')
        return render_template('backtest.html', exchanges=[], backtest_config={})

@app.route('/realtime')
def realtime_page():
    """Real-time trading page"""
    try:
        config = config_manager.load_config()
        
        # Get active exchanges
        active_exchanges = config_manager.get_active_exchanges()
        
        # Get open positions
        open_positions = trade_tracker.get_open_positions()
        
        # Get recent signals/trades
        recent_trades = trade_tracker.get_closed_trades()[-20:]  # Last 20 trades
        
        return render_template('realtime.html',
                             active_exchanges=active_exchanges,
                             open_positions=open_positions,
                             recent_trades=recent_trades,
                             scanner_running=scanner_running,
                             live_trading=config.get('live_trading', False))
        
    except Exception as e:
        logger.error(f"Error in realtime route: {e}")
        flash(f"Error loading realtime page: {e}", 'error')
        return render_template('realtime.html',
                             active_exchanges={},
                             open_positions={},
                             recent_trades=[],
                             scanner_running=False,
                             live_trading=False)

@app.route('/configuration')
def config_page():
    """Configuration page"""
    try:
        config = config_manager.load_config()
        return render_template('configuration.html', config=config)
    except Exception as e:
        logger.error(f"Error in configuration route: {e}")
        flash(f"Error loading configuration page: {e}", 'error')
        return render_template('configuration.html', config={})

@app.route('/api/backtest', methods=['POST'])
def api_backtest():
    """Run backtest API endpoint for frontend"""
    try:
        data = request.get_json()
        
        symbol = data.get('symbol')
        strategy = data.get('strategy')
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        initial_capital = data.get('initialCapital', 10000)
        commission = data.get('commission', 0.001)
        
        if not all([symbol, strategy, start_date, end_date]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Simulate backtest execution and return mock results
        # In a real implementation, this would run the actual backtest
        import random
        import time
        
        # Simulate processing time
        time.sleep(1)
        
        # Generate mock results
        total_return = random.uniform(-20, 80)  # -20% to 80%
        sharpe_ratio = random.uniform(0.2, 3.2)  # 0.2 to 3.2
        max_drawdown = random.uniform(-30, 0)  # 0% to -30%
        win_rate = random.uniform(30, 80)  # 30% to 80%
        total_trades = random.randint(20, 320)  # 20 to 320
        final_portfolio = initial_capital * (1 + total_return / 100)
        
        results = {
            'totalReturn': total_return,
            'sharpeRatio': sharpe_ratio,
            'maxDrawdown': max_drawdown,
            'winRate': win_rate,
            'totalTrades': total_trades,
            'finalPortfolio': final_portfolio,
            'trades': []  # Could include detailed trade list
        }
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Error running backtest: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/run_backtest', methods=['POST'])
def run_backtest():
    """Run backtest API endpoint (legacy)"""
    try:
        data = request.get_json()
        
        exchange_name = data.get('exchange')
        symbol = data.get('symbol')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        timeframe = data.get('timeframe', '1h')
        
        if not all([exchange_name, symbol, start_date, end_date]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Update backtest config
        config = config_manager.load_config()
        config['backtest']['start_date'] = start_date
        config['backtest']['end_date'] = end_date
        config_manager.save_config(config)
        
        # Run backtest in a separate thread
        def run_backtest_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            backtest_engine = BacktestEngine()
            loop.run_until_complete(backtest_engine.run_backtest(exchange_name, symbol, timeframe))
        
        # Start backtest thread
        backtest_thread = threading.Thread(target=run_backtest_async)
        backtest_thread.daemon = True
        backtest_thread.start()
        
        return jsonify({'status': 'success', 'message': 'Backtest started'})
        
    except Exception as e:
        logger.error(f"Error running backtest: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/scanner/start', methods=['POST'])
def api_start_scanner():
    """Start real-time scanner (frontend API)"""
    global scanner_thread, scanner_running
    
    try:
        if scanner_running:
            return jsonify({'success': False, 'message': 'Scanner is already running'})
        
        # Start scanner in a separate thread
        scanner_thread = threading.Thread(target=run_scanner_async)
        scanner_thread.daemon = True
        scanner_thread.start()
        
        return jsonify({'success': True, 'message': 'Scanner started successfully'})
        
    except Exception as e:
        logger.error(f"Error starting scanner: {e}")
        return jsonify({'success': False, 'message': f'Error starting scanner: {str(e)}'})

@app.route('/api/scanner/stop', methods=['POST'])
def api_stop_scanner():
    """Stop real-time scanner (frontend API)"""
    global scanner, scanner_running
    
    try:
        if not scanner_running:
            return jsonify({'success': False, 'message': 'Scanner is not running'})
        
        # Stop scanner
        if scanner:
            scanner.running = False
        
        scanner_running = False
        
        return jsonify({'success': True, 'message': 'Scanner stopped successfully'})
        
    except Exception as e:
        logger.error(f"Error stopping scanner: {e}")
        return jsonify({'success': False, 'message': f'Error stopping scanner: {str(e)}'})

@app.route('/api/start_scanner', methods=['POST'])
def start_scanner():
    """Start real-time scanner (legacy)"""
    global scanner_thread, scanner_running
    
    try:
        if scanner_running:
            return jsonify({'error': 'Scanner is already running'}), 400
        
        # Start scanner in a separate thread
        scanner_thread = threading.Thread(target=run_scanner_async)
        scanner_thread.daemon = True
        scanner_thread.start()
        
        return jsonify({'status': 'success', 'message': 'Scanner started'})
        
    except Exception as e:
        logger.error(f"Error starting scanner: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop_scanner', methods=['POST'])
def stop_scanner():
    """Stop real-time scanner (legacy)"""
    global scanner, scanner_running
    
    try:
        if not scanner_running:
            return jsonify({'error': 'Scanner is not running'}), 400
        
        # Stop scanner
        if scanner:
            scanner.running = False
        
        scanner_running = False
        
        return jsonify({'status': 'success', 'message': 'Scanner stopped'})
        
    except Exception as e:
        logger.error(f"Error stopping scanner: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_performance', methods=['GET'])
def get_performance():
    """Get performance data"""
    try:
        performance = trade_tracker.get_performance_summary()
        return jsonify(performance)
        
    except Exception as e:
        logger.error(f"Error getting performance: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_trades', methods=['GET'])
def get_trades():
    """Get trades data"""
    try:
        trades_df = trade_tracker.get_trades_dataframe()
        
        if trades_df.empty:
            return jsonify({'trades': []})
        
        # Convert to JSON serializable format
        trades_data = trades_df.to_dict('records')
        
        # Convert timestamps to strings
        for trade in trades_data:
            if 'entry_time' in trade and trade['entry_time']:
                trade['entry_time'] = trade['entry_time'].isoformat()
            if 'exit_time' in trade and trade['exit_time']:
                trade['exit_time'] = trade['exit_time'].isoformat()
        
        return jsonify({'trades': trades_data})
        
    except Exception as e:
        logger.error(f"Error getting trades: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/positions', methods=['GET'])
def api_get_positions():
    """Get open positions (frontend API)"""
    try:
        positions = trade_tracker.get_open_positions()
        
        # Convert to list format for frontend
        positions_list = []
        for key, position in positions.items():
            positions_list.append({
                'symbol': position.symbol,
                'side': position.side.upper(),
                'entryPrice': position.entry_price,
                'currentPrice': getattr(position, 'current_price', position.entry_price),
                'quantity': position.quantity,
                'pnl': position.pnl,
                'pnlPercentage': position.pnl_percentage,
                'timestamp': position.entry_time.isoformat() if position.entry_time else datetime.now().isoformat()
            })
        
        return jsonify(positions_list)
        
    except Exception as e:
        logger.error(f"Error getting positions: {e}")
        return jsonify([])  # Return empty list on error

@app.route('/api/get_positions', methods=['GET'])
def get_positions():
    """Get open positions (legacy)"""
    try:
        positions = trade_tracker.get_open_positions()
        
        # Convert to JSON serializable format
        positions_data = {}
        for key, position in positions.items():
            positions_data[key] = {
                'id': position.id,
                'exchange': position.exchange,
                'symbol': position.symbol,
                'side': position.side,
                'entry_price': position.entry_price,
                'entry_time': position.entry_time.isoformat() if position.entry_time else None,
                'quantity': position.quantity,
                'current_price': getattr(position, 'current_price', position.entry_price),
                'pnl': position.pnl,
                'pnl_percentage': position.pnl_percentage,
                'status': position.status
            }
        
        return jsonify({'positions': positions_data})
        
    except Exception as e:
        logger.error(f"Error getting positions: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/signals', methods=['GET'])
def api_get_signals():
    """Get trading signals (frontend API)"""
    try:
        # Generate mock signals for demo
        import random
        
        symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'ADA/USDT', 'DOT/USDT']
        indicators = ['RSI: 28', 'MACD: Bullish', 'BB: Oversold', 'SMA: Cross', 'Volume: High']
        
        signals = []
        for i in range(random.randint(1, 3)):  # 1-3 signals
            signals.append({
                'symbol': random.choice(symbols),
                'type': random.choice(['BUY', 'SELL']),
                'price': random.uniform(20000, 50000) if 'BTC' in symbols[0] else random.uniform(1000, 3000),
                'indicator': random.choice(indicators),
                'strength': random.randint(70, 95),
                'timestamp': datetime.now().isoformat()
            })
        
        return jsonify(signals)
        
    except Exception as e:
        logger.error(f"Error getting signals: {e}")
        return jsonify([])

@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """Get or update configuration (frontend API)"""
    if request.method == 'GET':
        try:
            config = config_manager.load_config()
            return jsonify(config)
        except Exception as e:
            logger.error(f"Error getting configuration: {e}")
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # Save the configuration
            success = config_manager.save_config(data)
            
            if success:
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'error': 'Failed to save configuration'}), 500
                
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_config', methods=['GET'])
def get_config():
    """Get current configuration (legacy)"""
    try:
        config = config_manager.load_config()
        return jsonify(config)
    except Exception as e:
        logger.error(f"Error getting configuration: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/update_config', methods=['POST'])
def update_config():
    """Update configuration"""
    try:
        data = request.get_json()
        
        config_type = data.get('type')
        config_data = data.get('data')
        
        if config_type == 'exchange':
            exchange_name = data.get('exchange')
            success = config_manager.update_exchange_config(exchange_name, config_data)
        elif config_type == 'strategy':
            success = config_manager.update_strategy_config(config_data)
        elif config_type == 'exchanges':
            # Update multiple exchanges
            exchanges = data.get('exchanges', [])
            demo_mode = data.get('demo_mode', True)
            for exchange_name in exchanges:
                exchange_config = {
                    'active': True,
                    'demo_mode': demo_mode
                }
                config_manager.update_exchange_config(exchange_name, exchange_config)
            success = True
        elif config_type == 'trading_pairs':
            # Update trading pairs
            current_config = config_manager.load_config()
            current_config['trading_pairs'] = data.get('pairs', [])
            success = config_manager.save_config(current_config)
        elif config_type == 'credentials':
            # Update API credentials
            exchange_name = data.get('exchange')
            credentials = {
                'api_key': data.get('api_key'),
                'api_secret': data.get('api_secret'),
                'api_passphrase': data.get('api_passphrase', '')
            }
            
            # Save credentials securely
            current_credentials = config_manager.load_credentials()
            if exchange_name not in current_credentials:
                current_credentials[exchange_name] = {}
            current_credentials[exchange_name].update(credentials)
            success = config_manager.save_credentials(current_credentials)
        else:
            return jsonify({'error': 'Invalid config type'}), 400
        
        if success:
            return jsonify({'status': 'success', 'message': 'Configuration updated'})
        else:
            return jsonify({'error': 'Failed to update configuration'}), 500
        
    except Exception as e:
        logger.error(f"Error updating config: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_chart_data', methods=['GET'])
def get_chart_data():
    """Get chart data for visualization"""
    try:
        chart_type = request.args.get('type', 'portfolio')
        
        if chart_type == 'portfolio':
            # Get portfolio performance data
            trades_df = trade_tracker.get_trades_dataframe()
            
            if trades_df.empty:
                return jsonify({'error': 'No trade data available'}), 400
            
            # Create sample portfolio values (this would be calculated from actual trades)
            dates = pd.date_range(start='2023-01-01', end=datetime.now(), freq='D')
            portfolio_values = pd.Series(
                index=dates,
                data=np.random.walk(len(dates)) * 100 + 10000  # Sample data
            )
            
            # Create chart
            fig = visualizer.create_portfolio_chart(portfolio_values)
            chart_json = visualizer.get_chart_json(fig)
            
            return jsonify({'chart': chart_json})
        
        elif chart_type == 'drawdown':
            # Get drawdown data
            dates = pd.date_range(start='2023-01-01', end=datetime.now(), freq='D')
            portfolio_values = pd.Series(
                index=dates,
                data=np.random.walk(len(dates)) * 100 + 10000  # Sample data
            )
            
            fig = visualizer.create_drawdown_chart(portfolio_values)
            chart_json = visualizer.get_chart_json(fig)
            
            return jsonify({'chart': chart_json})
        
        else:
            return jsonify({'error': 'Invalid chart type'}), 400
        
    except Exception as e:
        logger.error(f"Error getting chart data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_metrics', methods=['GET'])
def get_metrics():
    """Get calculated metrics"""
    try:
        # Get sample portfolio data
        dates = pd.date_range(start='2023-01-01', end=datetime.now(), freq='D')
        portfolio_values = pd.Series(
            index=dates,
            data=np.random.walk(len(dates)) * 100 + 10000  # Sample data
        )
        
        # Get trades for metrics calculation
        trades_df = trade_tracker.get_trades_dataframe()
        trades_list = trades_df.to_dict('records') if not trades_df.empty else []
        
        # Calculate metrics
        metrics = metrics_calculator.calculate_all_metrics(
            portfolio_values=portfolio_values,
            trades=trades_list
        )
        
        # Format metrics
        formatted_metrics = metrics_calculator.format_metrics(metrics)
        
        return jsonify({'metrics': formatted_metrics})
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/export_data', methods=['GET'])
def export_data():
    """Export trading data"""
    try:
        export_type = request.args.get('type', 'trades')
        
        if export_type == 'trades':
            # Export trades to CSV
            filename = f"trades_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            trade_tracker.export_trades_csv(filename)
            
            return jsonify({
                'status': 'success',
                'message': f'Trades exported to {filename}',
                'filename': filename
            })
        
        elif export_type == 'config':
            # Export configuration
            filename = f"config_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
            config_manager.export_config(filename)
            
            return jsonify({
                'status': 'success',
                'message': f'Configuration exported to {filename}',
                'filename': filename
            })
        
        else:
            return jsonify({'error': 'Invalid export type'}), 400
        
    except Exception as e:
        logger.error(f"Error exporting data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for frontend"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/exchange/configure', methods=['POST'])
def configure_exchange():
    """Configure exchange API credentials"""
    try:
        data = request.get_json()
        exchange_name = data.get('exchange')
        config_data = data.get('config', {})
        
        if not exchange_name:
            return jsonify({'error': 'Exchange name required'}), 400
        
        # Save exchange configuration securely
        # In production, encrypt these credentials
        exchange_config = {
            'api_key': config_data.get('apiKey', ''),
            'api_secret': config_data.get('apiSecret', ''),
            'passphrase': config_data.get('passphrase', ''),
            'sandbox': config_data.get('sandbox', True),
            'active': True,
            'configured_at': datetime.now().isoformat()
        }
        
        # Update configuration (in production, use secure storage)
        current_config = config_manager.load_config()
        if 'exchanges' not in current_config:
            current_config['exchanges'] = {}
        
        current_config['exchanges'][exchange_name] = exchange_config
        success = config_manager.save_config(current_config)
        
        if success:
            return jsonify({'success': True, 'message': f'{exchange_name} configured successfully'})
        else:
            return jsonify({'error': 'Failed to save configuration'}), 500
            
    except Exception as e:
        logger.error(f"Error configuring exchange: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/exchange/test/<exchange_name>', methods=['POST'])
def test_exchange_connection(exchange_name):
    """Test exchange connection with provided credentials"""
    try:
        data = request.get_json()
        
        # Import exchange manager for testing
        import sys
        sys.path.append('.')
        from exchange_manager import ExchangeManager
        
        # Create exchange manager and test connection
        manager = ExchangeManager()
        
        # Create temporary credentials for testing
        credentials = {
            'apiKey': data.get('apiKey', ''),
            'secret': data.get('apiSecret', ''),
            'sandbox': data.get('sandbox', True)
        }
        
        if data.get('passphrase'):
            credentials['password'] = data.get('passphrase')
        
        # Initialize and test exchange
        exchange = manager.initialize_exchange(exchange_name, credentials, data.get('sandbox', True))
        
        if exchange:
            # Test connection
            test_result = manager.test_exchange_connection(exchange)
            
            if test_result['connected']:
                return jsonify({
                    'success': True,
                    'message': 'Connection successful',
                    'markets': test_result.get('market_count', 0),
                    'features': {
                        'ticker': test_result.get('ticker_accessible', False),
                        'orderbook': test_result.get('order_book_accessible', False),
                        'balance': test_result.get('balance_accessible', False)
                    }
                })
            else:
                return jsonify({
                    'success': False,
                    'error': test_result.get('error', 'Connection test failed')
                }), 400
        else:
            return jsonify({'success': False, 'error': 'Failed to initialize exchange'}), 400
            
    except Exception as e:
        logger.error(f"Error testing exchange connection: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/exchanges/available', methods=['GET'])
def get_available_exchanges():
    """Get list of available exchanges with their status"""
    try:
        # Import exchange manager
        import sys
        sys.path.append('.')
        from exchange_manager import ExchangeManager
        
        manager = ExchangeManager()
        available = manager.get_available_exchanges()
        
        # Return working crypto exchanges
        working_exchanges = [
            {
                'id': 'binance',
                'name': 'Binance',
                'status': 'working',
                'markets': 2069,
                'features': ['Spot', 'Futures', 'Options'],
                'notes': 'Full sandbox support'
            },
            {
                'id': 'bybit',
                'name': 'Bybit',
                'status': 'working',
                'markets': 2490,
                'features': ['Spot', 'Derivatives'],
                'notes': 'Full sandbox support'
            },
            {
                'id': 'delta',
                'name': 'Delta Exchange',
                'status': 'working',
                'markets': 552,
                'features': ['Spot', 'Futures (INR)'],
                'notes': 'Indian exchange'
            },
            {
                'id': 'gate',
                'name': 'Gate.io',
                'status': 'working',
                'markets': 1329,
                'features': ['Spot', 'Futures'],
                'notes': 'Good market coverage'
            },
            {
                'id': 'bitget',
                'name': 'Bitget',
                'status': 'working',
                'markets': 45,
                'features': ['Spot', 'Futures'],
                'notes': 'Limited markets'
            }
        ]
        
        return jsonify({
            'exchanges': working_exchanges,
            'total_working': len(working_exchanges),
            'total_markets': sum(ex['markets'] for ex in working_exchanges)
        })
        
    except Exception as e:
        logger.error(f"Error getting available exchanges: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/trading/execute', methods=['POST'])
def execute_trade():
    """Execute a live trade on selected exchange"""
    try:
        data = request.get_json()
        
        exchange_name = data.get('exchange')
        symbol = data.get('symbol')
        side = data.get('side')
        order_type = data.get('type')
        amount = data.get('amount')
        price = data.get('price')
        
        if not all([exchange_name, symbol, side, order_type, amount]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Import crypto execution engine
        import sys
        sys.path.append('.')
        from crypto_execution_engine import CryptoExecutionEngine, TradingOrder, OrderType, OrderSide
        
        # Initialize execution engine
        engine = CryptoExecutionEngine()
        
        # Initialize the selected exchange
        init_result = engine.initialize_exchanges([exchange_name], sandbox=True)
        
        if not init_result.get(exchange_name, False):
            return jsonify({'error': f'Failed to initialize {exchange_name}'}), 500
        
        # Create trading order
        trading_order = TradingOrder(
            symbol=symbol,
            side=OrderSide.BUY if side == 'buy' else OrderSide.SELL,
            amount=float(amount),
            order_type=OrderType.MARKET if order_type == 'market' else OrderType.LIMIT,
            price=float(price) if price else None,
            exchange=exchange_name
        )
        
        # Execute order (in sandbox mode for safety)
        import asyncio
        result = asyncio.run(engine.execute_order(trading_order))
        
        if result.success:
            return jsonify({
                'success': True,
                'orderId': result.order_id,
                'executedPrice': result.average_price,
                'executedAmount': result.filled_amount,
                'status': result.status,
                'exchange': result.exchange,
                'message': f'Order executed successfully on {exchange_name}'
            })
        else:
            return jsonify({
                'success': False,
                'error': result.error,
                'message': f'Order execution failed: {result.error}'
            }), 400
            
    except Exception as e:
        logger.error(f"Error executing trade: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/portfolio/multi-exchange', methods=['GET'])
def get_multi_exchange_portfolio():
    """Get portfolio data from all configured exchanges"""
    try:
        # Import crypto execution engine
        import sys
        sys.path.append('.')
        from crypto_execution_engine import CryptoExecutionEngine
        
        # Initialize execution engine
        engine = CryptoExecutionEngine()
        
        # Get configured exchanges from config
        config = config_manager.load_config()
        configured_exchanges = []
        
        for exchange_name, exchange_config in config.get('exchanges', {}).items():
            if exchange_config.get('active') and exchange_config.get('api_key'):
                configured_exchanges.append(exchange_name)
        
        if not configured_exchanges:
            return jsonify({
                'positions': [],
                'balances': [],
                'total_value': 0,
                'message': 'No exchanges configured'
            })
        
        # Initialize exchanges
        init_results = engine.initialize_exchanges(configured_exchanges, sandbox=True)
        working_exchanges = [ex for ex, success in init_results.items() if success]
        
        # Get portfolio data
        import asyncio
        balances = asyncio.run(engine.get_portfolio_balances())
        
        # Format response
        portfolio_data = {
            'positions': [],  # Would be populated with real position data
            'balances': balances,
            'working_exchanges': working_exchanges,
            'total_exchanges': len(configured_exchanges),
            'last_update': datetime.now().isoformat()
        }
        
        return jsonify(portfolio_data)
        
    except Exception as e:
        logger.error(f"Error getting multi-exchange portfolio: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/market-data/<exchange_name>/<symbol>', methods=['GET'])
def get_market_data(exchange_name, symbol):
    """Get real-time market data for a symbol from specific exchange"""
    try:
        # Import crypto execution engine
        import sys
        sys.path.append('.')
        from crypto_execution_engine import CryptoExecutionEngine
        
        # Initialize execution engine
        engine = CryptoExecutionEngine()
        
        # Initialize the exchange
        init_result = engine.initialize_exchanges([exchange_name], sandbox=True)
        
        if not init_result.get(exchange_name, False):
            return jsonify({'error': f'Failed to initialize {exchange_name}'}), 500
        
        # Get market data
        import asyncio
        market_data = asyncio.run(engine.get_market_data(symbol, exchange_name))
        
        if exchange_name in market_data and 'error' not in market_data[exchange_name]:
            data = market_data[exchange_name]
            return jsonify({
                'symbol': symbol,
                'exchange': exchange_name,
                'price': data['ticker']['last'],
                'bid': data['ticker']['bid'],
                'ask': data['ticker']['ask'],
                'volume': data['ticker']['baseVolume'],
                'change': data['ticker']['percentage'],
                'timestamp': data['timestamp'].isoformat()
            })
        else:
            error_msg = market_data.get(exchange_name, {}).get('error', 'Unknown error')
            return jsonify({'error': error_msg}), 500
            
    except Exception as e:
        logger.error(f"Error getting market data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get application status"""
    try:
        active_exchanges = config_manager.get_active_exchanges()
        exchange_status = []
        
        for name, config in active_exchanges.items():
            exchange_status.append({
                'name': name.title(),
                'status': 'connected',
                'mode': 'sandbox' if config.get('demo_mode', True) else 'live'
            })
        
        status = {
            'status': 'healthy',
            'scanner_running': scanner_running,
            'total_trades': len(trade_tracker.trades),
            'open_positions': len(trade_tracker.open_positions),
            'closed_trades': len(trade_tracker.closed_trades),
            'active_exchanges': len(active_exchanges),
            'exchanges': exchange_status,
            'live_trading': config_manager.is_live_trading_enabled(),
            'last_update': datetime.now().isoformat()
        }
        
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({'error': str(e)}), 500

# Configuration API endpoints
@app.route('/api/get_exchanges', methods=['GET'])
def get_exchanges():
    """Get list of available exchanges"""
    try:
        exchanges = get_active_exchanges()
        return jsonify([exchange.to_dict() for exchange in exchanges])
    except Exception as e:
        logger.error(f"Error getting exchanges: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_trading_pairs', methods=['GET'])
def get_trading_pairs():
    """Get list of available trading pairs"""
    try:
        pairs = get_active_trading_pairs()
        return jsonify([pair.to_dict() for pair in pairs])
    except Exception as e:
        logger.error(f"Error getting trading pairs: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_strategies', methods=['GET'])
def get_strategies():
    """Get list of available trading strategies"""
    try:
        strategies = get_active_strategies()
        return jsonify([strategy.to_dict() for strategy in strategies])
    except Exception as e:
        logger.error(f"Error getting strategies: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/update_exchange_config', methods=['POST'])
def update_exchange_config():
    """Update exchange configuration"""
    try:
        data = request.get_json()
        exchange_id = data.get('exchange_id')
        config_data = data.get('config', {})
        
        # Update exchange in database
        exchange = Exchange.query.get(exchange_id)
        if not exchange:
            return jsonify({'error': 'Exchange not found'}), 404
        
        # Update exchange properties
        exchange.active = config_data.get('active', exchange.active)
        exchange.demo_mode = config_data.get('demo_mode', exchange.demo_mode)
        exchange.api_key = config_data.get('api_key', exchange.api_key)
        exchange.api_secret = config_data.get('api_secret', exchange.api_secret)
        exchange.api_passphrase = config_data.get('api_passphrase', exchange.api_passphrase)
        
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Exchange configuration updated'})
        
    except Exception as e:
        logger.error(f"Error updating exchange config: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/update_strategy_config', methods=['POST'])
def update_strategy_config():
    """Update strategy configuration"""
    try:
        data = request.get_json()
        strategy_ids = data.get('strategy_ids', [])
        
        # Update active strategies in configuration
        update_configuration('active_strategies', strategy_ids, 'List of active strategies')
        
        return jsonify({'status': 'success', 'message': 'Strategy configuration updated'})
        
    except Exception as e:
        logger.error(f"Error updating strategy config: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/update_trading_pairs_config', methods=['POST'])
def update_trading_pairs_config():
    """Update trading pairs configuration"""
    try:
        data = request.get_json()
        pair_ids = data.get('pair_ids', [])
        
        # Get pair symbols from IDs
        pairs = TradingPair.query.filter(TradingPair.id.in_(pair_ids)).all()
        pair_symbols = [pair.symbol for pair in pairs]
        
        # Update active trading pairs in configuration
        update_configuration('active_trading_pairs', pair_symbols, 'List of active trading pairs')
        
        return jsonify({'status': 'success', 'message': 'Trading pairs configuration updated'})
        
    except Exception as e:
        logger.error(f"Error updating trading pairs config: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return render_template('index.html'), 500

if __name__ == '__main__':
    try:
        # Initialize the application
        initialize_app()
        
        # Start Next.js server in background
        logger.info("Starting Next.js frontend server...")
        nextjs_started = start_nextjs_server()
        
        if nextjs_started:
            logger.info("Next.js server started successfully")
            # Give Next.js a moment to start up
            time.sleep(3)
        else:
            logger.warning("Failed to start Next.js server - running Flask only")
        
        logger.info("Starting AlgoTrading Web Application")
        logger.info("🚀 Access the modern UI at: http://localhost:5000")
        logger.info("📊 Legacy dashboard available at: http://localhost:5000/legacy")
        
        # Run the Flask application
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=os.environ.get('DEBUG', 'False').lower() == 'true',
            threaded=True
        )
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        
        # Stop scanner if running
        if scanner_running and scanner:
            scanner.running = False
            
        # Clean up Next.js process
        if nextjs_process:
            nextjs_process.terminate()
            
    except Exception as e:
        logger.error(f"Fatal error starting application: {e}")
        # Clean up Next.js process on error
        if nextjs_process:
            nextjs_process.terminate()
        raise
