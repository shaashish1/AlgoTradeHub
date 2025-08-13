# Landing Page / Dashboard Wireframe

## Overview
The main dashboard provides users with a comprehensive overview of their trading performance, active positions, and quick access to key features.

## Layout Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Header Navigation                                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ Hero Section                                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ Quick Stats Cards                                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ Main Chart Area                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ Active Exchanges Status                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Open Positions Table                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ Footer / Status Bar                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### Header Navigation
- **Logo**: AlgoTradeHub with rocket icon
- **Navigation**: Dashboard, Backtest, Real-time, Features
- **User Menu**: Profile, Settings, Help
- **Status Indicators**: Scanner status, trading mode

### Hero Section
- **Welcome Message**: Personalized greeting
- **System Status**: Overall health indicator
- **Quick Actions**: Primary CTAs for common tasks

### Quick Stats Cards
- **Portfolio Value**: Current total value
- **Today's P&L**: Daily profit/loss with percentage
- **Win Rate**: Success rate of trades
- **Active Positions**: Number of open positions

### Main Chart Area
- **Interactive Chart**: Portfolio performance over time
- **Time Range Selector**: 1D, 1W, 1M, 3M, 1Y, ALL
- **Chart Type Toggle**: Portfolio, P&L, Trades, Drawdown
- **Zoom/Pan Controls**: For detailed analysis

### Active Exchanges
- **Exchange Cards**: Status, mode (sandbox/live), connection
- **Symbol Count**: Number of active trading pairs
- **Health Indicators**: Connection status, API limits

### Open Positions Table
- **Columns**: Symbol, Side, Entry Price, Current Price, P&L, P&L%, Duration
- **Color Coding**: Green for profits, red for losses
- **Action Buttons**: View details, close position
- **Sorting**: By P&L, duration, symbol

## Responsive Behavior

### Desktop (>1024px)
- Full layout with sidebar and main content
- Large charts with detailed information
- Multiple columns for stats and data

### Tablet (768px-1024px)
- Stacked layout with collapsible sidebar
- Medium-sized charts
- Two-column layout for stats

### Mobile (<768px)
- Single column layout
- Compact charts
- Swipeable cards for stats
- Bottom navigation

## Interactive Elements

### Real-time Updates
- **Auto-refresh**: Every 30 seconds
- **WebSocket**: Live price updates
- **Notifications**: Toast messages for alerts
- **Loading States**: Skeleton screens during updates

### User Actions
- **Quick Trade**: One-click trading from positions
- **Chart Interactions**: Hover for details, click for drill-down
- **Filter/Sort**: Dynamic table filtering
- **Export**: Data export functionality

## Accessibility Features
- **Keyboard Navigation**: Tab order, shortcuts
- **Screen Reader**: ARIA labels, semantic HTML
- **Color Contrast**: WCAG 2.1 AA compliance
- **Focus Indicators**: Clear focus states

## Performance Considerations
- **Lazy Loading**: Charts and tables load on demand
- **Virtualization**: Large tables use virtual scrolling
- **Caching**: API responses cached appropriately
- **Compression**: Assets optimized and compressed