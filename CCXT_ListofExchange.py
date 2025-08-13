#!/usr/bin/env python3
"""
CCXT Exchange Listing Utility
This utility provides a dynamic list of all exchanges supported by CCXT
"""

import ccxt
import json
import yaml
from typing import Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

console = Console()

class ExchangeListManager:
    def __init__(self):
        """Initialize the exchange list manager"""
        self.exchanges = {}
        self.supported_exchanges = []
        
    def get_all_exchanges(self) -> List[str]:
        """Get list of all supported exchanges"""
        try:
            # Get all available exchanges
            all_exchanges = ccxt.exchanges
            
            # Filter out exchanges that are known to have issues
            problematic_exchanges = ['coinmate', 'southxchange', 'vaultoro']
            
            supported = []
            for exchange_name in all_exchanges:
                if exchange_name not in problematic_exchanges:
                    supported.append(exchange_name)
            
            self.supported_exchanges = sorted(supported)
            console.print(f"✅ Found {len(self.supported_exchanges)} supported exchanges", style="green")
            
            return self.supported_exchanges
            
        except Exception as e:
            logger.error(f"Error getting exchanges: {e}")
            console.print(f"❌ Error getting exchanges: {e}", style="red")
            return []
    
    def get_exchange_info(self, exchange_name: str) -> Dict:
        """Get detailed information about an exchange"""
        try:
            # Get exchange class
            exchange_class = getattr(ccxt, exchange_name)
            
            # Create temporary instance to get info
            exchange = exchange_class()
            
            info = {
                'id': exchange.id,
                'name': exchange.name,
                'countries': getattr(exchange, 'countries', []),
                'urls': getattr(exchange, 'urls', {}),
                'has': getattr(exchange, 'has', {}),
                'rateLimit': getattr(exchange, 'rateLimit', 0),
                'certified': getattr(exchange, 'certified', False),
                'pro': getattr(exchange, 'pro', False),
                'sandbox': getattr(exchange, 'sandbox', False),
                'api': getattr(exchange, 'api', {}),
                'fees': getattr(exchange, 'fees', {}),
                'requiredCredentials': getattr(exchange, 'requiredCredentials', {})
            }
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting exchange info for {exchange_name}: {e}")
            return {}
    
    def display_exchanges_table(self):
        """Display all exchanges in a formatted table"""
        try:
            console.print("🏦 CCXT Supported Exchanges", style="bold blue")
            
            # Create table
            table = Table(title="Supported Cryptocurrency Exchanges", show_header=True, header_style="bold cyan")
            table.add_column("Exchange ID", style="white", width=20)
            table.add_column("Name", style="green", width=25)
            table.add_column("Countries", style="yellow", width=15)
            table.add_column("Certified", style="blue", width=10)
            table.add_column("Pro", style="magenta", width=8)
            table.add_column("Rate Limit", style="red", width=12)
            
            # Get all exchanges
            exchanges = self.get_all_exchanges()
            
            # Add exchanges to table
            for exchange_name in exchanges:
                try:
                    info = self.get_exchange_info(exchange_name)
                    
                    if info:
                        countries = ', '.join(info.get('countries', []))[:12] + '...' if len(', '.join(info.get('countries', []))) > 12 else ', '.join(info.get('countries', []))
                        certified = "✅" if info.get('certified', False) else "❌"
                        pro = "✅" if info.get('pro', False) else "❌"
                        rate_limit = f"{info.get('rateLimit', 0)}ms"
                        
                        table.add_row(
                            exchange_name,
                            info.get('name', exchange_name),
                            countries,
                            certified,
                            pro,
                            rate_limit
                        )
                
                except Exception as e:
                    logger.error(f"Error processing {exchange_name}: {e}")
                    continue
            
            console.print(table)
            
        except Exception as e:
            logger.error(f"Error displaying exchanges table: {e}")
            console.print(f"❌ Error displaying exchanges: {e}", style="red")
    
    def create_config_template(self, selected_exchanges: List[str] = None) -> Dict:
        """Create a configuration template for selected exchanges"""
        try:
            if selected_exchanges is None:
                # Use popular exchanges as default
                selected_exchanges = [
                    'binance', 'kraken', 'bybit', 'bitget', 'cex', 'deribit',
                    'okx', 'poloniex', 'wazirx', 'bitbns'
                ]
            
            config = {
                'exchanges': {},
                'backtest': {
                    'start_date': '2023-01-01',
                    'end_date': '2024-01-01',
                    'initial_capital': 10000,
                    'commission': 0.001
                },
                'strategy': {
                    'name': 'sample_strategy',
                    'parameters': {
                        'rsi_period': 14,
                        'rsi_overbought': 70,
                        'rsi_oversold': 30
                    }
                },
                'live_trading': False,
                'scan_interval': 5
            }
            
            # Add exchange configurations
            for exchange_name in selected_exchanges:
                try:
                    info = self.get_exchange_info(exchange_name)
                    
                    exchange_config = {
                        'active': False,
                        'api_key': '',
                        'secret': '',
                        'sandbox': True,
                        'symbols': ['BTC/USDT', 'ETH/USDT'],
                        'rate_limit': info.get('rateLimit', 1000)
                    }
                    
                    # Add passphrase if required
                    required_creds = info.get('requiredCredentials', {})
                    if required_creds.get('password', False):
                        exchange_config['passphrase'] = ''
                    
                    config['exchanges'][exchange_name] = exchange_config
                    
                except Exception as e:
                    logger.error(f"Error creating config for {exchange_name}: {e}")
                    continue
            
            return config
            
        except Exception as e:
            logger.error(f"Error creating config template: {e}")
            return {}
    
    def save_config_template(self, filename: str = 'config_template.yaml', selected_exchanges: List[str] = None):
        """Save configuration template to file"""
        try:
            config = self.create_config_template(selected_exchanges)
            
            if config:
                with open(filename, 'w') as f:
                    yaml.dump(config, f, default_flow_style=False, indent=2)
                
                console.print(f"✅ Configuration template saved to {filename}", style="green")
                console.print("📝 Please edit the file to add your API credentials", style="yellow")
                
        except Exception as e:
            logger.error(f"Error saving config template: {e}")
            console.print(f"❌ Error saving config template: {e}", style="red")
    
    def display_popular_exchanges(self):
        """Display popular exchanges with their features"""
        try:
            popular_exchanges = [
                'binance', 'kraken', 'bybit', 'bitget', 'cex', 'deribit',
                'okx', 'poloniex', 'wazirx', 'bitbns', 'huobi', 'kucoin'
            ]
            
            console.print("🌟 Popular Cryptocurrency Exchanges", style="bold green")
            
            # Create table
            table = Table(title="Popular Exchanges for Algo Trading", show_header=True, header_style="bold cyan")
            table.add_column("Exchange", style="white", width=15)
            table.add_column("Name", style="green", width=20)
            table.add_column("Features", style="yellow", width=40)
            table.add_column("Suitable For", style="blue", width=20)
            
            exchange_features = {
                'binance': ('Binance', 'Spot, Futures, Options, High volume, Low fees', 'All levels'),
                'kraken': ('Kraken', 'Spot, Futures, High security, Regulated', 'Institutions'),
                'bybit': ('Bybit', 'Derivatives, Futures, High leverage', 'Futures trading'),
                'bitget': ('Bitget', 'Spot, Futures, Copy trading', 'All levels'),
                'cex': ('CEX.IO', 'Spot, Credit cards, Regulated', 'Beginners'),
                'deribit': ('Deribit', 'Options, Futures, BTC/ETH focus', 'Options trading'),
                'okx': ('OKX', 'Spot, Futures, DeFi, Wide range', 'Advanced'),
                'poloniex': ('Poloniex', 'Spot, Margin, Many altcoins', 'Altcoin trading'),
                'wazirx': ('WazirX', 'Spot, INR support, India focused', 'Indian users'),
                'bitbns': ('BitBNS', 'Spot, INR support, India focused', 'Indian users'),
                'huobi': ('Huobi', 'Spot, Futures, Global presence', 'All levels'),
                'kucoin': ('KuCoin', 'Spot, Futures, Many altcoins', 'Altcoin trading')
            }
            
            for exchange_id in popular_exchanges:
                if exchange_id in exchange_features:
                    name, features, suitable = exchange_features[exchange_id]
                    table.add_row(exchange_id, name, features, suitable)
            
            console.print(table)
            
        except Exception as e:
            logger.error(f"Error displaying popular exchanges: {e}")
            console.print(f"❌ Error displaying popular exchanges: {e}", style="red")
    
    def interactive_config_creator(self):
        """Interactive configuration creator"""
        try:
            console.print("🛠️ Interactive Configuration Creator", style="bold blue")
            
            # Display popular exchanges
            self.display_popular_exchanges()
            
            console.print("\nSelect exchanges to include in your configuration:")
            console.print("Enter exchange IDs separated by commas (e.g., binance,kraken,bybit)")
            console.print("Press Enter for default selection")
            
            user_input = input("Your selection: ").strip()
            
            if user_input:
                selected_exchanges = [ex.strip() for ex in user_input.split(',')]
                # Validate selections
                all_exchanges = self.get_all_exchanges()
                valid_exchanges = [ex for ex in selected_exchanges if ex in all_exchanges]
                
                if valid_exchanges:
                    console.print(f"✅ Selected exchanges: {', '.join(valid_exchanges)}", style="green")
                    self.save_config_template('config.yaml', valid_exchanges)
                else:
                    console.print("❌ No valid exchanges selected", style="red")
            else:
                # Use default popular exchanges
                console.print("Using default popular exchanges", style="yellow")
                self.save_config_template('config.yaml')
            
        except Exception as e:
            logger.error(f"Error in interactive config creator: {e}")
            console.print(f"❌ Error in interactive config creator: {e}", style="red")

def main():
    """Main entry point"""
    try:
        console.print("🔗 CCXT Exchange List Manager", style="bold blue")
        
        manager = ExchangeListManager()
        
        # Display menu
        console.print("\nSelect an option:", style="bold yellow")
        console.print("1. Display all supported exchanges")
        console.print("2. Display popular exchanges")
        console.print("3. Create configuration template")
        console.print("4. Interactive configuration creator")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            manager.display_exchanges_table()
        elif choice == '2':
            manager.display_popular_exchanges()
        elif choice == '3':
            manager.save_config_template()
        elif choice == '4':
            manager.interactive_config_creator()
        else:
            console.print("❌ Invalid choice", style="red")
            
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!", style="yellow")
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
