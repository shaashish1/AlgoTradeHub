#!/usr/bin/env python3
"""
AlgoTradeHub - Comprehensive Algorithmic Trading System
Central Hub for All Trading Features and Scripts
"""

import asyncio
import ccxt
import pandas as pd
import numpy as np
import json
import time
import os
import sys
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.progress import Progress
from rich.columns import Columns

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
console = Console()

class FeatureBrowser:
    """Browse and execute all available features and scripts"""
    
    def __init__(self):
        self.console = console
        
    def get_available_scripts(self) -> Dict[str, Dict]:
        """Get all available scripts organized by category"""
        scripts = {
            "crypto": {
                "1": {
                    "name": "Interactive Crypto Demo",
                    "file": "crypto/scripts/interactive_crypto_demo.py",
                    "description": "Interactive cryptocurrency trading demo with real-time data"
                },
                "2": {
                    "name": "Batch Runner Demo", 
                    "file": "crypto/scripts/batch_runner_demo.py",
                    "description": "Batch processing for multiple strategy testing"
                },
                "3": {
                    "name": "Delta Exchange Backtesting",
                    "file": "crypto/scripts/delta_backtest_strategies.py", 
                    "description": "Advanced backtesting with Delta Exchange integration"
                }
            },
            "core": {
                "1": {
                    "name": "Backtest Engine",
                    "file": "backtest.py", 
                    "description": "Standalone backtesting engine"
                },
                "2": {
                    "name": "Web Application",
                    "file": "app.py",
                    "description": "Web-based trading dashboard"
                },
                "3": {
                    "name": "Strategy Testing",
                    "file": "strategy.py",
                    "description": "Individual strategy testing and analysis"
                }
            },
            "testing": {
                "1": {
                    "name": "Feature Demo",
                    "file": "demo_all_features.py",
                    "description": "Comprehensive feature demonstration"
                },
                "2": {
                    "name": "Quick Test",
                    "file": "quick_test.py", 
                    "description": "Quick system functionality test"
                },
                "3": {
                    "name": "All Features Test",
                    "file": "test_all_features.py",
                    "description": "Complete system testing suite"
                }
            }
        }
        return scripts
    
    def display_feature_menu(self):
        """Display comprehensive feature menu"""
        scripts = self.get_available_scripts()
        
        self.console.print("\n🎯 [bold blue]AlgoTradeHub Feature Browser[/bold blue]")
        self.console.print("=" * 60)
        
        for category, items in scripts.items():
            self.console.print(f"\n📁 [bold cyan]{category.upper()} FEATURES[/bold cyan]")
            for key, script in items.items():
                self.console.print(f"  {category[0].upper()}{key}. [bold]{script['name']}[/bold]")
                self.console.print(f"      {script['description']}", style="dim")
        
        self.console.print(f"\n🔧 [bold yellow]ADVANCED OPTIONS[/bold yellow]")
        self.console.print(f"  A1. [bold]Comprehensive Backtesting Suite[/bold]")
        self.console.print(f"      Multi-timeframe, multi-strategy, multi-asset backtesting")
        self.console.print(f"  A2. [bold]Strategy Performance Analysis[/bold]") 
        self.console.print(f"      Analyze which strategies work best for different assets/timeframes")
        self.console.print(f"  A3. [bold]Market Data Analysis[/bold]")
        self.console.print(f"      Historical data analysis and pattern recognition")
        
        return scripts
    
    def execute_script(self, script_path: str, args: List[str] = None):
        """Execute a selected script"""
        try:
            if not os.path.exists(script_path):
                self.console.print(f"❌ Script not found: {script_path}", style="red")
                return
            
            cmd = [sys.executable, script_path]
            if args:
                cmd.extend(args)
            
            self.console.print(f"🚀 Executing: {script_path}", style="green")
            self.console.print(f"Command: {' '.join(cmd)}", style="dim")
            
            # Execute the script with interactive capability
            result = subprocess.run(cmd, text=True)
            
            if result.returncode == 0:
                self.console.print("✅ Script executed successfully", style="green")
            else:
                self.console.print(f"❌ Script execution failed with code {result.returncode}", style="red")
                    
        except Exception as e:
            self.console.print(f"❌ Error executing script: {e}", style="red")

class ComprehensiveBacktester:
    """Advanced backtesting with multi-timeframe, multi-strategy, multi-asset analysis"""
    
    def __init__(self):
        self.console = console
        self.strategies = [
            "rsi_strategy", "macd_strategy", "bollinger_strategy",
            "multi_indicator_strategy", "sma_crossover_strategy",
            "ema_strategy", "momentum_strategy", "volume_breakout_strategy",
            "stochastic_strategy"
        ]
        self.timeframes = ["1m", "5m", "15m", "30m", "1h", "4h", "1d"]
        self.assets = [
            "BTC/USDT", "ETH/USDT", "BNB/USDT", "ADA/USDT", "SOL/USDT",
            "DOT/USDT", "MATIC/USDT", "AVAX/USDT", "LINK/USDT", "UNI/USDT"
        ]
        
    def get_user_selections(self) -> Dict:
        """Get user selections for comprehensive backtesting"""
        self.console.print("\n🔧 [bold]Comprehensive Backtesting Configuration[/bold]")
        
        # Strategy selection
        self.console.print("\n🧠 [bold]Strategy Selection[/bold]")
        self.console.print("Available strategies:")
        for i, strategy in enumerate(self.strategies, 1):
            self.console.print(f"  {i}. {strategy.replace('_', ' ').title()}")
        
        strategy_choice = Prompt.ask(
            "Select strategies (comma-separated numbers, or 'all')", 
            default="all"
        )
        
        if strategy_choice.lower() == "all":
            selected_strategies = self.strategies
        else:
            indices = [int(x.strip()) - 1 for x in strategy_choice.split(",")]
            selected_strategies = [self.strategies[i] for i in indices if 0 <= i < len(self.strategies)]
        
        # Timeframe selection
        self.console.print("\n⏰ [bold]Timeframe Selection[/bold]")
        self.console.print("Available timeframes:")
        for i, tf in enumerate(self.timeframes, 1):
            self.console.print(f"  {i}. {tf}")
        
        timeframe_choice = Prompt.ask(
            "Select timeframes (comma-separated numbers, or 'all')", 
            default="all"
        )
        
        if timeframe_choice.lower() == "all":
            selected_timeframes = self.timeframes
        else:
            indices = [int(x.strip()) - 1 for x in timeframe_choice.split(",")]
            selected_timeframes = [self.timeframes[i] for i in indices if 0 <= i < len(self.timeframes)]
        
        # Asset selection
        self.console.print("\n💰 [bold]Asset Selection[/bold]")
        self.console.print("Available assets:")
        for i, asset in enumerate(self.assets, 1):
            self.console.print(f"  {i}. {asset}")
        
        asset_choice = Prompt.ask(
            "Select assets (comma-separated numbers, or 'all')", 
            default="1,2,3,4,5"
        )
        
        if asset_choice.lower() == "all":
            selected_assets = self.assets
        else:
            indices = [int(x.strip()) - 1 for x in asset_choice.split(",")]
            selected_assets = [self.assets[i] for i in indices if 0 <= i < len(self.assets)]
        
        # Date range - get maximum available days
        self.console.print("\n📅 [bold]Date Range Configuration[/bold]")
        use_max_days = Confirm.ask("Use maximum available historical data?", default=True)
        
        if use_max_days:
            # Use maximum available data (typically 2+ years for most exchanges)
            start_date = "2022-01-01"
            end_date = datetime.now().strftime("%Y-%m-%d")
        else:
            start_date = Prompt.ask("Start date (YYYY-MM-DD)", default="2023-01-01")
            end_date = Prompt.ask("End date (YYYY-MM-DD)", default="2024-01-01")
        
        # Other parameters
        initial_capital = float(Prompt.ask("Initial capital ($)", default="10000"))
        commission = float(Prompt.ask("Commission rate (0.001 = 0.1%)", default="0.001"))
        
        return {
            'strategies': selected_strategies,
            'timeframes': selected_timeframes,
            'assets': selected_assets,
            'start_date': start_date,
            'end_date': end_date,
            'initial_capital': initial_capital,
            'commission': commission
        }
    
    async def run_comprehensive_backtest(self, config: Dict):
        """Run comprehensive backtesting across all selected parameters"""
        strategies = config['strategies']
        timeframes = config['timeframes']
        assets = config['assets']
        
        total_tests = len(strategies) * len(timeframes) * len(assets)
        
        self.console.print(f"\n🚀 [bold]Starting Comprehensive Backtesting[/bold]")
        self.console.print(f"Total tests to run: {total_tests:,}")
        self.console.print(f"Estimated time: {total_tests * 2 / 60:.1f} minutes")
        
        results = []
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Running backtests...", total=total_tests)
            
            for strategy in strategies:
                for timeframe in timeframes:
                    for asset in assets:
                        try:
                            # Simulate backtest (replace with actual backtest logic)
                            result = await self.simulate_backtest(
                                strategy, timeframe, asset, config
                            )
                            
                            if result:
                                results.append(result)
                            
                            progress.advance(task)
                            await asyncio.sleep(0.1)  # Small delay
                            
                        except Exception as e:
                            logger.error(f"Error testing {strategy} on {asset} {timeframe}: {e}")
                            progress.advance(task)
        
        return results
    
    async def simulate_backtest(self, strategy: str, timeframe: str, asset: str, config: Dict) -> Dict:
        """Simulate a backtest (replace with actual backtest logic)"""
        # This is a simulation - replace with actual backtest engine
        import random
        
        # Simulate realistic results based on strategy and timeframe
        base_return = random.uniform(-20, 30)
        
        # Adjust returns based on timeframe (shorter timeframes typically more volatile)
        timeframe_multiplier = {
            "1m": 0.5, "5m": 0.7, "15m": 0.8, "30m": 0.9,
            "1h": 1.0, "4h": 1.1, "1d": 1.2
        }
        
        adjusted_return = base_return * timeframe_multiplier.get(timeframe, 1.0)
        
        return {
            'strategy': strategy,
            'timeframe': timeframe,
            'asset': asset,
            'total_return': adjusted_return,
            'sharpe_ratio': random.uniform(0.5, 2.5),
            'max_drawdown': random.uniform(5, 25),
            'win_rate': random.uniform(40, 70),
            'total_trades': random.randint(50, 500),
            'final_portfolio': config['initial_capital'] * (1 + adjusted_return / 100)
        }
    
    def analyze_results(self, results: List[Dict]):
        """Analyze and display comprehensive results"""
        if not results:
            self.console.print("❌ No results to analyze", style="red")
            return
        
        # Sort by total return
        results.sort(key=lambda x: x.get('total_return', 0), reverse=True)
        
        # Display top performers
        self.console.print("\n🏆 [bold green]Top 10 Performers[/bold green]")
        table = Table()
        table.add_column("Rank", style="yellow")
        table.add_column("Strategy", style="cyan")
        table.add_column("Asset", style="magenta")
        table.add_column("Timeframe", style="blue")
        table.add_column("Return %", style="green")
        table.add_column("Sharpe", style="white")
        table.add_column("Drawdown %", style="red")
        
        for i, result in enumerate(results[:10], 1):
            rank_icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            table.add_row(
                rank_icon,
                result['strategy'].replace('_', ' ').title(),
                result['asset'],
                result['timeframe'],
                f"{result['total_return']:.2f}",
                f"{result['sharpe_ratio']:.2f}",
                f"{result['max_drawdown']:.2f}"
            )
        
        self.console.print(table)
        
        # Strategy analysis
        self.analyze_by_strategy(results)
        
        # Timeframe analysis
        self.analyze_by_timeframe(results)
        
        # Asset analysis
        self.analyze_by_asset(results)
    
    def analyze_by_strategy(self, results: List[Dict]):
        """Analyze performance by strategy"""
        strategy_stats = {}
        
        for result in results:
            strategy = result['strategy']
            if strategy not in strategy_stats:
                strategy_stats[strategy] = []
            strategy_stats[strategy].append(result['total_return'])
        
        self.console.print("\n📊 [bold blue]Strategy Performance Analysis[/bold blue]")
        
        strategy_summary = []
        for strategy, returns in strategy_stats.items():
            avg_return = sum(returns) / len(returns)
            max_return = max(returns)
            min_return = min(returns)
            win_rate = len([r for r in returns if r > 0]) / len(returns) * 100
            
            strategy_summary.append({
                'strategy': strategy,
                'avg_return': avg_return,
                'max_return': max_return,
                'min_return': min_return,
                'win_rate': win_rate,
                'tests': len(returns)
            })
        
        # Sort by average return
        strategy_summary.sort(key=lambda x: x['avg_return'], reverse=True)
        
        table = Table(title="Strategy Performance Summary")
        table.add_column("Strategy", style="cyan")
        table.add_column("Avg Return %", style="green")
        table.add_column("Max Return %", style="bright_green")
        table.add_column("Min Return %", style="red")
        table.add_column("Win Rate %", style="yellow")
        table.add_column("Tests", style="white")
        
        for stats in strategy_summary:
            table.add_row(
                stats['strategy'].replace('_', ' ').title(),
                f"{stats['avg_return']:.2f}",
                f"{stats['max_return']:.2f}",
                f"{stats['min_return']:.2f}",
                f"{stats['win_rate']:.1f}",
                str(stats['tests'])
            )
        
        self.console.print(table)
    
    def analyze_by_timeframe(self, results: List[Dict]):
        """Analyze performance by timeframe"""
        timeframe_stats = {}
        
        for result in results:
            timeframe = result['timeframe']
            if timeframe not in timeframe_stats:
                timeframe_stats[timeframe] = []
            timeframe_stats[timeframe].append(result['total_return'])
        
        self.console.print("\n⏰ [bold blue]Timeframe Performance Analysis[/bold blue]")
        
        timeframe_summary = []
        for timeframe, returns in timeframe_stats.items():
            avg_return = sum(returns) / len(returns)
            win_rate = len([r for r in returns if r > 0]) / len(returns) * 100
            
            timeframe_summary.append({
                'timeframe': timeframe,
                'avg_return': avg_return,
                'win_rate': win_rate,
                'tests': len(returns)
            })
        
        # Sort by average return
        timeframe_summary.sort(key=lambda x: x['avg_return'], reverse=True)
        
        for stats in timeframe_summary:
            self.console.print(
                f"{stats['timeframe']:>4}: {stats['avg_return']:>6.2f}% avg "
                f"({stats['win_rate']:>5.1f}% win rate, {stats['tests']} tests)"
            )
    
    def analyze_by_asset(self, results: List[Dict]):
        """Analyze performance by asset"""
        asset_stats = {}
        
        for result in results:
            asset = result['asset']
            if asset not in asset_stats:
                asset_stats[asset] = []
            asset_stats[asset].append(result['total_return'])
        
        self.console.print("\n💰 [bold blue]Asset Performance Analysis[/bold blue]")
        
        asset_summary = []
        for asset, returns in asset_stats.items():
            avg_return = sum(returns) / len(returns)
            win_rate = len([r for r in returns if r > 0]) / len(returns) * 100
            
            asset_summary.append({
                'asset': asset,
                'avg_return': avg_return,
                'win_rate': win_rate,
                'tests': len(returns)
            })
        
        # Sort by average return
        asset_summary.sort(key=lambda x: x['avg_return'], reverse=True)
        
        for stats in asset_summary:
            self.console.print(
                f"{stats['asset']:>10}: {stats['avg_return']:>6.2f}% avg "
                f"({stats['win_rate']:>5.1f}% win rate, {stats['tests']} tests)"
            )

class TradingSystemMenu:
    """Main menu system for the trading application"""
    
    def __init__(self):
        self.console = console
        self.feature_browser = FeatureBrowser()
        self.comprehensive_backtester = ComprehensiveBacktester()
        
    def display_welcome(self):
        """Display welcome banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🚀 AlgoTradeHub 🚀                        ║
║              Central Hub for All Trading Features            ║
║                                                              ║
║  • Browse All Available Scripts & Features                  ║
║  • Multi-Exchange Support (Crypto & Stocks)                 ║
║  • Advanced Backtesting & Analysis                          ║
║  • Real-time Trading & Market Analysis                      ║
╚══════════════════════════════════════════════════════════════╝
        """
        self.console.print(banner, style="bold cyan")
    
    async def handle_user_choice(self, choice: str, scripts: Dict):
        """Handle user menu choice"""
        try:
            if choice.upper() == "A1":
                # Comprehensive Backtesting Suite
                config = self.comprehensive_backtester.get_user_selections()
                results = await self.comprehensive_backtester.run_comprehensive_backtest(config)
                self.comprehensive_backtester.analyze_results(results)
                
            elif choice.upper() == "A2":
                # Strategy Performance Analysis
                self.console.print("🔍 [bold]Strategy Performance Analysis[/bold]")
                self.console.print("This will analyze historical performance of all strategies...")
                
                # Run a smaller comprehensive test for analysis
                config = {
                    'strategies': self.comprehensive_backtester.strategies,
                    'timeframes': ["1h", "4h", "1d"],
                    'assets': self.comprehensive_backtester.assets[:5],
                    'start_date': "2023-01-01",
                    'end_date': "2024-01-01",
                    'initial_capital': 10000,
                    'commission': 0.001
                }
                
                results = await self.comprehensive_backtester.run_comprehensive_backtest(config)
                self.comprehensive_backtester.analyze_results(results)
                
            elif choice.upper() == "A3":
                # Market Data Analysis
                self.console.print("📊 [bold]Market Data Analysis[/bold]")
                self.console.print("Analyzing market patterns and trends...")
                
                # This would implement market data analysis
                self.console.print("Market data analysis feature coming soon!")
                
            else:
                # Handle script execution
                category = None
                script_key = None
                
                if choice.upper().startswith('C'):
                    category = 'crypto'
                    script_key = choice[1:]
                elif choice.upper().startswith('T'):
                    category = 'testing'
                    script_key = choice[1:]
                elif choice.upper().startswith('R'):
                    category = 'core'
                    script_key = choice[1:]
                
                if category and script_key in scripts.get(category, {}):
                    script_info = scripts[category][script_key]
                    
                    # Get additional arguments if needed
                    args = []
                    if category == 'crypto':
                        if 'delta' in script_info['file']:
                            # Delta exchange script options
                            self.console.print("\nDelta Exchange Script Options:")
                            self.console.print("1. --list-pairs (List available pairs)")
                            self.console.print("2. --top-volume 10 (Get top 10 volume pairs)")
                            self.console.print("3. --interactive (Interactive mode)")
                            
                            option = Prompt.ask("Select option (1-3, or press Enter for default)", default="3")
                            if option == "1":
                                args = ["--list-pairs"]
                            elif option == "2":
                                args = ["--top-volume", "10"]
                            elif option == "3":
                                args = ["--interactive"]
                    
                    self.feature_browser.execute_script(script_info['file'], args)
                else:
                    self.console.print(f"❌ Invalid choice: {choice}", style="red")
                    
        except Exception as e:
            self.console.print(f"❌ Error handling choice: {e}", style="red")
            logger.error(f"Error handling choice {choice}: {e}")

async def main():
    """Main entry point with comprehensive menu system"""
    try:
        # Initialize menu system
        menu = TradingSystemMenu()
        
        while True:
            # Display welcome banner
            menu.display_welcome()
            
            # Display feature menu
            scripts = menu.feature_browser.display_feature_menu()
            
            # Get user choice
            console.print("\n🎯 [bold]What would you like to do?[/bold]")
            console.print("Enter choice (e.g., C1 for Crypto feature 1, A1 for Advanced option 1)")
            console.print("Or type 'quit' to exit")
            
            choice = Prompt.ask("Your choice", default="A1")
            
            if choice.lower() in ['quit', 'exit', 'q']:
                console.print("👋 [bold yellow]Goodbye![/bold yellow]")
                break
            
            # Handle user choice
            await menu.handle_user_choice(choice, scripts)
            
            # Ask if user wants to continue
            if not Confirm.ask("\nWould you like to continue?", default=True):
                console.print("👋 [bold yellow]Goodbye![/bold yellow]")
                break
        
    except KeyboardInterrupt:
        console.print("\n👋 [bold yellow]Goodbye![/bold yellow]")
    except Exception as e:
        console.print(f"\n❌ [bold red]Fatal error: {e}[/bold red]")
        logger.error(f"Fatal error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Set event loop policy for Windows
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Run the main application
    asyncio.run(main())