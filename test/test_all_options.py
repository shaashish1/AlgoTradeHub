#!/usr/bin/env python3
"""
Test script to demonstrate all options in main.py
"""

import asyncio
import sys
import os
from rich.console import Console
from rich.prompt import Prompt

console = Console()

async def test_delta_direct():
    """Test Delta Exchange script directly"""
    console.print("🧪 Testing Delta Exchange script directly...")
    
    try:
        # Import and run the Delta Exchange backtester
        sys.path.append('crypto/scripts')
        from delta_backtest_strategies import DeltaExchangeBacktester
        
        backtester = DeltaExchangeBacktester()
        
        # Test connection
        connected = await backtester.initialize_delta_exchange()
        if connected:
            console.print("✅ Delta Exchange connection successful")
            
            # Test fetching pairs
            pairs = await backtester.fetch_available_pairs()
            console.print(f"📊 Found {len(pairs)} pairs")
            
            # Test top volume pairs
            top_pairs = await backtester.get_top_volume_pairs(3)
            console.print(f"🔥 Top pairs: {', '.join(top_pairs)}")
            
            # Test simulation
            strategies = ["rsi_strategy", "macd_strategy"]
            results = await backtester.run_backtest_simulation(top_pairs[:2], strategies)
            console.print(f"✅ Simulation completed: {len(results)} results")
            
            # Display results
            backtester.display_results_summary(results)
            
            # Cleanup
            if backtester.exchange:
                await backtester.exchange.close()
        else:
            console.print("❌ Failed to connect to Delta Exchange")
            
    except Exception as e:
        console.print(f"❌ Delta test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_comprehensive_backtesting():
    """Test the comprehensive backtesting feature"""
    console.print("🧪 Testing Comprehensive Backtesting...")
    
    try:
        from main import ComprehensiveBacktester
        
        backtester = ComprehensiveBacktester()
        
        # Create a simple test configuration
        config = {
            'strategies': ['rsi_strategy', 'macd_strategy'],
            'timeframes': ['1h', '4h'],
            'assets': ['BTC/USDT', 'ETH/USDT'],
            'start_date': '2023-01-01',
            'end_date': '2024-01-01',
            'initial_capital': 10000,
            'commission': 0.001
        }
        
        console.print("🚀 Running comprehensive backtest...")
        results = await backtester.run_comprehensive_backtest(config)
        
        console.print(f"✅ Completed {len(results)} backtests")
        
        # Analyze results
        backtester.analyze_results(results)
        
    except Exception as e:
        console.print(f"❌ Comprehensive backtest failed: {e}")
        import traceback
        traceback.print_exc()

async def test_all_features():
    """Test all main features"""
    console.print("🎯 [bold blue]Testing All AlgoTradeHub Features[/bold blue]")
    console.print("=" * 60)
    
    # Test 1: Delta Exchange
    console.print("\n1️⃣ Testing Delta Exchange Integration...")
    await test_delta_direct()
    
    # Test 2: Comprehensive Backtesting
    console.print("\n2️⃣ Testing Comprehensive Backtesting...")
    await test_comprehensive_backtesting()
    
    # Test 3: Script Execution
    console.print("\n3️⃣ Testing Script Execution...")
    try:
        from main import FeatureBrowser
        browser = FeatureBrowser()
        
        # Test script existence
        scripts = browser.get_available_scripts()
        console.print(f"✅ Found {sum(len(items) for items in scripts.values())} total scripts")
        
        # Test a simple script execution (non-interactive)
        if os.path.exists('quick_test.py'):
            console.print("🚀 Testing quick_test.py execution...")
            import subprocess
            result = subprocess.run([sys.executable, 'quick_test.py'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                console.print("✅ quick_test.py executed successfully")
            else:
                console.print(f"⚠️ quick_test.py returned code {result.returncode}")
        
    except Exception as e:
        console.print(f"❌ Script execution test failed: {e}")
    
    console.print("\n🎉 [bold green]All feature tests completed![/bold green]")

def show_menu():
    """Show interactive menu for testing"""
    console.print("\n🎯 [bold]AlgoTradeHub Test Menu[/bold]")
    console.print("1. Test Delta Exchange (C3)")
    console.print("2. Test Comprehensive Backtesting (A1)")
    console.print("3. Test All Features")
    console.print("4. Exit")
    
    return Prompt.ask("Select test", choices=["1", "2", "3", "4"], default="3")

async def main():
    """Main test function"""
    try:
        while True:
            choice = show_menu()
            
            if choice == "1":
                await test_delta_direct()
            elif choice == "2":
                await test_comprehensive_backtesting()
            elif choice == "3":
                await test_all_features()
            elif choice == "4":
                console.print("👋 Goodbye!")
                break
            
            if not Prompt.ask("\nRun another test?", default=True):
                break
                
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!")
    except Exception as e:
        console.print(f"❌ Test error: {e}")

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(main())