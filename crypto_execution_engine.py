#!/usr/bin/env python3
"""
Crypto Execution Engine - Based on AdrenalineAI CCXT Template
Handles actual crypto trading execution across multiple exchanges
"""

import ccxt
import asyncio
import json
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
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

@dataclass
class TradingOrder:
    symbol: str
    side: OrderSide
    amount: float
    order_type: OrderType
    price: Optional[float] = None
    stop_price: Optional[float] = None
    exchange: Optional[str] = None
    
@dataclass
class OrderResult:
    success: bool
    order_id: Optional[str] = None
    filled_amount: float = 0.0
    average_price: float = 0.0
    status: str = "unknown"
    error: Optional[str] = None
    exchange: Optional[str] = None
    timestamp: Optional[datetime] = None

class CryptoExecutionEngine:
    """Comprehensive crypto trading execution engine"""
    
    def __init__(self, config_file: str = "config.yaml"):
        self.config_file = config_file
        self.exchanges = {}
        self.active_exchanges = []
        self.order_history = []
        self.positions = {}
        
    def initialize_exchanges(self, exchange_names: List[str], sandbox: bool = True) -> Dict[str, bool]:
        """Initialize multiple exchanges for trading"""
        results = {}
        
        for exchange_name in exchange_names:
            try:
                if exchange_name not in ccxt.exchanges:
                    results[exchange_name] = False
                    continue
                
                # Get exchange class
                exchange_class = getattr(ccxt, exchange_name)
                
                # Load configuration
                config = {
                    'sandbox': sandbox,
                    'enableRateLimit': True,
                    'timeout': 30000,
                }
                
                # Initialize exchange
                exchange = exchange_class(config)
                exchange.load_markets()
                
                self.exchanges[exchange_name] = exchange
                self.active_exchanges.append(exchange_name)
                results[exchange_name] = True
                
                logger.info(f"✅ {exchange_name} initialized for trading")
                
            except Exception as e:
                logger.error(f"❌ Failed to initialize {exchange_name}: {e}")
                results[exchange_name] = False
        
        return results
    
    async def get_market_data(self, symbol: str, exchange_name: str = None) -> Dict[str, Any]:
        """Get comprehensive market data for a symbol"""
        if exchange_name and exchange_name in self.exchanges:
            exchanges_to_check = [exchange_name]
        else:
            exchanges_to_check = self.active_exchanges
        
        market_data = {}
        
        for ex_name in exchanges_to_check:
            try:
                exchange = self.exchanges[ex_name]
                
                # Get ticker
                ticker = exchange.fetch_ticker(symbol)
                
                # Get order book
                orderbook = exchange.fetch_order_book(symbol, limit=10)
                
                # Get recent trades
                trades = exchange.fetch_trades(symbol, limit=10) if exchange.has['fetchTrades'] else []
                
                market_data[ex_name] = {
                    'ticker': ticker,
                    'orderbook': orderbook,
                    'recent_trades': trades,
                    'timestamp': datetime.now()
                }
                
            except Exception as e:
                logger.warning(f"Failed to get market data from {ex_name}: {e}")
                market_data[ex_name] = {'error': str(e)}
        
        return market_data
    
    async def execute_order(self, order: TradingOrder) -> OrderResult:
        """Execute a trading order"""
        try:
            # Determine which exchange to use
            if order.exchange and order.exchange in self.exchanges:
                exchange = self.exchanges[order.exchange]
                exchange_name = order.exchange
            elif self.active_exchanges:
                exchange_name = self.active_exchanges[0]  # Use first available
                exchange = self.exchanges[exchange_name]
            else:
                return OrderResult(
                    success=False,
                    error="No active exchanges available",
                    timestamp=datetime.now()
                )
            
            # Validate symbol
            if order.symbol not in exchange.markets:
                return OrderResult(
                    success=False,
                    error=f"Symbol {order.symbol} not available on {exchange_name}",
                    exchange=exchange_name,
                    timestamp=datetime.now()
                )
            
            # Prepare order parameters
            order_params = {}
            
            # Execute order based on type
            if order.order_type == OrderType.MARKET:
                result = exchange.create_market_order(
                    order.symbol,
                    order.side.value,
                    order.amount
                )
            elif order.order_type == OrderType.LIMIT:
                if not order.price:
                    return OrderResult(
                        success=False,
                        error="Price required for limit order",
                        exchange=exchange_name,
                        timestamp=datetime.now()
                    )
                result = exchange.create_limit_order(
                    order.symbol,
                    order.side.value,
                    order.amount,
                    order.price
                )
            else:
                return OrderResult(
                    success=False,
                    error=f"Order type {order.order_type} not implemented",
                    exchange=exchange_name,
                    timestamp=datetime.now()
                )
            
            # Process result
            order_result = OrderResult(
                success=True,
                order_id=result.get('id'),
                filled_amount=result.get('filled', 0.0),
                average_price=result.get('average', 0.0),
                status=result.get('status', 'unknown'),
                exchange=exchange_name,
                timestamp=datetime.now()
            )
            
            # Store in history
            self.order_history.append({
                'order': order,
                'result': order_result,
                'raw_response': result
            })
            
            logger.info(f"✅ Order executed: {order.symbol} {order.side.value} {order.amount} on {exchange_name}")
            
            return order_result
            
        except Exception as e:
            error_result = OrderResult(
                success=False,
                error=str(e),
                exchange=exchange_name if 'exchange_name' in locals() else None,
                timestamp=datetime.now()
            )
            
            logger.error(f"❌ Order execution failed: {e}")
            return error_result
    
    async def test_trading_execution(self, test_symbol: str = "BTC/USDT", test_amount: float = 0.001) -> Dict[str, Any]:
        """Test trading execution across all active exchanges"""
        console.print(f"🧪 Testing Trading Execution for {test_symbol}", style="bold blue")
        
        test_results = {}
        
        for exchange_name in self.active_exchanges:
            console.print(f"\n🔍 Testing {exchange_name}...", style="yellow")
            
            try:
                exchange = self.exchanges[exchange_name]
                
                # Check if symbol is available
                if test_symbol not in exchange.markets:
                    test_results[exchange_name] = {
                        'status': 'symbol_not_available',
                        'error': f"Symbol {test_symbol} not available"
                    }
                    continue
                
                # Get current market data
                ticker = exchange.fetch_ticker(test_symbol)
                current_price = ticker['last']
                
                # Test order creation (dry run - we'll cancel immediately)
                test_order = TradingOrder(
                    symbol=test_symbol,
                    side=OrderSide.BUY,
                    amount=test_amount,
                    order_type=OrderType.LIMIT,
                    price=current_price * 0.8,  # 20% below market (unlikely to fill)
                    exchange=exchange_name
                )
                
                # Execute test order
                result = await self.execute_order(test_order)
                
                if result.success and result.order_id:
                    # Try to cancel the order immediately
                    try:
                        cancel_result = exchange.cancel_order(result.order_id, test_symbol)
                        test_results[exchange_name] = {
                            'status': 'success',
                            'order_created': True,
                            'order_cancelled': True,
                            'current_price': current_price,
                            'test_price': test_order.price
                        }
                        console.print(f"✅ {exchange_name}: Order creation and cancellation successful", style="green")
                    except Exception as cancel_error:
                        test_results[exchange_name] = {
                            'status': 'partial_success',
                            'order_created': True,
                            'order_cancelled': False,
                            'cancel_error': str(cancel_error),
                            'current_price': current_price
                        }
                        console.print(f"⚠️ {exchange_name}: Order created but cancellation failed", style="yellow")
                else:
                    test_results[exchange_name] = {
                        'status': 'order_creation_failed',
                        'error': result.error,
                        'current_price': current_price
                    }
                    console.print(f"❌ {exchange_name}: Order creation failed", style="red")
                
            except Exception as e:
                test_results[exchange_name] = {
                    'status': 'error',
                    'error': str(e)
                }
                console.print(f"❌ {exchange_name}: Test failed with error: {e}", style="red")
            
            # Small delay between tests
            await asyncio.sleep(1)
        
        return test_results
    
    async def get_portfolio_balances(self) -> Dict[str, Dict]:
        """Get portfolio balances from all active exchanges"""
        balances = {}
        
        for exchange_name in self.active_exchanges:
            try:
                exchange = self.exchanges[exchange_name]
                balance = exchange.fetch_balance()
                
                # Filter out zero balances
                non_zero_balances = {
                    currency: amounts for currency, amounts in balance.items()
                    if isinstance(amounts, dict) and amounts.get('total', 0) > 0
                }
                
                balances[exchange_name] = non_zero_balances
                
            except Exception as e:
                logger.warning(f"Failed to get balance from {exchange_name}: {e}")
                balances[exchange_name] = {'error': str(e)}
        
        return balances
    
    def get_supported_trading_pairs(self, exchange_name: str = None) -> Dict[str, List[str]]:
        """Get supported trading pairs for exchanges"""
        if exchange_name and exchange_name in self.exchanges:
            exchanges_to_check = [exchange_name]
        else:
            exchanges_to_check = self.active_exchanges
        
        supported_pairs = {}
        
        for ex_name in exchanges_to_check:
            try:
                exchange = self.exchanges[ex_name]
                markets = exchange.markets
                
                # Categorize pairs
                pairs = {
                    'spot': [],
                    'futures': [],
                    'options': [],
                    'popular': []
                }
                
                popular_bases = ['BTC', 'ETH', 'BNB', 'ADA', 'SOL', 'DOT', 'MATIC', 'AVAX']
                popular_quotes = ['USDT', 'USD', 'BTC', 'ETH']
                
                for symbol, market in markets.items():
                    if market.get('spot'):
                        pairs['spot'].append(symbol)
                    if market.get('future'):
                        pairs['futures'].append(symbol)
                    if market.get('option'):
                        pairs['options'].append(symbol)
                    
                    # Check if it's a popular pair
                    base, quote = symbol.split('/')
                    if base in popular_bases and quote in popular_quotes:
                        pairs['popular'].append(symbol)
                
                supported_pairs[ex_name] = pairs
                
            except Exception as e:
                logger.error(f"Failed to get trading pairs from {ex_name}: {e}")
                supported_pairs[ex_name] = {'error': str(e)}
        
        return supported_pairs
    
    def display_execution_summary(self, test_results: Dict, balances: Dict, trading_pairs: Dict):
        """Display comprehensive execution test summary"""
        console.print(Panel.fit("📊 Crypto Execution Test Summary", style="bold magenta"))
        
        # Execution test results
        console.print("\n🔄 Order Execution Tests", style="bold green")
        
        exec_table = Table(title="Trading Execution Test Results")
        exec_table.add_column("Exchange", style="cyan")
        exec_table.add_column("Status", style="green")
        exec_table.add_column("Order Creation", style="yellow")
        exec_table.add_column("Order Cancellation", style="blue")
        exec_table.add_column("Notes", style="white")
        
        for exchange, result in test_results.items():
            status = result.get('status', 'unknown')
            if status == 'success':
                status_icon = "✅ Success"
                order_created = "✅" if result.get('order_created') else "❌"
                order_cancelled = "✅" if result.get('order_cancelled') else "❌"
                notes = f"Price: ${result.get('current_price', 0):.2f}"
            elif status == 'partial_success':
                status_icon = "⚠️ Partial"
                order_created = "✅"
                order_cancelled = "❌"
                notes = "Cancel failed"
            else:
                status_icon = "❌ Failed"
                order_created = "❌"
                order_cancelled = "❌"
                notes = result.get('error', 'Unknown error')[:30]
            
            exec_table.add_row(exchange, status_icon, order_created, order_cancelled, notes)
        
        console.print(exec_table)
        
        # Balance summary
        console.print("\n💰 Portfolio Balances", style="bold blue")
        
        balance_table = Table(title="Exchange Balances")
        balance_table.add_column("Exchange", style="cyan")
        balance_table.add_column("Status", style="green")
        balance_table.add_column("Currencies", style="yellow")
        balance_table.add_column("Notes", style="white")
        
        for exchange, balance_data in balances.items():
            if 'error' in balance_data:
                status = "❌ Error"
                currencies = "0"
                notes = balance_data['error'][:30]
            else:
                status = "✅ Connected"
                currencies = str(len([k for k, v in balance_data.items() if isinstance(v, dict)]))
                notes = "Balance accessible"
            
            balance_table.add_row(exchange, status, currencies, notes)
        
        console.print(balance_table)
        
        # Trading pairs summary
        console.print("\n📈 Trading Pairs Available", style="bold yellow")
        
        pairs_table = Table(title="Supported Trading Pairs")
        pairs_table.add_column("Exchange", style="cyan")
        pairs_table.add_column("Spot", style="green")
        pairs_table.add_column("Futures", style="yellow")
        pairs_table.add_column("Popular", style="blue")
        pairs_table.add_column("Total", style="white")
        
        for exchange, pairs_data in trading_pairs.items():
            if 'error' in pairs_data:
                pairs_table.add_row(exchange, "❌", "❌", "❌", "Error")
            else:
                spot_count = len(pairs_data.get('spot', []))
                futures_count = len(pairs_data.get('futures', []))
                popular_count = len(pairs_data.get('popular', []))
                total_count = spot_count + futures_count
                
                pairs_table.add_row(
                    exchange,
                    str(spot_count),
                    str(futures_count),
                    str(popular_count),
                    str(total_count)
                )
        
        console.print(pairs_table)

async def main():
    """Main execution testing function"""
    try:
        console.print(Panel.fit("🚀 Crypto Execution Engine Test", style="bold cyan"))
        
        # Initialize execution engine
        engine = CryptoExecutionEngine()
        
        # Test exchanges (using sandbox mode)
        test_exchanges = ['binance', 'kraken', 'bybit', 'okx']
        
        console.print(f"🔧 Initializing exchanges: {', '.join(test_exchanges)}")
        init_results = engine.initialize_exchanges(test_exchanges, sandbox=True)
        
        working_exchanges = [ex for ex, success in init_results.items() if success]
        console.print(f"✅ Working exchanges: {', '.join(working_exchanges)}")
        
        if not working_exchanges:
            console.print("❌ No exchanges initialized successfully", style="red")
            return
        
        # Test trading execution
        test_results = await engine.test_trading_execution("BTC/USDT", 0.001)
        
        # Get portfolio balances
        balances = await engine.get_portfolio_balances()
        
        # Get supported trading pairs
        trading_pairs = engine.get_supported_trading_pairs()
        
        # Display summary
        engine.display_execution_summary(test_results, balances, trading_pairs)
        
        # Save results
        results = {
            'timestamp': datetime.now().isoformat(),
            'initialization': init_results,
            'execution_tests': test_results,
            'balances': balances,
            'trading_pairs': {k: {pair_type: len(pairs) for pair_type, pairs in v.items() if isinstance(pairs, list)} 
                             for k, v in trading_pairs.items() if 'error' not in v}
        }
        
        with open('crypto_execution_test_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        console.print(f"\n💾 Results saved to crypto_execution_test_results.json", style="green")
        
    except Exception as e:
        console.print(f"❌ Error in main: {e}", style="red")
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    asyncio.run(main())