#!/usr/bin/env python3
"""
Exchange Operations Script
Handles exchange-related operations for Next.js API routes
"""

import sys
import json
import argparse
from exchange_manager import ExchangeManager
from crypto_execution_engine import CryptoExecutionEngine

def main():
    parser = argparse.ArgumentParser(description='Exchange Operations')
    parser.add_argument('--operation', required=True, help='Operation to perform')
    parser.add_argument('--exchange', required=True, help='Exchange name')
    parser.add_argument('--params', default='{}', help='Operation parameters as JSON')
    
    args = parser.parse_args()
    
    try:
        params = json.loads(args.params)
        result = {}
        
        if args.operation == 'test_connection':
            # Test exchange connection
            manager = ExchangeManager()
            success = manager.test_exchange_connection(args.exchange, params)
            result = {
                'success': success,
                'exchange': args.exchange,
                'message': f'Connection {"successful" if success else "failed"}'
            }
            
        elif args.operation == 'get_balance':
            # Get account balance
            engine = CryptoExecutionEngine()
            init_result = engine.initialize_exchanges([args.exchange], sandbox=True)
            
            if init_result.get(args.exchange):
                balance = engine.get_account_balance(args.exchange)
                result = {
                    'success': True,
                    'balance': balance
                }
            else:
                result = {
                    'success': False,
                    'error': f'Failed to initialize {args.exchange}'
                }
                
        elif args.operation == 'get_markets':
            # Get available markets
            manager = ExchangeManager()
            markets = manager.get_exchange_markets(args.exchange)
            result = {
                'success': True,
                'markets': markets
            }
            
        elif args.operation == 'get_status':
            # Get exchange status
            manager = ExchangeManager()
            status = manager.get_exchange_status(args.exchange)
            result = {
                'success': True,
                'status': status
            }
            
        else:
            result = {
                'success': False,
                'error': f'Unknown operation: {args.operation}'
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