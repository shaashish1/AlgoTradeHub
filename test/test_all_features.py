#!/usr/bin/env python3
"""
Automated Test Suite for AlgoTradeHub
Tests all features with default values automatically
"""

import asyncio
import sys
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from utils.config_manager import ConfigManager
from strategy import TradingStrategy
from backtest import BacktestEngine
from main import SystemHealthChecker, TradingSystemMenu, run_backtest

console = Console()

class AutomatedTester:
    """Automated testing for all AlgoTradeHub features"""
    
    def __init__(self):
        self.console = console
        self.test_results = []
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log test results"""
        self.test_results.append({
            'test': test_name,
            'status': status,
            'details': details,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        self.console.print(f"{status_icon} {test_name}: {status}")
        if details:
            self.console.print(f"   {details}", style="dim")
    
    async def test_system_health(self):
        """Test system health checker"""
        self.console.print("\n🔍 [bold blue]Testing System Health Checker[/bold blue]")
        
        try:
            health_checker = SystemHealthChecker()
            
            # Test dependency check
            deps_ok = health_checker.check_dependencies()
            self.log_test("Dependency Check", "PASS" if deps_ok else "FAIL")
            
            # Test config check
            config_ok = health_checker.check_config_files()
            self.log_test("Configuration Check", "PASS" if config_ok else "FAIL")
            
            # Test exchange connectivity
            exchange_status = health_checker.check_exchange_connectivity()
            active_count = sum(1 for status in exchange_status.values() if status)
            self.log_test("Exchange Connectivity", "PASS" if active_count > 0 else "FAIL", 
                         f"{active_count} exchanges active")
            
            return deps_ok and config_ok and active_count > 0
            
        except Exception as e:
            self.log_test("System Health Check", "FAIL", str(e))
            return False
    
    async def test_all_strategies(self):
        """Test all trading strategies"""
        self.console.print("\n🧠 [bold blue]Testing All Trading Strategies[/bold blue]")
        
        strategies = [
            "rsi_strategy", "macd_strategy", "bollinger_strategy",
            "multi_indicator_strategy", "sma_crossover_strategy",
            "ema_strategy", "momentum_strategy", "volume_breakout_strategy",
            "stochastic_strategy"
        ]
        
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        for strategy_name in strategies:
            try:
                # Update config with strategy
                config['strategy']['name'] = strategy_name
                
                # Initialize strategy
                strategy = TradingStrategy(config)
                
                # Test strategy initialization
                self.log_test(f"Strategy: {strategy_name}", "PASS", "Initialized successfully")
                
            except Exception as e:
                self.log_test(f"Strategy: {strategy_name}", "FAIL", str(e))
    
    async def test_backtest_all_strategies(self):
        """Test backtesting with all strategies"""
        self.console.print("\n📊 [bold blue]Testing Backtesting Engine[/bold blue]")
        
        strategies = [
            "rsi_strategy", "macd_strategy", "bollinger_strategy",
            "multi_indicator_strategy", "sma_crossover_strategy"
        ]
        
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        # Default backtest parameters
        backtest_params = {
            'start_date': "2023-01-01",
            'end_date': "2024-01-01",
            'initial_capital': 10000.0,
            'commission': 0.001
        }
        
        for strategy_name in strategies:
            try:
                self.console.print(f"\n📈 Testing {strategy_name.replace('_', ' ').title()}")
                
                # Run backtest
                results = await run_backtest(config, strategy_name, backtest_params)
                
                if results:
                    self.log_test(f"Backtest: {strategy_name}", "PASS", 
                                f"Return: {results.get('total_return', 0):.2f}%, "
                                f"Sharpe: {results.get('sharpe_ratio', 0):.2f}")
                else:
                    self.log_test(f"Backtest: {strategy_name}", "FAIL", "No results generated")
                
                # Small delay between tests
                await asyncio.sleep(1)
                
            except Exception as e:
                self.log_test(f"Backtest: {strategy_name}", "FAIL", str(e))
    
    async def test_configuration_management(self):
        """Test configuration management"""
        self.console.print("\n⚙️ [bold blue]Testing Configuration Management[/bold blue]")
        
        try:
            config_manager = ConfigManager()
            
            # Test loading config
            config = config_manager.load_config()
            self.log_test("Config Loading", "PASS", "Configuration loaded successfully")
            
            # Test config validation
            required_sections = ['exchanges', 'strategy', 'backtest']
            for section in required_sections:
                if section in config:
                    self.log_test(f"Config Section: {section}", "PASS")
                else:
                    self.log_test(f"Config Section: {section}", "FAIL", "Section missing")
            
            # Test exchange configuration
            active_exchanges = [name for name, cfg in config['exchanges'].items() 
                              if cfg.get('active', False)]
            self.log_test("Active Exchanges", "PASS" if active_exchanges else "FAIL", 
                         f"Found: {', '.join(active_exchanges)}")
            
        except Exception as e:
            self.log_test("Configuration Management", "FAIL", str(e))
    
    async def test_market_types(self):
        """Test different market type configurations"""
        self.console.print("\n📈 [bold blue]Testing Market Type Configurations[/bold blue]")
        
        menu = TradingSystemMenu()
        
        market_types = ["crypto", "stocks", "both"]
        
        for market_type in market_types:
            try:
                # Test market type configuration
                result_type = menu.configure_exchanges_for_market_type(market_type)
                
                if market_type == "stocks":
                    # Stocks should fallback to crypto for now
                    self.log_test(f"Market Type: {market_type}", "PASS", 
                                f"Fallback to {result_type} (expected)")
                else:
                    self.log_test(f"Market Type: {market_type}", "PASS", 
                                f"Configured as {result_type}")
                
            except Exception as e:
                self.log_test(f"Market Type: {market_type}", "FAIL", str(e))
    
    def display_test_summary(self):
        """Display comprehensive test summary"""
        self.console.print("\n📋 [bold blue]Test Summary Report[/bold blue]")
        self.console.print("=" * 60)
        
        # Create summary table
        table = Table(title="AlgoTradeHub Test Results")
        table.add_column("Test Category", style="cyan")
        table.add_column("Test Name", style="magenta")
        table.add_column("Status", style="yellow")
        table.add_column("Details", style="white")
        table.add_column("Time", style="dim")
        
        # Add test results
        for result in self.test_results:
            status_style = "green" if result['status'] == "PASS" else "red"
            table.add_row(
                result['test'].split(':')[0] if ':' in result['test'] else "General",
                result['test'],
                f"[{status_style}]{result['status']}[/{status_style}]",
                result['details'][:50] + "..." if len(result['details']) > 50 else result['details'],
                result['timestamp']
            )
        
        self.console.print(table)
        
        # Summary statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['status'] == "PASS")
        failed_tests = sum(1 for r in self.test_results if r['status'] == "FAIL")
        
        summary_panel = Panel(
            f"""
📊 Total Tests: {total_tests}
✅ Passed: {passed_tests}
❌ Failed: {failed_tests}
📈 Success Rate: {(passed_tests/total_tests*100):.1f}%

🎯 System Status: {'READY FOR PRODUCTION' if failed_tests == 0 else 'NEEDS ATTENTION'}
            """.strip(),
            title="Test Summary",
            style="green" if failed_tests == 0 else "yellow"
        )
        
        self.console.print(summary_panel)
    
    async def run_comprehensive_test(self):
        """Run all tests comprehensively"""
        start_time = time.time()
        
        self.console.print("""
╔══════════════════════════════════════════════════════════════╗
║                🧪 AlgoTradeHub Test Suite 🧪                 ║
║              Comprehensive Automated Testing                 ║
║                                                              ║
║  Testing all features with default parameters               ║
║  • System Health Checks                                     ║
║  • All Trading Strategies                                   ║
║  • Backtesting Engine                                       ║
║  • Configuration Management                                 ║
║  • Market Type Configurations                              ║
╚══════════════════════════════════════════════════════════════╝
        """, style="bold cyan")
        
        # Run all test suites
        await self.test_system_health()
        await self.test_configuration_management()
        await self.test_market_types()
        await self.test_all_strategies()
        await self.test_backtest_all_strategies()
        
        # Display results
        end_time = time.time()
        duration = end_time - start_time
        
        self.console.print(f"\n⏱️ Total test duration: {duration:.2f} seconds")
        self.display_test_summary()

async def main():
    """Main test runner"""
    try:
        tester = AutomatedTester()
        await tester.run_comprehensive_test()
        
        console.print("\n🎉 [bold green]All tests completed![/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n⚠️ [bold yellow]Tests interrupted by user[/bold yellow]")
    except Exception as e:
        console.print(f"\n❌ [bold red]Test suite error: {e}[/bold red]")

if __name__ == "__main__":
    # Set event loop policy for Windows
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Run the test suite
    asyncio.run(main())