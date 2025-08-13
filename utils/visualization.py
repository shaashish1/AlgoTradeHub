#!/usr/bin/env python3
"""
Visualization Module
Creates charts and graphs for trading analysis
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime
import base64
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class Visualizer:
    def __init__(self):
        """Initialize visualizer"""
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#F18F01',
            'danger': '#C73E1D',
            'warning': '#FFB30F',
            'info': '#17A2B8',
            'light': '#F8F9FA',
            'dark': '#343A40'
        }
        
        # Configure matplotlib
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
        
    def create_portfolio_chart(self, portfolio_values: pd.Series, 
                              benchmark_values: pd.Series = None,
                              title: str = "Portfolio Performance") -> go.Figure:
        """Create portfolio performance chart"""
        try:
            fig = go.Figure()
            
            # Add portfolio line
            fig.add_trace(go.Scatter(
                x=portfolio_values.index,
                y=portfolio_values.values,
                mode='lines',
                name='Portfolio',
                line=dict(color=self.colors['primary'], width=2)
            ))
            
            # Add benchmark if provided
            if benchmark_values is not None:
                fig.add_trace(go.Scatter(
                    x=benchmark_values.index,
                    y=benchmark_values.values,
                    mode='lines',
                    name='Benchmark',
                    line=dict(color=self.colors['secondary'], width=2, dash='dash')
                ))
            
            # Update layout
            fig.update_layout(
                title=title,
                xaxis_title="Date",
                yaxis_title="Portfolio Value ($)",
                template='plotly_white',
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating portfolio chart: {e}")
            return go.Figure()
    
    def create_drawdown_chart(self, portfolio_values: pd.Series, 
                            title: str = "Drawdown Analysis") -> go.Figure:
        """Create drawdown chart"""
        try:
            # Calculate drawdown
            running_max = portfolio_values.expanding().max()
            drawdown = (portfolio_values - running_max) / running_max * 100
            
            fig = go.Figure()
            
            # Add drawdown area
            fig.add_trace(go.Scatter(
                x=drawdown.index,
                y=drawdown.values,
                fill='tozeroy',
                mode='lines',
                name='Drawdown',
                line=dict(color=self.colors['danger'], width=1),
                fillcolor=f"rgba(199, 62, 29, 0.3)"
            ))
            
            # Add zero line
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            
            # Update layout
            fig.update_layout(
                title=title,
                xaxis_title="Date",
                yaxis_title="Drawdown (%)",
                template='plotly_white',
                hovermode='x unified',
                showlegend=False
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating drawdown chart: {e}")
            return go.Figure()
    
    def create_returns_distribution(self, portfolio_values: pd.Series,
                                  title: str = "Returns Distribution") -> go.Figure:
        """Create returns distribution chart"""
        try:
            returns = portfolio_values.pct_change().dropna() * 100
            
            fig = go.Figure()
            
            # Add histogram
            fig.add_trace(go.Histogram(
                x=returns.values,
                nbinsx=50,
                name='Returns',
                opacity=0.7,
                marker_color=self.colors['primary']
            ))
            
            # Add normal distribution overlay
            mean_return = returns.mean()
            std_return = returns.std()
            x_range = np.linspace(returns.min(), returns.max(), 100)
            normal_dist = (1 / (std_return * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_range - mean_return) / std_return) ** 2)
            
            # Scale normal distribution to match histogram
            normal_dist = normal_dist * len(returns) * (returns.max() - returns.min()) / 50
            
            fig.add_trace(go.Scatter(
                x=x_range,
                y=normal_dist,
                mode='lines',
                name='Normal Distribution',
                line=dict(color=self.colors['secondary'], width=2, dash='dash')
            ))
            
            # Update layout
            fig.update_layout(
                title=title,
                xaxis_title="Returns (%)",
                yaxis_title="Frequency",
                template='plotly_white',
                showlegend=True
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating returns distribution: {e}")
            return go.Figure()
    
    def create_trade_points_chart(self, price_data: pd.Series, 
                                trades: List[Dict],
                                title: str = "Trade Points") -> go.Figure:
        """Create chart showing trade entry/exit points"""
        try:
            fig = go.Figure()
            
            # Add price line
            fig.add_trace(go.Scatter(
                x=price_data.index,
                y=price_data.values,
                mode='lines',
                name='Price',
                line=dict(color=self.colors['dark'], width=2)
            ))
            
            # Add trade points
            buy_trades = [t for t in trades if t.get('side') == 'buy']
            sell_trades = [t for t in trades if t.get('side') == 'sell']
            
            if buy_trades:
                buy_times = [t['entry_time'] for t in buy_trades]
                buy_prices = [t['entry_price'] for t in buy_trades]
                
                fig.add_trace(go.Scatter(
                    x=buy_times,
                    y=buy_prices,
                    mode='markers',
                    name='Buy',
                    marker=dict(
                        color=self.colors['success'],
                        size=10,
                        symbol='triangle-up'
                    )
                ))
            
            if sell_trades:
                sell_times = [t['exit_time'] for t in sell_trades if t.get('exit_time')]
                sell_prices = [t['exit_price'] for t in sell_trades if t.get('exit_price')]
                
                fig.add_trace(go.Scatter(
                    x=sell_times,
                    y=sell_prices,
                    mode='markers',
                    name='Sell',
                    marker=dict(
                        color=self.colors['danger'],
                        size=10,
                        symbol='triangle-down'
                    )
                ))
            
            # Update layout
            fig.update_layout(
                title=title,
                xaxis_title="Date",
                yaxis_title="Price ($)",
                template='plotly_white',
                hovermode='x unified'
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating trade points chart: {e}")
            return go.Figure()
    
    def create_pnl_chart(self, trades: List[Dict], 
                        title: str = "PnL by Trade") -> go.Figure:
        """Create PnL chart"""
        try:
            if not trades:
                return go.Figure()
            
            # Calculate cumulative PnL
            trade_numbers = list(range(1, len(trades) + 1))
            individual_pnl = [t.get('pnl', 0) for t in trades]
            cumulative_pnl = np.cumsum(individual_pnl)
            
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Individual Trade PnL', 'Cumulative PnL'),
                vertical_spacing=0.1
            )
            
            # Individual PnL bar chart
            colors = [self.colors['success'] if pnl >= 0 else self.colors['danger'] for pnl in individual_pnl]
            
            fig.add_trace(go.Bar(
                x=trade_numbers,
                y=individual_pnl,
                name='Individual PnL',
                marker_color=colors,
                showlegend=False
            ), row=1, col=1)
            
            # Cumulative PnL line chart
            fig.add_trace(go.Scatter(
                x=trade_numbers,
                y=cumulative_pnl,
                mode='lines+markers',
                name='Cumulative PnL',
                line=dict(color=self.colors['primary'], width=2),
                showlegend=False
            ), row=2, col=1)
            
            # Update layout
            fig.update_layout(
                title=title,
                template='plotly_white',
                height=600
            )
            
            fig.update_xaxes(title_text="Trade Number", row=2, col=1)
            fig.update_yaxes(title_text="PnL ($)", row=1, col=1)
            fig.update_yaxes(title_text="Cumulative PnL ($)", row=2, col=1)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating PnL chart: {e}")
            return go.Figure()
    
    def create_metrics_table(self, metrics: Dict) -> go.Figure:
        """Create metrics table"""
        try:
            if not metrics:
                return go.Figure()
            
            # Prepare table data
            metric_names = []
            metric_values = []
            
            for key, value in metrics.items():
                metric_names.append(key.replace('_', ' ').title())
                
                if isinstance(value, float):
                    if 'percentage' in key or 'rate' in key:
                        metric_values.append(f"{value:.2f}%")
                    elif 'ratio' in key:
                        metric_values.append(f"{value:.3f}")
                    else:
                        metric_values.append(f"${value:.2f}")
                else:
                    metric_values.append(str(value))
            
            fig = go.Figure(data=[go.Table(
                header=dict(
                    values=['Metric', 'Value'],
                    fill_color=self.colors['light'],
                    align='left',
                    font=dict(size=12, color=self.colors['dark'])
                ),
                cells=dict(
                    values=[metric_names, metric_values],
                    fill_color='white',
                    align='left',
                    font=dict(size=11, color=self.colors['dark'])
                )
            )])
            
            fig.update_layout(
                title="Performance Metrics",
                template='plotly_white',
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating metrics table: {e}")
            return go.Figure()
    
    def create_heatmap(self, data: pd.DataFrame, 
                      title: str = "Correlation Heatmap") -> go.Figure:
        """Create correlation heatmap"""
        try:
            if data.empty:
                return go.Figure()
            
            # Calculate correlation matrix
            corr_matrix = data.corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=corr_matrix.values,
                texttemplate="%{text:.2f}",
                textfont={"size": 10},
                hoverongaps=False
            ))
            
            fig.update_layout(
                title=title,
                template='plotly_white',
                width=600,
                height=600
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating heatmap: {e}")
            return go.Figure()
    
    def create_candlestick_chart(self, ohlcv_data: pd.DataFrame,
                               title: str = "Price Chart") -> go.Figure:
        """Create candlestick chart"""
        try:
            if ohlcv_data.empty:
                return go.Figure()
            
            fig = go.Figure(data=go.Candlestick(
                x=ohlcv_data.index,
                open=ohlcv_data['open'],
                high=ohlcv_data['high'],
                low=ohlcv_data['low'],
                close=ohlcv_data['close'],
                name="Price"
            ))
            
            # Add volume subplot
            fig.add_trace(go.Bar(
                x=ohlcv_data.index,
                y=ohlcv_data['volume'],
                name="Volume",
                yaxis='y2',
                opacity=0.3
            ))
            
            # Update layout
            fig.update_layout(
                title=title,
                template='plotly_white',
                xaxis_title="Date",
                yaxis_title="Price ($)",
                yaxis2=dict(
                    title="Volume",
                    overlaying='y',
                    side='right'
                ),
                xaxis_rangeslider_visible=False
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating candlestick chart: {e}")
            return go.Figure()
    
    def fig_to_html(self, fig: go.Figure) -> str:
        """Convert plotly figure to HTML"""
        try:
            return fig.to_html(include_plotlyjs='cdn')
        except Exception as e:
            logger.error(f"Error converting figure to HTML: {e}")
            return "<div>Error generating chart</div>"
    
    def fig_to_json(self, fig: go.Figure) -> str:
        """Convert plotly figure to JSON"""
        try:
            return fig.to_json()
        except Exception as e:
            logger.error(f"Error converting figure to JSON: {e}")
            return "{}"
            
            if not available_metrics:
                return go.Figure()
