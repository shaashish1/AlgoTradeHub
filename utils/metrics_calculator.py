#!/usr/bin/env python3
"""
Metrics Calculator Module
Calculates comprehensive trading performance metrics
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetricsCalculator:
    def __init__(self):
        """Initialize metrics calculator"""
        self.risk_free_rate = 0.02  # 2% risk-free rate
        
    def calculate_all_metrics(self, portfolio_values: pd.Series, 
                            benchmark_values: pd.Series = None,
                            trades: List[Dict] = None) -> Dict:
        """Calculate all performance metrics"""
        try:
            metrics = {}
            
            # Basic metrics
            metrics.update(self.calculate_basic_metrics(portfolio_values))
            
            # Return metrics
            metrics.update(self.calculate_return_metrics(portfolio_values))
            
            # Risk metrics
            metrics.update(self.calculate_risk_metrics(portfolio_values))
            
            # Drawdown metrics
            metrics.update(self.calculate_drawdown_metrics(portfolio_values))
            
            # Benchmark comparison
            if benchmark_values is not None:
                metrics.update(self.calculate_benchmark_metrics(portfolio_values, benchmark_values))
            
            # Trade analysis
            if trades is not None:
                metrics.update(self.calculate_trade_metrics(trades))
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {e}")
            return {}
    
    def calculate_basic_metrics(self, portfolio_values: pd.Series) -> Dict:
        """Calculate basic performance metrics"""
        try:
            if len(portfolio_values) < 2:
                return {}
            
            initial_value = portfolio_values.iloc[0]
            final_value = portfolio_values.iloc[-1]
            peak_value = portfolio_values.max()
            
            # Calculate duration
            if hasattr(portfolio_values.index, 'to_pydatetime'):
                start_date = portfolio_values.index[0]
                end_date = portfolio_values.index[-1]
                duration = (end_date - start_date).days
            else:
                duration = len(portfolio_values)
            
            metrics = {
                'Start': portfolio_values.index[0] if hasattr(portfolio_values.index, 'strftime') else 'N/A',
                'End': portfolio_values.index[-1] if hasattr(portfolio_values.index, 'strftime') else 'N/A',
                'Duration': duration,
                'Equity Final [$]': final_value,
                'Equity Peak [$]': peak_value,
                'Return [%]': ((final_value - initial_value) / initial_value) * 100
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating basic metrics: {e}")
            return {}
    
    def calculate_return_metrics(self, portfolio_values: pd.Series) -> Dict:
        """Calculate return-based metrics"""
        try:
            if len(portfolio_values) < 2:
                return {}
            
            returns = portfolio_values.pct_change().dropna()
            
            if len(returns) == 0:
                return {}
            
            # Calculate periods per year (assume daily data)
            periods_per_year = 252  # Trading days per year
            
            # Adjust if we have different frequency
            if hasattr(portfolio_values.index, 'freq'):
                if portfolio_values.index.freq == 'H':
                    periods_per_year = 252 * 24
                elif portfolio_values.index.freq == 'T':
                    periods_per_year = 252 * 24 * 60
            
            # Total return
            total_return = (portfolio_values.iloc[-1] / portfolio_values.iloc[0] - 1) * 100
            
            # Annualized return
            years = len(returns) / periods_per_year
            annualized_return = (pow(portfolio_values.iloc[-1] / portfolio_values.iloc[0], 1/years) - 1) * 100 if years > 0 else 0
            
            # Volatility
            volatility = returns.std() * np.sqrt(periods_per_year) * 100
            
            # CAGR
            cagr = annualized_return
            
            metrics = {
                'Return (Ann.) [%]': annualized_return,
                'Volatility (Ann.) [%]': volatility,
                'CAGR [%]': cagr
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating return metrics: {e}")
            return {}
    
    def calculate_risk_metrics(self, portfolio_values: pd.Series) -> Dict:
        """Calculate risk-adjusted metrics"""
        try:
            if len(portfolio_values) < 2:
                return {}
            
            returns = portfolio_values.pct_change().dropna()
            
            if len(returns) == 0:
                return {}
            
            # Calculate annualized metrics
            periods_per_year = 252
            years = len(returns) / periods_per_year
            
            annualized_return = (pow(portfolio_values.iloc[-1] / portfolio_values.iloc[0], 1/years) - 1) * 100 if years > 0 else 0
            volatility = returns.std() * np.sqrt(periods_per_year) * 100
            
            # Sharpe Ratio
            excess_return = annualized_return - self.risk_free_rate * 100
            sharpe_ratio = excess_return / volatility if volatility > 0 else 0
            
            # Sortino Ratio
            downside_returns = returns[returns < 0]
            if len(downside_returns) > 0:
                downside_deviation = downside_returns.std() * np.sqrt(periods_per_year) * 100
                sortino_ratio = excess_return / downside_deviation if downside_deviation > 0 else 0
            else:
                sortino_ratio = 0
            
            # Calmar Ratio
            max_drawdown = self.calculate_max_drawdown(portfolio_values)
            calmar_ratio = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0
            
            metrics = {
                'Sharpe Ratio': sharpe_ratio,
                'Sortino Ratio': sortino_ratio,
                'Calmar Ratio': calmar_ratio
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating risk metrics: {e}")
            return {}
    
    def calculate_drawdown_metrics(self, portfolio_values: pd.Series) -> Dict:
        """Calculate drawdown metrics"""
        try:
            if len(portfolio_values) < 2:
                return {}
            
            # Calculate running maximum
            running_max = portfolio_values.expanding().max()
            
            # Calculate drawdown
            drawdown = (portfolio_values - running_max) / running_max * 100
            
            # Max drawdown
            max_drawdown = drawdown.min()
            
            # Average drawdown
            negative_drawdowns = drawdown[drawdown < 0]
            avg_drawdown = negative_drawdowns.mean() if len(negative_drawdowns) > 0 else 0
            
            # Drawdown duration calculations
            drawdown_periods = self.calculate_drawdown_periods(drawdown)
            max_drawdown_duration = max(drawdown_periods) if drawdown_periods else 0
            avg_drawdown_duration = np.mean(drawdown_periods) if drawdown_periods else 0
            
            metrics = {
                'Max. Drawdown [%]': max_drawdown,
                'Avg. Drawdown [%]': avg_drawdown,
                'Max. Drawdown Duration': max_drawdown_duration,
                'Avg. Drawdown Duration': avg_drawdown_duration
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating drawdown metrics: {e}")
            return {}
    
    def calculate_max_drawdown(self, portfolio_values: pd.Series) -> float:
        """Calculate maximum drawdown"""
        try:
            running_max = portfolio_values.expanding().max()
            drawdown = (portfolio_values - running_max) / running_max * 100
            return drawdown.min()
            
        except Exception as e:
            logger.error(f"Error calculating max drawdown: {e}")
            return 0.0
    
    def calculate_drawdown_periods(self, drawdown: pd.Series) -> List[int]:
        """Calculate drawdown periods"""
        try:
            periods = []
            current_period = 0
            in_drawdown = False
            
            for value in drawdown:
                if value < 0:
                    if not in_drawdown:
                        in_drawdown = True
                        current_period = 1
                    else:
                        current_period += 1
                else:
                    if in_drawdown:
                        periods.append(current_period)
                        in_drawdown = False
                        current_period = 0
            
            # Handle case where we end in drawdown
            if in_drawdown:
                periods.append(current_period)
            
            return periods
            
        except Exception as e:
            logger.error(f"Error calculating drawdown periods: {e}")
            return []
    
    def calculate_benchmark_metrics(self, portfolio_values: pd.Series, 
                                  benchmark_values: pd.Series) -> Dict:
        """Calculate benchmark comparison metrics"""
        try:
            if len(portfolio_values) != len(benchmark_values):
                return {}
            
            # Benchmark return
            benchmark_return = (benchmark_values.iloc[-1] / benchmark_values.iloc[0] - 1) * 100
            
            # Portfolio and benchmark returns
            portfolio_returns = portfolio_values.pct_change().dropna()
            benchmark_returns = benchmark_values.pct_change().dropna()
            
            if len(portfolio_returns) != len(benchmark_returns):
                return {}
            
            # Beta calculation
            covariance = np.cov(portfolio_returns, benchmark_returns)[0, 1]
            benchmark_variance = np.var(benchmark_returns)
            beta = covariance / benchmark_variance if benchmark_variance != 0 else 0
            
            # Alpha calculation
            periods_per_year = 252
            years = len(portfolio_returns) / periods_per_year
            portfolio_annualized_return = (pow(portfolio_values.iloc[-1] / portfolio_values.iloc[0], 1/years) - 1) * 100 if years > 0 else 0
            benchmark_annualized_return = (pow(benchmark_values.iloc[-1] / benchmark_values.iloc[0], 1/years) - 1) * 100 if years > 0 else 0
            
            alpha = portfolio_annualized_return - (self.risk_free_rate * 100 + beta * (benchmark_annualized_return - self.risk_free_rate * 100))
            
            metrics = {
                'Buy & Hold Return [%]': benchmark_return,
                'Alpha [%]': alpha,
                'Beta': beta
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating benchmark metrics: {e}")
            return {}
    
    def calculate_trade_metrics(self, trades: List[Dict]) -> Dict:
        """Calculate trade-based metrics"""
        try:
            if not trades:
                return {
                    '# Trades': 0,
                    'Win Rate [%]': 0,
                    'Best Trade [%]': 0,
                    'Worst Trade [%]': 0,
                    'Avg. Trade [%]': 0,
                    'Max. Trade Duration': 0,
                    'Avg. Trade Duration': 0,
                    'Profit Factor': 0,
                    'Expectancy [%]': 0,
                    'Net Profit [$]': 0
                }
            
            # Filter completed trades
            completed_trades = [t for t in trades if t.get('exit_price') is not None]
            
            if not completed_trades:
                return {
                    '# Trades': 0,
                    'Win Rate [%]': 0,
                    'Best Trade [%]': 0,
                    'Worst Trade [%]': 0,
                    'Avg. Trade [%]': 0,
                    'Max. Trade Duration': 0,
                    'Avg. Trade Duration': 0,
                    'Profit Factor': 0,
                    'Expectancy [%]': 0,
                    'Net Profit [$]': 0
                }
            
            # Calculate PnL for each trade
            pnl_values = []
            pnl_percentages = []
            durations = []
            
            for trade in completed_trades:
                # Calculate PnL
                entry_price = trade.get('entry_price', 0)
                exit_price = trade.get('exit_price', 0)
                quantity = trade.get('quantity', 0)
                side = trade.get('side', 'buy')
                
                if side == 'buy':
                    pnl = (exit_price - entry_price) * quantity
                else:
                    pnl = (entry_price - exit_price) * quantity
                
                pnl_values.append(pnl)
                
                # Calculate percentage
                if entry_price > 0 and quantity > 0:
                    pnl_pct = (pnl / (entry_price * quantity)) * 100
                    pnl_percentages.append(pnl_pct)
                
                # Calculate duration
                entry_time = trade.get('entry_time')
                exit_time = trade.get('exit_time')
                
                if entry_time and exit_time:
                    if isinstance(entry_time, str):
                        entry_time = datetime.fromisoformat(entry_time)
                    if isinstance(exit_time, str):
                        exit_time = datetime.fromisoformat(exit_time)
                    
                    duration = (exit_time - entry_time).total_seconds() / 3600  # hours
                    durations.append(duration)
            
            # Calculate metrics
            total_trades = len(completed_trades)
            winning_trades = [pnl for pnl in pnl_values if pnl > 0]
            losing_trades = [pnl for pnl in pnl_values if pnl < 0]
            
            win_rate = len(winning_trades) / total_trades * 100 if total_trades > 0 else 0
            
            best_trade = max(pnl_percentages) if pnl_percentages else 0
            worst_trade = min(pnl_percentages) if pnl_percentages else 0
            avg_trade = np.mean(pnl_percentages) if pnl_percentages else 0
            
            max_duration = max(durations) if durations else 0
            avg_duration = np.mean(durations) if durations else 0
            
            # Profit factor
            gross_profit = sum(winning_trades) if winning_trades else 0
            gross_loss = abs(sum(losing_trades)) if losing_trades else 0
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else (float('inf') if gross_profit > 0 else 0)
            
            # Net profit
            net_profit = sum(pnl_values)
            
            # Expectancy
            expectancy = avg_trade
            
            metrics = {
                '# Trades': total_trades,
                'Win Rate [%]': win_rate,
                'Best Trade [%]': best_trade,
                'Worst Trade [%]': worst_trade,
                'Avg. Trade [%]': avg_trade,
                'Max. Trade Duration': max_duration,
                'Avg. Trade Duration': avg_duration,
                'Profit Factor': profit_factor if profit_factor != float('inf') else 999.99,
                'Expectancy [%]': expectancy,
                'Net Profit [$]': net_profit
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating trade metrics: {e}")
            return {}
    
    def calculate_exposure_time(self, portfolio_values: pd.Series, 
                              trades: List[Dict]) -> float:
        """Calculate exposure time percentage"""
        try:
            if not trades or len(portfolio_values) < 2:
                return 0.0
            
            # Calculate total time
            total_time = portfolio_values.index[-1] - portfolio_values.index[0]
            total_seconds = total_time.total_seconds()
            
            # Calculate time in market
            time_in_market = timedelta(0)
            
            for trade in trades:
                entry_time = trade.get('entry_time')
                exit_time = trade.get('exit_time')
                
                if entry_time and exit_time:
                    if isinstance(entry_time, str):
                        entry_time = datetime.fromisoformat(entry_time)
                    if isinstance(exit_time, str):
                        exit_time = datetime.fromisoformat(exit_time)
                    
                    trade_duration = exit_time - entry_time
                    time_in_market += trade_duration
            
            # Calculate exposure percentage
            exposure_percentage = (time_in_market.total_seconds() / total_seconds) * 100
            
            return min(100, exposure_percentage)  # Cap at 100%
            
        except Exception as e:
            logger.error(f"Error calculating exposure time: {e}")
            return 0.0
    
    def calculate_information_ratio(self, portfolio_returns: pd.Series, 
                                  benchmark_returns: pd.Series) -> float:
        """Calculate information ratio"""
        try:
            if len(portfolio_returns) != len(benchmark_returns):
                return 0.0
            
            # Calculate active returns
            active_returns = portfolio_returns - benchmark_returns
            
            # Calculate tracking error
            tracking_error = active_returns.std() * np.sqrt(252)
            
            # Calculate information ratio
            active_return = active_returns.mean() * 252
            information_ratio = active_return / tracking_error if tracking_error != 0 else 0
            
            return information_ratio
            
        except Exception as e:
            logger.error(f"Error calculating information ratio: {e}")
            return 0.0
    
    def calculate_var(self, returns: pd.Series, confidence_level: float = 0.05) -> float:
        """Calculate Value at Risk"""
        try:
            if len(returns) == 0:
                return 0.0
            
            # Calculate VaR at given confidence level
            var = np.percentile(returns, confidence_level * 100)
            
            return var * 100  # Convert to percentage
            
        except Exception as e:
            logger.error(f"Error calculating VaR: {e}")
            return 0.0
    
    def calculate_cvar(self, returns: pd.Series, confidence_level: float = 0.05) -> float:
        """Calculate Conditional Value at Risk (Expected Shortfall)"""
        try:
            if len(returns) == 0:
                return 0.0
            
            # Calculate VaR threshold
            var_threshold = np.percentile(returns, confidence_level * 100)
            
            # Calculate CVaR (average of returns below VaR)
            tail_losses = returns[returns <= var_threshold]
            cvar = tail_losses.mean() if len(tail_losses) > 0 else 0
            
            return cvar * 100  # Convert to percentage
            
        except Exception as e:
            logger.error(f"Error calculating CVaR: {e}")
            return 0.0
    
    def format_metrics(self, metrics: Dict) -> Dict:
        """Format metrics for display"""
        try:
            formatted = {}
            
            for key, value in metrics.items():
                if isinstance(value, float):
                    if 'Duration' in key and 'Max.' not in key and 'Avg.' not in key:
                        formatted[key] = f"{value:.0f} days"
                    elif '[%]' in key:
                        formatted[key] = f"{value:.2f}%"
                    elif '[$]' in key:
                        formatted[key] = f"${value:,.2f}"
                    elif key in ['Sharpe Ratio', 'Sortino Ratio', 'Calmar Ratio', 'Beta']:
                        formatted[key] = f"{value:.4f}"
                    else:
                        formatted[key] = f"{value:.2f}"
                else:
                    formatted[key] = str(value)
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error formatting metrics: {e}")
            return metrics
