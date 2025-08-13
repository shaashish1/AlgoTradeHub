#!/usr/bin/env python3
"""
Data Fetcher Module
Handles fetching market data from various exchanges
"""

import ccxt
import ccxt.async_support as ccxt_async
import pandas as pd
import numpy as np
import asyncio
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataFetcher:
    def __init__(self, config: Dict):
        """Initialize data fetcher"""
        self.config = config
        self.exchanges = {}
        self.data_cache = {}
        self.cache_timeout = 60  # Cache timeout in seconds
        
    async def initialize_exchange(self, exchange_name: str) -> Optional[ccxt_async.Exchange]:
        """Initialize a single exchange"""
        try:
            if exchange_name in self.exchanges:
                return self.exchanges[exchange_name]
            
            exchange_config = self.config['exchanges'].get(exchange_name)
            if not exchange_config or not exchange_config.get('active', False):
                return None
            
            # Get exchange class
            exchange_class = getattr(ccxt_async, exchange_name)
            
            # Initialize exchange
            exchange = exchange_class({
                'apiKey': exchange_config.get('api_key', ''),
                'secret': exchange_config.get('secret', ''),
                'password': exchange_config.get('passphrase', ''),
                'sandbox': exchange_config.get('sandbox', True),
                'enableRateLimit': True,
                'timeout': 30000,
                'rateLimit': exchange_config.get('rate_limit', 1000),
            })
            
            # Load markets
            await exchange.load_markets()
            
            self.exchanges[exchange_name] = exchange
            logger.info(f"Initialized exchange: {exchange_name}")
            
            return exchange
            
        except Exception as e:
            logger.error(f"Error initializing exchange {exchange_name}: {e}")
            return None
    
    async def fetch_ohlcv(self, exchange_name: str, symbol: str, 
                         timeframe: str = '1m', limit: int = 100,
                         since: Optional[int] = None) -> Optional[pd.DataFrame]:
        """Fetch OHLCV data for a symbol"""
        try:
            # Check cache first
            cache_key = f"{exchange_name}_{symbol}_{timeframe}_{limit}"
            if cache_key in self.data_cache:
                cached_data, timestamp = self.data_cache[cache_key]
                if (datetime.now() - timestamp).seconds < self.cache_timeout:
                    return cached_data
            
            # Initialize exchange if needed
            exchange = await self.initialize_exchange(exchange_name)
            if not exchange:
                return None
            
            # Fetch OHLCV data
            ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
            
            if not ohlcv:
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            # Cache the result
            self.data_cache[cache_key] = (df, datetime.now())
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching OHLCV data for {symbol} on {exchange_name}: {e}")
            return None
    
    async def fetch_ticker(self, exchange_name: str, symbol: str) -> Optional[Dict]:
        """Fetch ticker data for a symbol"""
        try:
            # Initialize exchange if needed
            exchange = await self.initialize_exchange(exchange_name)
            if not exchange:
                return None
            
            # Fetch ticker
            ticker = await exchange.fetch_ticker(symbol)
            
            return ticker
            
        except Exception as e:
            logger.error(f"Error fetching ticker for {symbol} on {exchange_name}: {e}")
            return None
    
    async def fetch_order_book(self, exchange_name: str, symbol: str, 
                              limit: int = 10) -> Optional[Dict]:
        """Fetch order book data"""
        try:
            # Initialize exchange if needed
            exchange = await self.initialize_exchange(exchange_name)
            if not exchange:
                return None
            
            # Fetch order book
            order_book = await exchange.fetch_order_book(symbol, limit=limit)
            
            return order_book
            
        except Exception as e:
            logger.error(f"Error fetching order book for {symbol} on {exchange_name}: {e}")
            return None
    
    async def fetch_trades(self, exchange_name: str, symbol: str, 
                          limit: int = 100) -> Optional[List[Dict]]:
        """Fetch recent trades"""
        try:
            # Initialize exchange if needed
            exchange = await self.initialize_exchange(exchange_name)
            if not exchange:
                return None
            
            # Fetch trades
            trades = await exchange.fetch_trades(symbol, limit=limit)
            
            return trades
            
        except Exception as e:
            logger.error(f"Error fetching trades for {symbol} on {exchange_name}: {e}")
            return None
    
    async def fetch_historical_data(self, exchange_name: str, symbol: str,
                                   timeframe: str, start_date: str, 
                                   end_date: str) -> Optional[pd.DataFrame]:
        """Fetch historical data for a date range"""
        try:
            # Initialize exchange if needed
            exchange = await self.initialize_exchange(exchange_name)
            if not exchange:
                return None
            
            # Convert dates to timestamps
            start_timestamp = int(pd.Timestamp(start_date).timestamp() * 1000)
            end_timestamp = int(pd.Timestamp(end_date).timestamp() * 1000)
            
            # Fetch data in chunks
            all_data = []
            current_timestamp = start_timestamp
            
            while current_timestamp < end_timestamp:
                try:
                    # Fetch chunk
                    ohlcv = await exchange.fetch_ohlcv(
                        symbol, 
                        timeframe, 
                        since=current_timestamp,
                        limit=1000
                    )
                    
                    if not ohlcv:
                        break
                    
                    all_data.extend(ohlcv)
                    current_timestamp = ohlcv[-1][0] + 1
                    
                    # Respect rate limits
                    await asyncio.sleep(exchange.rateLimit / 1000)
                    
                except Exception as e:
                    logger.error(f"Error fetching data chunk: {e}")
                    break
            
            if not all_data:
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(all_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            # Remove duplicates
            df = df[~df.index.duplicated(keep='first')]
            
            # Sort by timestamp
            df = df.sort_index()
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching historical data: {e}")
            return None
    
    async def get_market_info(self, exchange_name: str, symbol: str) -> Optional[Dict]:
        """Get market information for a symbol"""
        try:
            # Initialize exchange if needed
            exchange = await self.initialize_exchange(exchange_name)
            if not exchange:
                return None
            
            # Get market info
            if symbol in exchange.markets:
                market = exchange.markets[symbol]
                return {
                    'symbol': symbol,
                    'base': market.get('base'),
                    'quote': market.get('quote'),
                    'active': market.get('active'),
                    'type': market.get('type'),
                    'spot': market.get('spot'),
                    'margin': market.get('margin'),
                    'future': market.get('future'),
                    'option': market.get('option'),
                    'contract': market.get('contract'),
                    'settle': market.get('settle'),
                    'precision': market.get('precision'),
                    'limits': market.get('limits'),
                    'fees': market.get('fees'),
                    'info': market.get('info')
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting market info for {symbol} on {exchange_name}: {e}")
            return None
    
    async def fetch_multiple_symbols(self, exchange_name: str, symbols: List[str],
                                   timeframe: str = '1m', limit: int = 100) -> Dict[str, pd.DataFrame]:
        """Fetch data for multiple symbols concurrently"""
        try:
            # Initialize exchange if needed
            exchange = await self.initialize_exchange(exchange_name)
            if not exchange:
                return {}
            
            # Create tasks for all symbols
            tasks = []
            for symbol in symbols:
                task = self.fetch_ohlcv(exchange_name, symbol, timeframe, limit)
                tasks.append(task)
            
            # Execute tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            data = {}
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Error fetching data for {symbols[i]}: {result}")
                    continue
                
                if result is not None:
                    data[symbols[i]] = result
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching multiple symbols: {e}")
            return {}
    
    async def get_active_symbols(self, exchange_name: str) -> List[str]:
        """Get list of active symbols for an exchange"""
        try:
            # Initialize exchange if needed
            exchange = await self.initialize_exchange(exchange_name)
            if not exchange:
                return []
            
            # Get configured symbols
            exchange_config = self.config['exchanges'].get(exchange_name, {})
            symbols = exchange_config.get('symbols', [])
            
            # Validate symbols exist on exchange
            valid_symbols = []
            for symbol in symbols:
                if symbol in exchange.markets:
                    market = exchange.markets[symbol]
                    if market.get('active', False):
                        valid_symbols.append(symbol)
                else:
                    logger.warning(f"Symbol {symbol} not found on {exchange_name}")
            
            return valid_symbols
            
        except Exception as e:
            logger.error(f"Error getting active symbols for {exchange_name}: {e}")
            return []
    
    async def validate_symbol(self, exchange_name: str, symbol: str) -> bool:
        """Validate if a symbol exists and is active on an exchange"""
        try:
            # Initialize exchange if needed
            exchange = await self.initialize_exchange(exchange_name)
            if not exchange:
                return False
            
            # Check if symbol exists and is active
            if symbol in exchange.markets:
                market = exchange.markets[symbol]
                return market.get('active', False)
            
            return False
            
        except Exception as e:
            logger.error(f"Error validating symbol {symbol} on {exchange_name}: {e}")
            return False
    
    def clear_cache(self):
        """Clear data cache"""
        self.data_cache.clear()
        logger.info("Data cache cleared")
    
    async def cleanup(self):
        """Clean up resources"""
        try:
            # Close all exchange connections
            for exchange in self.exchanges.values():
                await exchange.close()
            
            # Clear cache
            self.clear_cache()
            
            logger.info("Data fetcher cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
