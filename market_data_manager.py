#!/usr/bin/env python3
"""
Market Data Manager - Intelligent data source selection and management
Handles optimal data sourcing across multiple exchanges
"""

import ccxt
import asyncio
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import logging
from dataclasses import dataclass
from enum import Enum
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DataSource:
    exchange_name: str
    reliability_score: float
    latency_ms: float
    coverage_score: float
    cost_score: float
    last_updated: datetime
    
@dataclass
class MarketData:
    symbol: str
    price: float
    volume: float
    timestamp: datetime
    bid: float
    ask: float
    source_exchange: str
    high_24h: float = 0.0
    low_24h: float = 0.0
    change_24h: float = 0.0
    
@dataclass
class OrderBook:
    symbol: str
    bids: List[Tuple[float, float]]  # [(price, amount), ...]
    asks: List[Tuple[float, float]]
    timestamp: datetime
    source_exchange: str

class MarketDataManager:
    """Intelligent market data management with optimal source selection"""
    
    def __init__(self):
        self.data_sources: Dict[str, DataSource] = {}
        self.source_rankings: Dict[str, List[str]] = {}  # symbol -> ranked list of exchanges
        self.fallback_sources: Dict[str, List[str]] = {}  # primary -> fallback list
        self.exchanges: Dict[str, ccxt.Exchange] = {}
        self.cache: Dict[str, Dict] = {}  # symbol -> cached data
        self.cache_duration = 30  # seconds
        
    def initialize_data_sources(self, exchange_configs: Dict[str, Dict]) -> Dict[str, bool]:
        """Initialize data sources with exchange configurations"""
        results = {}
        
        for exchange_name, config in exchange_configs.items():
            try:
                if exchange_name not in ccxt.exchanges:
                    results[exchange_name] = False
                    continue
                
                # Initialize exchange
                exchange_class = getattr(ccxt, exchange_name)
                exchange = exchange_class({
                    'sandbox': config.get('sandbox', True),
                    'enableRateLimit': True,
                    'timeout': 30000,
                })
                
                # Load markets
                exchange.load_markets()
                self.exchanges[exchange_name] = exchange
                
                # Create data source entry
                self.data_sources[exchange_name] = DataSource(
                    exchange_name=exchange_name,
                    reliability_score=self._calculate_reliability_score(exchange_name),
                    latency_ms=self._measure_latency(exchange),
                    coverage_score=self._calculate_coverage_score(exchange),
                    cost_score=self._calculate_cost_score(exchange_name),
                    last_updated=datetime.now()
                )
                
                results[exchange_name] = True
                logger.info(f"✅ Data source {exchange_name} initialized")
                
            except Exception as e:
                logger.error(f"❌ Failed to initialize data source {exchange_name}: {e}")
                results[exchange_name] = False
        
        # Build source rankings
        self._build_source_rankings()
        
        return results
    
    def _calculate_reliability_score(self, exchange_name: str) -> float:
        """Calculate reliability score based on exchange reputation"""
        # Known reliable exchanges get higher scores
        reliability_map = {
            'binance': 0.95,
            'kraken': 0.90,
            'coinbase': 0.88,
            'bybit': 0.85,
            'okx': 0.82,
            'kucoin': 0.80,
            'gate': 0.78,
            'huobi': 0.75,
            'bitget': 0.72,
            'delta': 0.70,  # Indian exchange
        }
        return reliability_map.get(exchange_name, 0.60)  # Default score
    
    def _measure_latency(self, exchange: ccxt.Exchange) -> float:
        """Measure average latency for the exchange"""
        try:
            start_time = time.time()
            # Simple ping test - get server time
            if hasattr(exchange, 'fetch_time'):
                exchange.fetch_time()
            else:
                # Fallback - fetch a ticker
                markets = list(exchange.markets.keys())
                if markets:
                    exchange.fetch_ticker(markets[0])
            
            latency = (time.time() - start_time) * 1000  # Convert to ms
            return min(latency, 5000)  # Cap at 5 seconds
            
        except Exception as e:
            logger.warning(f"Failed to measure latency for {exchange.id}: {e}")
            return 5000  # High latency as penalty
    
    def _calculate_coverage_score(self, exchange: ccxt.Exchange) -> float:
        """Calculate coverage score based on available markets"""
        try:
            market_count = len(exchange.markets)
            # Normalize to 0-1 scale (assuming 2000+ markets is excellent)
            return min(market_count / 2000, 1.0)
        except:
            return 0.0
    
    def _calculate_cost_score(self, exchange_name: str) -> float:
        """Calculate cost score based on rate limits and fees"""
        # Higher score = lower cost (better)
        cost_map = {
            'binance': 0.90,  # Good rate limits
            'kraken': 0.85,
            'coinbase': 0.80,
            'bybit': 0.88,
            'okx': 0.85,
            'kucoin': 0.82,
            'gate': 0.80,
            'huobi': 0.78,
            'bitget': 0.75,
            'delta': 0.70,
        }
        return cost_map.get(exchange_name, 0.60)
    
    def _build_source_rankings(self):
        """Build source rankings for each available symbol"""
        # Get all unique symbols across exchanges
        all_symbols = set()
        for exchange in self.exchanges.values():
            all_symbols.update(exchange.markets.keys())
        
        # Rank sources for each symbol
        for symbol in all_symbols:
            available_sources = []
            
            for exchange_name, exchange in self.exchanges.items():
                if symbol in exchange.markets:
                    source = self.data_sources[exchange_name]
                    # Calculate composite score
                    composite_score = (
                        source.reliability_score * 0.4 +
                        (1 - source.latency_ms / 5000) * 0.3 +  # Lower latency = higher score
                        source.coverage_score * 0.2 +
                        source.cost_score * 0.1
                    )
                    available_sources.append((exchange_name, composite_score))
            
            # Sort by composite score (descending)
            available_sources.sort(key=lambda x: x[1], reverse=True)
            self.source_rankings[symbol] = [source[0] for source in available_sources]
            
            # Set up fallback sources (all except the primary)
            if len(available_sources) > 1:
                primary = available_sources[0][0]
                fallbacks = [source[0] for source in available_sources[1:]]
                self.fallback_sources[f"{symbol}:{primary}"] = fallbacks
    
    def get_optimal_data_source(self, symbol: str) -> Optional[str]:
        """Get the optimal data source for a symbol"""
        if symbol in self.source_rankings and self.source_rankings[symbol]:
            return self.source_rankings[symbol][0]
        return None
    
    async def fetch_market_data(self, symbol: str, timeframe: str = '1m') -> Optional[MarketData]:
        """Fetch market data from optimal source with fallback"""
        # Check cache first
        cache_key = f"{symbol}:{timeframe}"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if (datetime.now() - cached_data['timestamp']).seconds < self.cache_duration:
                return cached_data['data']
        
        # Get optimal source
        primary_source = self.get_optimal_data_source(symbol)
        if not primary_source:
            logger.warning(f"No data source available for {symbol}")
            return None
        
        # Try primary source
        market_data = await self._fetch_from_source(symbol, primary_source)
        if market_data:
            # Cache the result
            self.cache[cache_key] = {
                'data': market_data,
                'timestamp': datetime.now()
            }
            return market_data
        
        # Try fallback sources
        fallback_key = f"{symbol}:{primary_source}"
        if fallback_key in self.fallback_sources:
            for fallback_source in self.fallback_sources[fallback_key]:
                logger.info(f"Trying fallback source {fallback_source} for {symbol}")
                market_data = await self._fetch_from_source(symbol, fallback_source)
                if market_data:
                    # Cache the result
                    self.cache[cache_key] = {
                        'data': market_data,
                        'timestamp': datetime.now()
                    }
                    return market_data
        
        logger.error(f"Failed to fetch market data for {symbol} from all sources")
        return None
    
    async def _fetch_from_source(self, symbol: str, source: str) -> Optional[MarketData]:
        """Fetch market data from a specific source"""
        try:
            if source not in self.exchanges:
                return None
            
            exchange = self.exchanges[source]
            
            # Fetch ticker
            ticker = exchange.fetch_ticker(symbol)
            
            # Create MarketData object
            market_data = MarketData(
                symbol=symbol,
                price=ticker.get('last', 0.0),
                volume=ticker.get('baseVolume', 0.0),
                timestamp=datetime.fromtimestamp(ticker.get('timestamp', 0) / 1000),
                bid=ticker.get('bid', 0.0),
                ask=ticker.get('ask', 0.0),
                source_exchange=source,
                high_24h=ticker.get('high', 0.0),
                low_24h=ticker.get('low', 0.0),
                change_24h=ticker.get('percentage', 0.0)
            )
            
            return market_data
            
        except Exception as e:
            logger.warning(f"Failed to fetch {symbol} from {source}: {e}")
            return None
    
    async def get_order_book(self, symbol: str, limit: int = 10) -> Optional[OrderBook]:
        """Get order book from optimal source"""
        primary_source = self.get_optimal_data_source(symbol)
        if not primary_source:
            return None
        
        try:
            exchange = self.exchanges[primary_source]
            orderbook_data = exchange.fetch_order_book(symbol, limit)
            
            return OrderBook(
                symbol=symbol,
                bids=orderbook_data.get('bids', []),
                asks=orderbook_data.get('asks', []),
                timestamp=datetime.fromtimestamp(orderbook_data.get('timestamp', 0) / 1000),
                source_exchange=primary_source
            )
            
        except Exception as e:
            logger.error(f"Failed to fetch order book for {symbol}: {e}")
            return None
    
    async def get_price_history(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> Optional[pd.DataFrame]:
        """Get price history from optimal source"""
        primary_source = self.get_optimal_data_source(symbol)
        if not primary_source:
            return None
        
        try:
            exchange = self.exchanges[primary_source]
            
            if not exchange.has['fetchOHLCV']:
                logger.warning(f"{primary_source} doesn't support OHLCV data")
                return None
            
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['source'] = primary_source
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to fetch price history for {symbol}: {e}")
            return None
    
    def register_fallback_source(self, primary: str, fallback: str):
        """Register a custom fallback source"""
        if primary not in self.fallback_sources:
            self.fallback_sources[primary] = []
        
        if fallback not in self.fallback_sources[primary]:
            self.fallback_sources[primary].append(fallback)
    
    def get_data_source_status(self) -> Dict[str, Dict]:
        """Get status of all data sources"""
        status = {}
        
        for source_name, source in self.data_sources.items():
            try:
                exchange = self.exchanges[source_name]
                # Test connectivity
                start_time = time.time()
                markets = exchange.markets
                response_time = (time.time() - start_time) * 1000
                
                status[source_name] = {
                    'status': 'connected',
                    'reliability_score': source.reliability_score,
                    'latency_ms': response_time,
                    'coverage_score': source.coverage_score,
                    'market_count': len(markets),
                    'last_updated': source.last_updated.isoformat()
                }
                
            except Exception as e:
                status[source_name] = {
                    'status': 'error',
                    'error': str(e),
                    'last_updated': source.last_updated.isoformat()
                }
        
        return status
    
    def get_symbol_sources(self, symbol: str) -> Dict[str, Any]:
        """Get available sources for a specific symbol"""
        if symbol not in self.source_rankings:
            return {'symbol': symbol, 'sources': [], 'primary': None, 'fallbacks': []}
        
        sources = self.source_rankings[symbol]
        primary = sources[0] if sources else None
        fallbacks = sources[1:] if len(sources) > 1 else []
        
        return {
            'symbol': symbol,
            'sources': sources,
            'primary': primary,
            'fallbacks': fallbacks,
            'source_details': {
                source: {
                    'reliability': self.data_sources[source].reliability_score,
                    'latency': self.data_sources[source].latency_ms,
                    'coverage': self.data_sources[source].coverage_score
                } for source in sources if source in self.data_sources
            }
        }

async def main():
    """Test market data manager"""
    try:
        print("🧪 Testing Market Data Manager")
        
        # Initialize manager
        manager = MarketDataManager()
        
        # Test configuration
        test_config = {
            'binance': {'sandbox': True},
            'kraken': {'sandbox': True},
            'bybit': {'sandbox': True}
        }
        
        # Initialize data sources
        init_results = manager.initialize_data_sources(test_config)
        print(f"✅ Initialized sources: {init_results}")
        
        # Test market data fetching
        test_symbol = 'BTC/USDT'
        market_data = await manager.fetch_market_data(test_symbol)
        
        if market_data:
            print(f"✅ Market data for {test_symbol}:")
            print(f"   Price: ${market_data.price}")
            print(f"   Source: {market_data.source_exchange}")
            print(f"   Timestamp: {market_data.timestamp}")
        
        # Test order book
        order_book = await manager.get_order_book(test_symbol)
        if order_book:
            print(f"✅ Order book for {test_symbol} from {order_book.source_exchange}")
            print(f"   Best bid: ${order_book.bids[0][0] if order_book.bids else 'N/A'}")
            print(f"   Best ask: ${order_book.asks[0][0] if order_book.asks else 'N/A'}")
        
        # Get data source status
        status = manager.get_data_source_status()
        print(f"✅ Data source status: {json.dumps(status, indent=2, default=str)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())