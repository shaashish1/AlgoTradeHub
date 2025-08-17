#!/usr/bin/env python3
"""
CCXT Exchange Manager - Integrated from AdrenalineAI Template
Comprehensive exchange management for crypto and stock trading
"""

import ccxt
import asyncio
import json
import yaml
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()

class ExchangeManager:
    """Comprehensive exchange manager for crypto and stock trading"""
    
    def __init__(self, config_file: str = "config.yaml"):
        self.config_file = config_file
        self.config = self.load_config()
        self.exchanges = {}
        self.active_exchange = None
        self.supported_crypto_exchanges = [
            'binance', 'kraken', 'coinbase', 'bybit', 'okx', 'kucoin',
            'huobi', 'bitget', 'mexc', 'bitfinex', 'gate', 'poloniex',
            'wazirx', 'bitbns', 'delta'  # Indian exchanges
        ]
        self.supported_stock_exchanges = [
            'fyers', 'zerodha', 'upstox', 'angel', 'iifl'  # Indian stock brokers
        ]
        
    def load_config(self) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}
    
    def get_available_exchanges(self) -> Dict[str, List[str]]:
        """Get all available exchanges categorized by type"""
        ccxt_exchanges = ccxt.exchanges
        
        available = {
            'crypto': [],
            'stock': [],
            'supported_crypto': [],
            'supported_stock': []
        }
        
        # Filter crypto exchanges
        for exchange in ccxt_exchanges:
            if exchange in self.supported_crypto_exchanges:
                available['supported_crypto'].append(exchange)
            available['crypto'].append(exchange)
        
        # Add stock exchanges (these would need custom implementations)
        available['stock'] = self.supported_stock_exchanges
        available['supported_stock'] = []  # None currently implemented
        
        return available
    
    def initialize_exchange(self, exchange_name: str, credentials: Dict = None, sandbox: bool = True) -> Optional[ccxt.Exchange]:
        """Initialize a specific exchange with credentials"""
        try:
            if exchange_name not in ccxt.exchanges:
                logger.error(f"Exchange {exchange_name} not supported by CCXT")
                return None
            
            # Get exchange class
            exchange_class = getattr(ccxt, exchange_name)
            
            # Prepare configuration
            config = {
                'sandbox': sandbox,
                'enableRateLimit': True,
                'timeout': 30000,
            }
            
            # Add credentials if provided
            if credentials:
                config.update(credentials)
            elif exchange_name in self.config.get('exchanges', {}):
                exchange_config = self.config['exchanges'][exchange_name]
                if exchange_config.get('api_key') and exchange_config.get('secret'):
                    config.update({
                        'apiKey': exchange_config['api_key'],
                        'secret': exchange_config['secret'],
                        'sandbox': exchange_config.get('sandbox', True)
                    })
                    
                    # Add passphrase if required (for exchanges like OKX)
                    if 'passphrase' in exchange_config:
                        config['password'] = exchange_config['passphrase']
            
            # Initialize exchange
            exchange = exchange_class(config)
            
            # Test connection
            try:
                exchange.load_markets()
                logger.info(f"✅ {exchange_name} initialized successfully")
                return exchange
            except Exception as e:
                logger.warning(f"⚠️ {exchange_name} initialized but connection test failed: {e}")
                return exchange
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize {exchange_name}: {e}")
            return None
    
    def test_exchange_connection(self, exchange: ccxt.Exchange) -> Dict[str, Any]:
        """Test exchange connection and capabilities"""
        results = {
            'exchange': exchange.id,
            'connected': False,
            'markets_loaded': False,
            'balance_accessible': False,
            'order_book_accessible': False,
            'ticker_accessible': False,
            'error': None
        }
        
        try:
            # Test market loading
            markets = exchange.load_markets()
            results['markets_loaded'] = True
            results['market_count'] = len(markets)
            
            # Test ticker access
            if exchange.has['fetchTicker']:
                symbols = list(markets.keys())[:5]  # Test first 5 symbols
                for symbol in symbols:
                    try:
                        ticker = exchange.fetch_ticker(symbol)
                        results['ticker_accessible'] = True
                        break
                    except:
                        continue
            
            # Test order book access
            if exchange.has['fetchOrderBook']:
                symbols = list(markets.keys())[:5]
                for symbol in symbols:
                    try:
                        orderbook = exchange.fetch_order_book(symbol)
                        results['order_book_accessible'] = True
                        break
                    except:
                        continue
            
            # Test balance access (requires API credentials)
            if exchange.has['fetchBalance']:
                try:
                    balance = exchange.fetch_balance()
                    results['balance_accessible'] = True
                except:
                    pass  # Expected to fail without proper credentials
            
            results['connected'] = True
            
        except Exception as e:
            results['error'] = str(e)
            logger.error(f"Connection test failed for {exchange.id}: {e}")
        
        return results
    
    async def test_all_crypto_exchanges(self) -> Dict[str, Dict]:
        """Test all supported crypto exchanges"""
        console.print("🧪 Testing All Crypto Exchanges", style="bold blue")
        
        results = {}
        available = self.get_available_exchanges()
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Testing exchanges...", total=len(available['supported_crypto']))
            
            for exchange_name in available['supported_crypto']:
                try:
                    console.print(f"\n🔍 Testing {exchange_name}...", style="yellow")
                    
                    # Initialize exchange
                    exchange = self.initialize_exchange(exchange_name, sandbox=True)
                    if not exchange:
                        results[exchange_name] = {'status': 'failed_init', 'error': 'Initialization failed'}
                        progress.advance(task)
                        continue
                    
                    # Test connection
                    test_result = self.test_exchange_connection(exchange)
                    results[exchange_name] = test_result
                    
                    # Display result
                    status = "✅" if test_result['connected'] else "❌"
                    console.print(f"{status} {exchange_name}: {test_result.get('market_count', 0)} markets", style="green" if test_result['connected'] else "red")
                    
                    progress.advance(task)
                    
                    # Small delay to respect rate limits
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    results[exchange_name] = {'status': 'error', 'error': str(e)}
                    console.print(f"❌ {exchange_name}: {e}", style="red")
                    progress.advance(task)
        
        return results
    
    def test_crypto_trading_features(self, exchange_name: str) -> Dict[str, Any]:
        """Test specific trading features for a crypto exchange"""
        exchange = self.initialize_exchange(exchange_name, sandbox=True)
        if not exchange:
            return {'error': 'Failed to initialize exchange'}
        
        features = {
            'exchange': exchange_name,
            'spot_trading': False,
            'margin_trading': False,
            'futures_trading': False,
            'options_trading': False,
            'lending': False,
            'staking': False,
            'supported_order_types': [],
            'supported_timeframes': [],
            'fee_structure': {},
            'popular_pairs': []
        }
        
        try:
            # Load markets
            markets = exchange.load_markets()
            
            # Check market types
            for symbol, market in markets.items():
                if market.get('spot'):
                    features['spot_trading'] = True
                if market.get('margin'):
                    features['margin_trading'] = True
                if market.get('future'):
                    features['futures_trading'] = True
                if market.get('option'):
                    features['options_trading'] = True
            
            # Get supported order types
            if hasattr(exchange, 'options') and 'orderTypes' in exchange.options:
                features['supported_order_types'] = list(exchange.options['orderTypes'].keys())
            
            # Get supported timeframes
            if exchange.has['fetchOHLCV']:
                features['supported_timeframes'] = list(exchange.timeframes.keys()) if hasattr(exchange, 'timeframes') else []
            
            # Get fee structure
            if hasattr(exchange, 'fees'):
                features['fee_structure'] = {
                    'trading': exchange.fees.get('trading', {}),
                    'funding': exchange.fees.get('funding', {})
                }
            
            # Get popular trading pairs
            popular_bases = ['BTC', 'ETH', 'BNB', 'ADA', 'SOL', 'DOT', 'MATIC']
            popular_quotes = ['USDT', 'USD', 'BTC', 'ETH']
            
            for base in popular_bases:
                for quote in popular_quotes:
                    symbol = f"{base}/{quote}"
                    if symbol in markets:
                        features['popular_pairs'].append(symbol)
                        if len(features['popular_pairs']) >= 10:
                            break
                if len(features['popular_pairs']) >= 10:
                    break
            
        except Exception as e:
            features['error'] = str(e)
        
        return features
    
    def analyze_stock_trading_support(self) -> Dict[str, Any]:
        """Analyze current stock trading support and limitations"""
        analysis = {
            'ccxt_stock_support': False,
            'supported_stock_exchanges': [],
            'indian_broker_status': {},
            'limitations': [],
            'recommendations': []
        }
        
        # Check CCXT stock support
        ccxt_exchanges = ccxt.exchanges
        stock_related = ['alpaca', 'tradier', 'robinhood']  # Known stock-supporting exchanges
        
        for exchange in stock_related:
            if exchange in ccxt_exchanges:
                analysis['supported_stock_exchanges'].append(exchange)
                analysis['ccxt_stock_support'] = True
        
        # Analyze Indian broker support
        indian_brokers = {
            'fyers': {
                'api_available': True,
                'ccxt_support': False,
                'custom_integration_needed': True,
                'features': ['Equity', 'F&O', 'Currency', 'Commodity'],
                'status': 'Requires custom API integration'
            },
            'zerodha': {
                'api_available': True,
                'ccxt_support': False,
                'custom_integration_needed': True,
                'features': ['Equity', 'F&O', 'Currency', 'Commodity'],
                'status': 'KiteConnect API available'
            },
            'upstox': {
                'api_available': True,
                'ccxt_support': False,
                'custom_integration_needed': True,
                'features': ['Equity', 'F&O', 'Currency', 'Commodity'],
                'status': 'Upstox API 2.0 available'
            },
            'angel': {
                'api_available': True,
                'ccxt_support': False,
                'custom_integration_needed': True,
                'features': ['Equity', 'F&O', 'Currency', 'Commodity'],
                'status': 'SmartAPI available'
            }
        }
        
        analysis['indian_broker_status'] = indian_brokers
        
        # Identify limitations
        analysis['limitations'] = [
            "CCXT has limited stock exchange support",
            "Indian brokers not supported by CCXT",
            "Custom API integration required for Indian stocks",
            "Different authentication mechanisms needed",
            "Regulatory compliance requirements vary by broker"
        ]
        
        # Provide recommendations
        analysis['recommendations'] = [
            "Implement custom adapters for Indian brokers",
            "Use broker-specific Python SDKs (KiteConnect, Upstox API, etc.)",
            "Create unified interface for stock trading",
            "Implement proper error handling for broker APIs",
            "Add support for Indian market timings and holidays"
        ]
        
        return analysis
    
    def display_test_results(self, crypto_results: Dict, stock_analysis: Dict):
        """Display comprehensive test results"""
        console.print(Panel.fit("🧪 Exchange Testing Results", style="bold magenta"))
        
        # Crypto results
        console.print("\n💰 Crypto Exchange Results", style="bold green")
        
        crypto_table = Table(title="Crypto Exchange Test Results")
        crypto_table.add_column("Exchange", style="cyan")
        crypto_table.add_column("Status", style="green")
        crypto_table.add_column("Markets", style="yellow")
        crypto_table.add_column("Features", style="blue")
        
        for exchange, result in crypto_results.items():
            if result.get('connected'):
                status = "✅ Connected"
                markets = str(result.get('market_count', 0))
                features = []
                if result.get('ticker_accessible'):
                    features.append("Ticker")
                if result.get('order_book_accessible'):
                    features.append("OrderBook")
                if result.get('balance_accessible'):
                    features.append("Balance")
                feature_str = ", ".join(features) if features else "Basic"
            else:
                status = "❌ Failed"
                markets = "0"
                feature_str = result.get('error', 'Unknown error')[:30]
            
            crypto_table.add_row(exchange, status, markets, feature_str)
        
        console.print(crypto_table)
        
        # Stock analysis
        console.print("\n📈 Stock Trading Analysis", style="bold blue")
        
        stock_table = Table(title="Stock Exchange Support Analysis")
        stock_table.add_column("Broker", style="cyan")
        stock_table.add_column("API Available", style="green")
        stock_table.add_column("CCXT Support", style="yellow")
        stock_table.add_column("Status", style="blue")
        
        for broker, info in stock_analysis['indian_broker_status'].items():
            api_status = "✅ Yes" if info['api_available'] else "❌ No"
            ccxt_status = "✅ Yes" if info['ccxt_support'] else "❌ No"
            status = info['status']
            
            stock_table.add_row(broker, api_status, ccxt_status, status)
        
        console.print(stock_table)
        
        # Summary
        console.print("\n📊 Summary", style="bold yellow")
        
        working_crypto = len([r for r in crypto_results.values() if r.get('connected')])
        total_crypto = len(crypto_results)
        
        console.print(f"✅ Crypto Exchanges Working: {working_crypto}/{total_crypto}")
        console.print(f"❌ Stock Exchanges (CCXT): 0/{len(stock_analysis['indian_broker_status'])}")
        console.print(f"🔧 Custom Integration Needed: {len(stock_analysis['indian_broker_status'])} brokers")

async def main():
    """Main testing function"""
    try:
        console.print(Panel.fit("🚀 AlgoTradeHub Exchange Integration Test", style="bold cyan"))
        
        # Initialize exchange manager
        manager = ExchangeManager()
        
        # Test all crypto exchanges
        crypto_results = await manager.test_all_crypto_exchanges()
        
        # Analyze stock trading support
        stock_analysis = manager.analyze_stock_trading_support()
        
        # Display results
        manager.display_test_results(crypto_results, stock_analysis)
        
        # Save results
        results = {
            'timestamp': datetime.now().isoformat(),
            'crypto_exchanges': crypto_results,
            'stock_analysis': stock_analysis
        }
        
        with open('exchange_test_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        console.print(f"\n💾 Results saved to exchange_test_results.json", style="green")
        
        # Provide next steps
        console.print("\n🎯 Next Steps:", style="bold yellow")
        console.print("1. Configure API credentials for working crypto exchanges")
        console.print("2. Implement custom adapters for Indian stock brokers")
        console.print("3. Test live trading with small amounts")
        console.print("4. Integrate with existing AlgoTradeHub interface")
        
    except Exception as e:
        console.print(f"❌ Error in main: {e}", style="red")
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    asyncio.run(main())