#!/usr/bin/env python3
"""
Quick Test - Run main.py with automated responses
"""

import asyncio
import sys
from rich.console import Console

# Import the main components
from main import SystemHealthChecker, TradingSystemMenu, run_backtest

console = Console()

async def quick_test():
    """Quick automated test of main functionality"""
    
    console.print("🚀 [bold cyan]Quick AlgoTradeHub Test[/bold cyan]")
    console.print("Testing with default parameters...")
    
    # 1. System Health Check
    console.print("\n1️⃣ System Health Check")
    health_checker = SystemHealthChecker()
    system_ok = health_checker.display_system_status()
    
    if not system_ok:
        console.print("❌ System not ready")
        return
    
    # 2. Initialize Menu System
    console.print("\n2️⃣ Initializing Menu System")
    menu = TradingSystemMenu()
    
    # 3. Configure for Crypto Markets
    console.print("\n3️⃣ Configuring for Crypto Markets")
    market_type = menu.configure_exchanges_for_market_type("crypto")
    console.print(f"✅ Market type configured: {market_type}")
    
    # 4. Test Backtest with RSI Strategy
    console.print("\n4️⃣ Testing Backtest with RSI Strategy")
    strategy_name = "rsi_strategy"
    backtest_params = {
        'start_date': "2023-01-01",
        'end_date': "2024-01-01", 
        'initial_capital': 10000.0,
        'commission': 0.001
    }
    
    console.print(f"📊 Strategy: {strategy_name}")
    console.print(f"📅 Period: {backtest_params['start_date']} to {backtest_params['end_date']}")
    console.print(f"💰 Capital: ${backtest_params['initial_capital']:,.2f}")
    
    # Run backtest
    results = await run_backtest(menu.config, strategy_name, backtest_params)
    
    if results:
        console.print("\n✅ [bold green]Backtest Successful![/bold green]")
        console.print(f"📈 Total Return: {results.get('total_return', 0):.2f}%")
        console.print(f"📊 Sharpe Ratio: {results.get('sharpe_ratio', 0):.2f}")
        console.print(f"📉 Max Drawdown: {results.get('max_drawdown', 0):.2f}%")
        console.print(f"🎯 Win Rate: {results.get('win_rate', 0):.2f}%")
        console.print(f"💰 Final Portfolio: ${results.get('final_portfolio', 0):,.2f}")
    else:
        console.print("❌ Backtest failed")
    
    console.print("\n🎉 [bold green]Quick test completed![/bold green]")
    console.print("System is ready for full operation!")

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(quick_test())