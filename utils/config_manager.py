#!/usr/bin/env python3
"""
Configuration Manager Module
Handles loading and managing configuration files
"""

import yaml
import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigManager:
    def __init__(self, config_path: str = "config.yaml", credentials_path: str = "config/credentials.yaml"):
        """Initialize configuration manager"""
        self.config_path = config_path
        self.credentials_path = credentials_path
        self.config = {}
        self.credentials = {}
        self.last_loaded = None
        
    def load_config(self) -> Dict[str, Any]:
        """Load main configuration file"""
        try:
            if not os.path.exists(self.config_path):
                logger.error(f"Configuration file not found: {self.config_path}")
                return self.get_default_config()
            
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            
            # Merge with credentials if available
            self.load_credentials()
            
            # Update exchange configs with credentials
            self.merge_credentials()
            
            # Validate configuration
            self.validate_config()
            
            self.last_loaded = datetime.now()
            logger.info(f"Configuration loaded successfully from {self.config_path}")
            
            return self.config
            
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return self.get_default_config()
    
    def load_credentials(self) -> Dict[str, Any]:
        """Load credentials from separate file"""
        try:
            if not os.path.exists(self.credentials_path):
                logger.warning(f"Credentials file not found: {self.credentials_path}")
                return {}
            
            with open(self.credentials_path, 'r') as f:
                self.credentials = yaml.safe_load(f)
            
            logger.info(f"Credentials loaded from {self.credentials_path}")
            return self.credentials
            
        except Exception as e:
            logger.error(f"Error loading credentials: {e}")
            return {}
    
    def merge_credentials(self):
        """Merge credentials into main config"""
        try:
            if not self.credentials:
                return
            
            # Merge exchange credentials
            for exchange_name, creds in self.credentials.get('exchanges', {}).items():
                if exchange_name in self.config.get('exchanges', {}):
                    self.config['exchanges'][exchange_name].update(creds)
            
            # Merge other credentials
            for key, value in self.credentials.items():
                if key != 'exchanges':
                    self.config[key] = value
                    
        except Exception as e:
            logger.error(f"Error merging credentials: {e}")
    
    def validate_config(self) -> bool:
        """Validate configuration structure"""
        try:
            required_sections = ['exchanges', 'backtest', 'strategy']
            
            for section in required_sections:
                if section not in self.config:
                    logger.error(f"Missing required configuration section: {section}")
                    return False
            
            # Validate exchanges
            if not self.config['exchanges']:
                logger.warning("No exchanges configured")
            
            # Validate backtest config
            backtest_config = self.config['backtest']
            required_backtest_fields = ['start_date', 'end_date', 'initial_capital', 'commission']
            
            for field in required_backtest_fields:
                if field not in backtest_config:
                    logger.error(f"Missing required backtest field: {field}")
                    return False
            
            # Validate strategy config
            strategy_config = self.config['strategy']
            if 'name' not in strategy_config:
                logger.error("Missing strategy name")
                return False
            
            logger.info("Configuration validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Error validating configuration: {e}")
            return False
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'exchanges': {
                'binance': {
                    'active': False,
                    'api_key': '',
                    'secret': '',
                    'sandbox': True,
                    'symbols': ['BTC/USDT', 'ETH/USDT'],
                    'rate_limit': 1200
                }
            },
            'backtest': {
                'start_date': '2023-01-01',
                'end_date': datetime.now().strftime('%Y-%m-%d'),
                'initial_capital': 10000,
                'commission': 0.001
            },
            'strategy': {
                'name': 'rsi_strategy',
                'parameters': {
                    'rsi_period': 14,
                    'rsi_overbought': 70,
                    'rsi_oversold': 30
                }
            },
            'live_trading': False,
            'scan_interval': 5,
            'max_positions': 3,
            'risk_per_trade': 0.02,
            'logging': {
                'level': 'INFO',
                'file': 'trading.log'
            }
        }
    
    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """Save configuration to file"""
        try:
            if config is None:
                config = self.config
            
            # Remove sensitive data before saving
            safe_config = self.remove_sensitive_data(config)
            
            with open(self.config_path, 'w') as f:
                yaml.dump(safe_config, f, default_flow_style=False, indent=2)
            
            logger.info(f"Configuration saved to {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
    
    def save_credentials(self, credentials: Dict[str, Any] = None) -> bool:
        """Save credentials to separate file"""
        try:
            if credentials is None:
                credentials = self.credentials
            
            # Ensure credentials directory exists
            os.makedirs(os.path.dirname(self.credentials_path), exist_ok=True)
            
            with open(self.credentials_path, 'w') as f:
                yaml.dump(credentials, f, default_flow_style=False, indent=2)
            
            logger.info(f"Credentials saved to {self.credentials_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving credentials: {e}")
            return False
    
    def remove_sensitive_data(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Remove sensitive data from config"""
        try:
            safe_config = config.copy()
            
            # Remove API keys and secrets from exchanges
            for exchange_name, exchange_config in safe_config.get('exchanges', {}).items():
                if 'api_key' in exchange_config:
                    exchange_config['api_key'] = ''
                if 'secret' in exchange_config:
                    exchange_config['secret'] = ''
                if 'passphrase' in exchange_config:
                    exchange_config['passphrase'] = ''
            
            return safe_config
            
        except Exception as e:
            logger.error(f"Error removing sensitive data: {e}")
            return config
    
    def get_exchange_config(self, exchange_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific exchange"""
        return self.config.get('exchanges', {}).get(exchange_name)
    
    def get_active_exchanges(self) -> Dict[str, Dict[str, Any]]:
        """Get all active exchanges"""
        active_exchanges = {}
        
        for exchange_name, exchange_config in self.config.get('exchanges', {}).items():
            if exchange_config.get('active', False):
                active_exchanges[exchange_name] = exchange_config
        
        return active_exchanges
    
    def update_exchange_config(self, exchange_name: str, config_updates: Dict[str, Any]) -> bool:
        """Update exchange configuration"""
        try:
            if exchange_name not in self.config.get('exchanges', {}):
                logger.error(f"Exchange {exchange_name} not found in configuration")
                return False
            
            self.config['exchanges'][exchange_name].update(config_updates)
            
            # Save to credentials file if sensitive data
            sensitive_fields = ['api_key', 'secret', 'passphrase']
            if any(field in config_updates for field in sensitive_fields):
                # Update credentials
                if 'exchanges' not in self.credentials:
                    self.credentials['exchanges'] = {}
                
                if exchange_name not in self.credentials['exchanges']:
                    self.credentials['exchanges'][exchange_name] = {}
                
                for field in sensitive_fields:
                    if field in config_updates:
                        self.credentials['exchanges'][exchange_name][field] = config_updates[field]
                
                self.save_credentials()
            
            # Save main config
            self.save_config()
            
            logger.info(f"Updated configuration for {exchange_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating exchange config: {e}")
            return False
    
    def get_backtest_config(self) -> Dict[str, Any]:
        """Get backtest configuration"""
        return self.config.get('backtest', {})
    
    def get_strategy_config(self) -> Dict[str, Any]:
        """Get strategy configuration"""
        return self.config.get('strategy', {})
    
    def update_strategy_config(self, config_updates: Dict[str, Any]) -> bool:
        """Update strategy configuration"""
        try:
            if 'strategy' not in self.config:
                self.config['strategy'] = {}
            
            self.config['strategy'].update(config_updates)
            self.save_config()
            
            logger.info("Updated strategy configuration")
            return True
            
        except Exception as e:
            logger.error(f"Error updating strategy config: {e}")
            return False
    
    def is_live_trading_enabled(self) -> bool:
        """Check if live trading is enabled"""
        return self.config.get('live_trading', False)
    
    def get_scan_interval(self) -> int:
        """Get scan interval in seconds"""
        return self.config.get('scan_interval', 5)
    
    def get_risk_per_trade(self) -> float:
        """Get risk per trade percentage"""
        return self.config.get('risk_per_trade', 0.02)
    
    def get_max_positions(self) -> int:
        """Get maximum number of positions"""
        return self.config.get('max_positions', 3)
    
    def reload_config(self) -> Dict[str, Any]:
        """Reload configuration from file"""
        logger.info("Reloading configuration...")
        return self.load_config()
    
    def export_config(self, export_path: str) -> bool:
        """Export configuration to file"""
        try:
            safe_config = self.remove_sensitive_data(self.config)
            
            with open(export_path, 'w') as f:
                yaml.dump(safe_config, f, default_flow_style=False, indent=2)
            
            logger.info(f"Configuration exported to {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting configuration: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """Import configuration from file"""
        try:
            if not os.path.exists(import_path):
                logger.error(f"Import file not found: {import_path}")
                return False
            
            with open(import_path, 'r') as f:
                imported_config = yaml.safe_load(f)
            
            # Validate imported config
            old_config = self.config.copy()
            self.config = imported_config
            
            if not self.validate_config():
                self.config = old_config
                logger.error("Imported configuration is invalid")
                return False
            
            # Save imported config
            self.save_config()
            
            logger.info(f"Configuration imported from {import_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error importing configuration: {e}")
            return False
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get configuration summary"""
        try:
            active_exchanges = list(self.get_active_exchanges().keys())
            
            summary = {
                'active_exchanges': active_exchanges,
                'strategy': self.config.get('strategy', {}).get('name', 'unknown'),
                'live_trading': self.is_live_trading_enabled(),
                'scan_interval': self.get_scan_interval(),
                'backtest_period': f"{self.get_backtest_config().get('start_date')} to {self.get_backtest_config().get('end_date')}",
                'initial_capital': self.get_backtest_config().get('initial_capital', 0),
                'last_loaded': self.last_loaded.isoformat() if self.last_loaded else None
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting config summary: {e}")
            return {}
