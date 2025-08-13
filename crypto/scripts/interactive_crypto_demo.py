#!/usr/bin/env python3
"""
Interactive Crypto Demo with Live Strategy Selection
Real-time strategy testing with user interaction
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.config_manager import ConfigManager
from strategy import TradingStrategy
from backtest import BacktestEngine
from main import SystemHealthChecker

console = Console()

class InteractiveCryptoDemo:
    """Interactive demo for crypto trading strategies"""
    
    def __init__(self):
        self.console = console
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        self.results_history = []
        
    def display_welcome(self):
        """Display interactive welcome screen"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║              🚀 Interactive Crypto Demo 🚀                   ║
║                                                              ║
║  Real-time strategy testing with live interaction           ║
║  • Choose your strategies dynamically                       ║
║  • Compare results in real-time                             ║
║  • Adjust parameters on the fly                             ║
║  • See live performance metrics                             ║
╚══════════════════════════════════════════════════════════════╝
        """
        self.console.print(banner, style="bold cyan")
    
    def get_crypto_pairs(self) -> List[str]:
        """Get available crypto trading pairs"""
        return [
            "BTC/USDT", "ETH/USDT", "BNB/USDT", "ADA/USDT", "SOL/USDT",
            "DOT/USDT", "MATIC/USDT", "AVAX/USDT", "LINK/USDT", "UNI/USDT"
        ]
    
    def get_strategy_menu(self) -> Dict:
        """Get interactive strategy selection menu"""
        strategies = {
            "1": ("rsi_strategy", "RSI Strategy", "🔴 Oversold/Overbought signals"),
            "2": ("macd_strategy", "MACD Strategy", "📈 Trend following with MACD"),
            "3": ("bollinger_strategy", "Bollinger Bands", "📊 Mean reversion strategy"),
            "4": ("multi_indicator_strategy", "Multi-Indicator", "🎯 Combined signal approach"),
            "5": ("sma_crossover_strategy", "SMA Crossover", "↗️ Moving average crossover"),
            "6": ("ema_strategy", "EMA Strategy", "📉 Exponential moving average"),
            "7": ("momentum_strategy", "Momentum Strategy", "🚀 Momentum-based trading"),
            "8": ("volume_breakout_strategy", "Volume Breakout", "📊 Volume-based breakouts"),
            "9": ("stochastic_strategy", "Stochastic Strategy", "🔄 Stochastic oscillator"),
            "10": ("custom", "Custom Strategy", "⚙️ Build your own strategy")
        }
        return strategies
    
    def select_strategies(self) -> List[str]:
        """Interactive strategy selection"""
        self.console.print("\n🧠 [bold]Strategy Selection[/bold]")
        strategies = self.get_strategy_menu()
        
        for key, (_, name, description) in strategies.items():
            self.console.print(f"  {key}. [bold]{name}[/bold]")
            self.console.print(f"     {description}", style="dim")
        
        selected_strategies = []
        
        while True:
            choice = Prompt.ask(
                "\nSelect strategy (or 'done' to finish)", 
                choices=list(strategies.keys()) + ["done"],
                default="done"
            )
            
            if choice == "done":
                break
            elif choice == "10":  # Custom strategy
                self.console.print("🔧 Custom strategy builder coming soon!", style="yellow")
                continue
            else:
                strategy_name = strategies[choice][0]
                if strategy_name not in selected_strategies:
                    selected_strategies.append(strategy_name)
                    self.console.print(f"✅ Added {strategies[choice][1]}", style="green")
                else:
                    self.console.print(f"⚠️ {strategies[choice][1]} already selected", style="yellow")
        
        return selected_strategies
    
    def get_test_parameters(self) -> Dict:
        """Get interactive test parameters"""
        self.console.print("\n⚙️ [bold]Test Configuration[/bold]")
        
        # Time period selection
        periods = {
            "1": ("2024-01-01", "2024-12-31", "2024 Full Year"),
            "2": ("2023-07-01", "2023-12-31", "2023 H2"),
            "3": ("2023-01-01", "2023-12-31", "2023 Full Year"),
            "4": ("2022-01-01", "2023-12-31", "2022-2023 (2 Years)"),
            "5": ("custom", "custom", "Custom Date Range")
        }
        
        self.console.print("\n📅 Select time period:")
        for key, (_, _, description) in periods.items():
            self.console.print(f"  {key}. {description}")
        
        period_choice = Prompt.ask("Choose period", choices=list(periods.keys()), default="1")
        
        if period_choice == "5":
            start_date = Prompt.ask("Start date (YYYY-MM-DD)", default="2023-01-01")
            end_date = Prompt.ask("End date (YYYY-MM-DD)", default="2024-01-01")
        else:
            start_date, end_date, _ = periods[period_choice]
        
        # Capital amount
        capital_options = {
            "1": 5000,
            "2": 10000,
            "3": 25000,
            "4": 50000,
            "5": "custom"
        }
        
        self.console.print("\n💰 Select initial capital:")
        for key, amount in capital_options.items():
            if amount == "custom":
                self.console.print(f"  {key}. Custom amount")
            else:
                self.console.print(f"  {key}. ${amount:,}")
        
        capital_choice = Prompt.ask("Choose capital", choices=list(capital_options.keys()), default="2")
        
        if capital_choice == "5":
            initial_capital = float(Prompt.ask("Enter capital amount", default="10000"))
        else:
            initial_capital = capital_options[capital_choice]
        
        # Commission rate
        commission = float(Prompt.ask("Commission rate (0.001 = 0.1%)", default="0.001"))
        
        return {
            'start_date': start_date,
            'end_date': end_date,
            'initial_capital': initial_capital,
            'commission': commission
        }
    
    async def run_strategy_comparison(self, strategies: List[str], parameters: Dict):
        """Run and compare multiple strategies"""
        self.console.print(f"\n🚀 [bold]Running {len(strategies)} strategies...[/bold]")
        
        results = []
        
        for i, strategy_name in enumerate(strategies, 1):
            self.console.print(f"\n📊 Testing {strategy_name.replace('_', ' ').title()} ({i}/{len(strategies)})")
            
            try:
                # Update config
                config = self.config.copy()
                config['strategy']['name'] = strategy_name
                config['backtest'] = parameters
                
                # Run backtest
                backtest_engine = BacktestEngine(config)
                result = await backtest_engine.run_backtest()
                
                if result:
                    result['strategy_name'] = strategy_name
                    results.append(result)
                    
                    # Show immediate results
                    self.console.print(f"  ✅ Return: {result.get('total_return', 0):.2f}%", style="green")
                    self.console.print(f"  📊 Sharpe: {result.get('sharpe_ratio', 0):.2f}", style="blue")
                else:
                    self.console.print(f"  ❌ Failed to get results", style="red")
                
                # Small delay for better UX
                await asyncio.sleep(1)
                
            except Exception as e:
                self.console.print(f"  ❌ Error: {e}", style="red")
        
        return results
    
    def display_comparison_results(self, results: List[Dict]):
        """Display comprehensive comparison results"""
        if not results:
            self.console.print("❌ No results to display", style="red")
            return
        
        # Sort by total return
        results.sort(key=lambda x: x.get('total_return', 0), reverse=True)
        
        # Create comparison table
        table = Table(title="🏆 Strategy Performance Comparison")
        table.add_column("Rank", style="yellow")
        table.add_column("Strategy", style="cyan")
        table.add_column("Total Return", style="green")
        table.add_column("Sharpe Ratio", style="blue")
        table.add_column("Max Drawdown", style="red")
        table.add_column("Win Rate", style="magenta")
        table.add_column("Total Trades", style="white")
        
        for i, result in enumerate(results, 1):
            rank_style = "bold green" if i == 1 else "bold yellow" if i == 2 else "bold orange1" if i == 3 else "white"
            rank_icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            
            table.add_row(
                f"[{rank_style}]{rank_icon}[/{rank_style}]",
                result['strategy_name'].replace('_', ' ').title(),
                f"{result.get('total_return', 0):.2f}%",
                f"{result.get('sharpe_ratio', 0):.2f}",
                f"{result.get('max_drawdown', 0):.2f}%",
                f"{result.get('win_rate', 0):.1f}%",
                str(result.get('total_trades', 0))
            )
        
        self.console.print(table)
        
        # Winner announcement
        if results:
            winner = results[0]
            self.console.print(f"\n🎉 [bold green]Winner: {winner['strategy_name'].replace('_', ' ').title()}![/bold green]")
            self.console.print(f"📈 Best return: {winner.get('total_return', 0):.2f}%")
            self.console.print(f"💰 Final portfolio: ${winner.get('final_portfolio', 0):,.2f}")
    
    def save_results(self, results: List[Dict]):
        """Save results to history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.results_history.append({
            'timestamp': timestamp,
            'results': results
        })
    
    async def interactive_session(self):
        """Main interactive session"""
        while True:
            # System health check
            health_checker = SystemHealthChecker()
            if not health_checker.display_system_status():
                self.console.print("❌ System not ready", style="red")
                return
            
            # Strategy selection
            strategies = self.select_strategies()
            if not strategies:
                self.console.print("⚠️ No strategies selected", style="yellow")
                continue
            
            # Parameter configuration
            parameters = self.get_test_parameters()
            
            # Confirmation
            self.console.print(f"\n📋 [bold]Test Summary[/bold]")
            self.console.print(f"Strategies: {len(strategies)}")
            self.console.print(f"Period: {parameters['start_date']} to {parameters['end_date']}")
            self.console.print(f"Capital: ${parameters['initial_capital']:,}")
            
            if not Confirm.ask("Proceed with test?", default=True):
                continue
            
            # Run comparison
            results = await self.run_strategy_comparison(strategies, parameters)
            
            # Display results
            self.display_comparison_results(results)
            
            # Save results
            self.save_results(results)
            
            # Continue or exit
            if not Confirm.ask("\nRun another test?", default=True):
                break
        
        # Show session summary
        if self.results_history:
            self.console.print(f"\n📊 [bold]Session Summary[/bold]")
            self.console.print(f"Total tests run: {len(self.results_history)}")
            self.console.print("Thanks for using Interactive Crypto Demo! 🚀")

async def main():
    """Main execution function"""
    try:
        demo = InteractiveCryptoDemo()
        demo.display_welcome()
        
        await demo.interactive_session()
        
    except KeyboardInterrupt:
        console.print("\n👋 [bold yellow]Demo ended by user[/bold yellow]")
    except Exception as e:
        console.print(f"\n❌ [bold red]Error: {e}[/bold red]")

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(main())