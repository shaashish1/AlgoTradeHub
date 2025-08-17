#!/usr/bin/env python3
"""
Market Data Script
Handles market data operations for Next.js API routes
"""

import sys
import json
import argparse
import time
import random

def main():
    parser = argparse.ArgumentParser(description='Market Data Operations')
    parser.add_argument('--symbol', required=True, help='Trading symbol')
    parser.add_argument('--exchange', help='Exchange name')
    
    args = parser.parse_args()
    
    try:
        # Mock market data for demo
        base_prices = {
            'BTC/USDT': 43250.50,
            'ETH/USDT': 2650.75,
            'BNB/USDT': 315.20,
            'ADA/USDT': 0.485,
            'SOL/USDT': 98.45
        }
        
        base_price = base_prices.get(args.symbol, 1000.0)
        
        # Add some random variation
        current_price = base_price * (1 + (random.random() - 0.5) * 0.02)  # ±1% variation
        change_24h = (random.random() - 0.5) * 10  # ±5% change
        volume = random.randint(100000, 2000000)
        
        result = {
            'success': True,
            'symbol': args.symbol,
            'price': round(current_price, 2),
            'change24h': round(change_24h, 2),
            'volume': volume,
            'timestamp': time.time(),
            'exchange': args.exchange or 'binance'
        }
        
        print(json.dumps(result))
        
    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e)
        }
        print(json.dumps(error_result))
        sys.exit(1)

if __name__ == '__main__':
    main()