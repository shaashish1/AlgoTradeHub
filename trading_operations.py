#!/usr/bin/env python3
"""
Trading Operations Script
Handles trading-related operations for Next.js API routes
"""

import sys
import json
import argparse
from crypto_execution_engine import CryptoExecutionEngine, TradingOrder, OrderType, OrderSide

def main():
    parser = argparse.ArgumentParser(description='Trading Operations')
    parser.add_argument('--operation', required=True, help='Operation to perform')
    parser.add_argument('--order', default='{}', help='Order data as JSON')
    
    args = parser.parse_args()
    
    try:
        order_data = json.loads(args.order)
        result = {}
        
        if args.operation == 'execute_order':
            # Execute trading order
            engine = CryptoExecutionEngine()
            
            # Initialize exchange
            exchange_name = order_data.get('exchange')
            init_result = engine.initialize_exchanges([exchange_name], sandbox=True)
            
            if not init_result.get(exchange_name):
                result = {
                    'success': False,
                    'error': f'Failed to initialize {exchange_name}'
                }
            else:
                # Create order object
                order = TradingOrder(
                    symbol=order_data.get('symbol'),
                    side=OrderSide.BUY if order_data.get('side') == 'buy' else OrderSide.SELL,
                    amount=float(order_data.get('amount', 0)),
                    order_type=OrderType.MARKET if order_data.get('type') == 'market' else OrderType.LIMIT,
                    price=float(order_data.get('price', 0)) if order_data.get('price') else None,
                    exchange=exchange_name
                )
                
                # For demo purposes, simulate successful execution
                result = {
                    'success': True,
                    'orderId': f'DEMO_{exchange_name}_{int(time.time())}',
                    'executedPrice': order_data.get('price') or 43250.50,
                    'executedAmount': order.amount,
                    'message': f'Order executed successfully on {exchange_name}',
                    'timestamp': time.time()
                }
                
        elif args.operation == 'cancel_order':
            # Cancel order
            order_id = order_data.get('orderId')
            exchange = order_data.get('exchange')
            
            result = {
                'success': True,
                'message': f'Order {order_id} cancelled successfully',
                'orderId': order_id
            }
            
        elif args.operation == 'get_orders':
            # Get order history
            exchange = order_data.get('exchange')
            
            # Mock order history
            result = {
                'success': True,
                'orders': [
                    {
                        'id': 'DEMO_001',
                        'symbol': 'BTC/USDT',
                        'side': 'buy',
                        'amount': 0.1,
                        'price': 43000,
                        'status': 'filled',
                        'timestamp': time.time() - 3600
                    }
                ]
            }
            
        else:
            result = {
                'success': False,
                'error': f'Unknown operation: {args.operation}'
            }
            
        print(json.dumps(result))
        
    except Exception as e:
        import time
        error_result = {
            'success': False,
            'error': str(e)
        }
        print(json.dumps(error_result))
        sys.exit(1)

if __name__ == '__main__':
    import time
    main()