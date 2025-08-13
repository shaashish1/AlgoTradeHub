#!/usr/bin/env python3
"""
Comprehensive Batch Runner Demo with Parallel Processing
Runs multiple strategies across multiple exchanges simultaneously
"""

import asyncio
import concurrent.futures
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, TaskID
from rich.live import Live
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.config_manager import ConfigManager
from strategy import TradingStrategy
from backtest import BacktestEngine

console = Console()

class ParallelBatchRunner:
    """Advanced parallel batch runner for comprehensive strategy testing"""
    
    def __init__(self):
        self.console = console
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        self.results = []
        
    def get_test_configurations(self) -> List[Dict]:
        """Generate comprehensive test configurations"""
        strategies = [
            "rsi_strategy", "macd_strategy", "bollinger_strategy",
            "multi_indicator_strategy", "sma_crossover_strategy",
            "ema_strategy", "momentum_strategy", "volume_breakout_strategy",
            "stochastic_strategy"
        ]
        
        # Different time periods for testing
        time_periods = [
            ("2023-01-01", "2023-06-30", "6M"),
            ("2023-07-01", "2023-12-31", "6M"),
            ("2023-01-01", "2023-12-31", "1Y"),
            ("2022-01-01", "2023-12-31", "2Y")
        ]
        
        # Different capital amounts
        capital_amounts = [5000, 10000, 25000, 50000]
        
        configurations = []
        
        for strategy in strategies:
            for start_date, end_date, period_name in time_periods:
                for capital in capital_amounts:
                    config = {
                        'strategy': strategy,
                        'start_date': start_date,
                        'end_date': end_date,
                        'period_name': period_name,
                        'initial_capital': capital,
                        'commission': 0.001,
                        'test_id': f"{strategy}_{period_name}_{capital}"
                    }
                    configurations.append(config)
        
        return configurations
    
    async def run_single_backtest(self, test_config: Dict) -> Dict:
        """Run a single backtest configuration"""
        try:
            # Update main config
            config = self.config.copy()
            config['strategy']['name'] = test_config['strategy']
            config['backtest'] = {
                'start_date': test_config['start_date'],
                'end_date': test_config['end_date'],
                'initial_capital': test_config['initial_capital'],
                'commission': test_config['commission']
            }
            
            # Run backtest
            backtest_engine = BacktestEngine(config)
            results = await backtest_engine.run_backtest()
            
            if results:
                return {
                    'test_id': test_config['test_id'],
                    'strategy': test_config['strategy'],
                    'period': test_config['period_name'],
                    'capital': test_config['initial_capital'],
                    'total_return': results.get('total_return', 0),
                    'sharpe_ratio': results.get('sharpe_ratio', 0),
                    'max_drawdown': results.get('max_drawdown', 0),
                    'win_rate': results.get('win_rate', 0),
                    'total_trades': results.get('total_trades', 0),
                    'final_portfolio': results.get('final_portfolio', 0),
                    'status': 'SUCCESS'
                }
            else:
                return {
                    'test_id': test_config['test_id'],
                    'strategy': test_config['strategy'],
                    'period': test_config['period_name'],
                    'capital': test_config['initial_capital'],
                    'status': 'FAILED'
                }
                
        except Exception as e:
            return {
                'test_id': test_config['test_id'],
                'strategy': test_config['strategy'],
                'period': test_config['period_name'],
                'capital': test_config['initial_capital'],
                'error': str(e),
                'status': 'ERROR'
            }
    
    async def run_parallel_backtests(self, max_workers: int = 4):
        """Run backtests in parallel with progress tracking"""
        configurations = self.get_test_configurations()
        
        self.console.print(f"""
╔══════════════════════════════════════════════════════════════╗
║            🚀 Parallel Batch Runner Demo 🚀                  ║
║                                                              ║
║  Running comprehensive strategy analysis:                   ║
║  • {len(set(c['strategy'] for c in configurations))} Different Strategies                                ║
║  • {len(set(c['period_name'] for c in configurations))} Time Periods                                      ║
║  • {len(set(c['capital'] for c in configurations))} Capital Amounts                                     ║
║  • {len(configurations)} Total Test Combinations                           ║
║  • {max_workers} Parallel Workers                                      ║
╚══════════════════════════════════════════════════════════════╝
        """, style="bold cyan")
        
        start_time = time.time()
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Running backtests...", total=len(configurations))
            
            # Run tests in batches to avoid overwhelming the system
            batch_size = max_workers * 2
            all_results = []
            
            for i in range(0, len(configurations), batch_size):
                batch = configurations[i:i + batch_size]
                
                # Run batch in parallel
                tasks = [self.run_single_backtest(config) for config in batch]
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Process results
                for result in batch_results:
                    if isinstance(result, Exception):
                        self.console.print(f"❌ Error: {result}", style="red")
                    else:
                        all_results.append(result)
                        progress.advance(task)
                
                # Small delay between batches
                await asyncio.sleep(0.5)
        
        end_time = time.time()
        duration = end_time - start_time
        
        self.results = all_results
        
        self.console.print(f"\n⏱️ Completed {len(all_results)} tests in {duration:.2f} seconds")
        self.console.print(f"📊 Average time per test: {duration/len(all_results):.2f} seconds")
        
        return all_results
    
    def analyze_results(self):
        """Comprehensive analysis of all results"""
        if not self.results:
            self.console.print("❌ No results to analyze", style="red")
            return
        
        successful_results = [r for r in self.results if r.get('status') == 'SUCCESS']
        
        if not successful_results:
            self.console.print("❌ No successful results to analyze", style="red")
            return
        
        # Strategy Performance Analysis
        self.console.print("\n📊 [bold blue]Strategy Performance Analysis[/bold blue]")
        
        strategy_stats = {}
        for result in successful_results:
            strategy = result['strategy']
            if strategy not in strategy_stats:
                strategy_stats[strategy] = {
                    'returns': [],
                    'sharpe_ratios': [],
                    'drawdowns': [],
                    'win_rates': [],
                    'total_tests': 0
                }
            
            strategy_stats[strategy]['returns'].append(result.get('total_return', 0))
            strategy_stats[strategy]['sharpe_ratios'].append(result.get('sharpe_ratio', 0))
            strategy_stats[strategy]['drawdowns'].append(result.get('max_drawdown', 0))
            strategy_stats[strategy]['win_rates'].append(result.get('win_rate', 0))
            strategy_stats[strategy]['total_tests'] += 1
        
        # Create strategy comparison table
        strategy_table = Table(title="Strategy Performance Summary")
        strategy_table.add_column("Strategy", style="cyan")
        strategy_table.add_column("Avg Return", style="green")
        strategy_table.add_column("Avg Sharpe", style="yellow")
        strategy_table.add_column("Avg Drawdown", style="red")
        strategy_table.add_column("Avg Win Rate", style="blue")
        strategy_table.add_column("Tests", style="magenta")
        strategy_table.add_column("Consistency", style="white")
        
        for strategy, stats in strategy_stats.items():
            avg_return = sum(stats['returns']) / len(stats['returns'])
            avg_sharpe = sum(stats['sharpe_ratios']) / len(stats['sharpe_ratios'])
            avg_drawdown = sum(stats['drawdowns']) / len(stats['drawdowns'])
            avg_win_rate = sum(stats['win_rates']) / len(stats['win_rates'])
            
            # Calculate consistency (lower std dev = more consistent)
            return_std = pd.Series(stats['returns']).std()
            consistency = "High" if return_std < 5 else "Medium" if return_std < 10 else "Low"
            
            strategy_table.add_row(
                strategy.replace('_', ' ').title(),
                f"{avg_return:.2f}%",
                f"{avg_sharpe:.2f}",
                f"{avg_drawdown:.2f}%",
                f"{avg_win_rate:.1f}%",
                str(stats['total_tests']),
                consistency
            )
        
        self.console.print(strategy_table)
        
        # Best performers
        best_return = max(successful_results, key=lambda x: x.get('total_return', 0))
        best_sharpe = max(successful_results, key=lambda x: x.get('sharpe_ratio', 0))
        best_win_rate = max(successful_results, key=lambda x: x.get('win_rate', 0))
        
        self.console.print(f"\n🏆 [bold green]Top Performers[/bold green]")
        self.console.print(f"📈 Best Return: {best_return['strategy'].replace('_', ' ').title()} ({best_return.get('total_return', 0):.2f}%)")
        self.console.print(f"📊 Best Sharpe: {best_sharpe['strategy'].replace('_', ' ').title()} ({best_sharpe.get('sharpe_ratio', 0):.2f})")
        self.console.print(f"🎯 Best Win Rate: {best_win_rate['strategy'].replace('_', ' ').title()} ({best_win_rate.get('win_rate', 0):.1f}%)")
        
        # Capital efficiency analysis
        self.console.print(f"\n💰 [bold blue]Capital Efficiency Analysis[/bold blue]")
        
        capital_performance = {}
        for result in successful_results:
            capital = result['capital']
            if capital not in capital_performance:
                capital_performance[capital] = []
            capital_performance[capital].append(result.get('total_return', 0))
        
        for capital, returns in capital_performance.items():
            avg_return = sum(returns) / len(returns)
            self.console.print(f"${capital:,}: {avg_return:.2f}% average return ({len(returns)} tests)")

async def main():
    """Main execution function"""
    try:
        runner = ParallelBatchRunner()
        
        # Run parallel backtests
        results = await runner.run_parallel_backtests(max_workers=4)
        
        # Analyze results
        runner.analyze_results()
        
        console.print("\n🎉 [bold green]Comprehensive analysis completed![/bold green]")
        console.print("All strategies tested across multiple time periods and capital amounts.")
        
    except KeyboardInterrupt:
        console.print("\n⚠️ [bold yellow]Analysis interrupted by user[/bold yellow]")
    except Exception as e:
        console.print(f"\n❌ [bold red]Error: {e}[/bold red]")

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(main())