#!/usr/bin/env python3
"""
Simple test for Delta Exchange script
"""

import asyncio
import sys
import os

# Add the crypto scripts directory to path
sys.path.append('crypto/scripts')

async def test_delta():
    """Test the Delta Exchange functionality"""
    try:
        from delta_backtest_strategies import DeltaExchangeBacktester
        
        print("🧪 Testing Delta Exchange Backtester...")
        
        backtester = DeltaExchangeBacktester()
        
        # Test connection
        connected = await backtester.initialize_delta_exchange()
        if not connected:
            print("❌ Failed to connect to exchange")
            return
        
        print("✅ Connected successfully!")
        
        # Test fetching pairs
        pairs = await backtester.fetch_available_pairs()
        print(f"📊 Found {len(pairs)} trading pairs")
        
        if pairs:
            print("Sample pairs:")
            for pair in pairs[:5]:
                print(f"  - {pair}")
        
        # Test top volume pairs
        top_pairs = await backtester.get_top_volume_pairs(3)
        print(f"\n🔥 Top 3 volume pairs: {', '.join(top_pairs)}")
        
        # Test backtest simulation
        print("\n🚀 Running sample backtest...")
        strategies = ["rsi_strategy", "macd_strategy"]
        results = await backtester.run_backtest_simulation(top_pairs[:2], strategies)
        
        print(f"✅ Completed {len(results)} backtests")
        
        # Display results
        backtester.display_results_summary(results)
        
        # Cleanup
        if backtester.exchange:
            await backtester.exchange.close()
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(test_delta())