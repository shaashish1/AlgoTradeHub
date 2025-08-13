# 🎨 AlgoTradeHub Frontend

Modern Next.js frontend for the AlgoTradeHub trading platform with comprehensive trading tools and analytics.

## ✨ Features

### 🏠 Dashboard
- **Portfolio Overview**: Real-time portfolio value and performance metrics
- **Quick Stats**: Total return, win rate, active positions, and recent trades
- **Exchange Status**: Live connection status for all configured exchanges
- **Quick Actions**: One-click access to trading, backtesting, and configuration
- **Recent Activity**: Latest trades and alerts

### 🧪 Backtesting Suite
- **Simple Backtest**: Quick strategy testing with basic parameters
- **Comprehensive Suite**: Multi-strategy, multi-asset, multi-timeframe analysis
- **Real-time Progress**: Live progress tracking with estimated completion times
- **Interactive Results**: Detailed performance charts and metrics
- **Export Capabilities**: Download results as CSV or PDF

### ⚡ Real-time Trading
- **Live Scanner**: Real-time market monitoring across multiple exchanges
- **Signal Dashboard**: Trading signals with strength indicators
- **Position Management**: Live P&L tracking and position monitoring
- **Risk Controls**: Real-time risk metrics and alerts

### 📊 Performance Analytics
- **Portfolio Charts**: Interactive performance visualization
- **Strategy Comparison**: Side-by-side strategy performance analysis
- **Risk Metrics**: Sharpe ratio, max drawdown, profit factor
- **Trade Analysis**: Detailed trade history and statistics

### 🔧 Feature Browser
- **Tool Discovery**: Central hub for all available features
- **Quick Launch**: One-click access to any trading tool
- **Advanced Options**: Comprehensive configuration for power users

### ⚙️ Settings & Configuration
- **Exchange Setup**: API key management with sandbox mode
- **Trading Parameters**: Risk settings and position sizing
- **Notifications**: Email and push notification preferences
- **System Preferences**: Theme, language, and display options

## 🚀 Getting Started

### Prerequisites
- Node.js 16+ 
- npm or yarn
- Running AlgoTradeHub backend (Python)

### Installation

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Open in browser**:
   ```
   http://localhost:3000
   ```

## 🏗️ Project Structure

```
frontend/
├── app/                      # Next.js 13+ App Router
│   ├── page.tsx             # Dashboard (home page)
│   ├── backtest/            # Backtesting pages
│   │   ├── page.tsx         # Simple backtest
│   │   └── comprehensive/   # Advanced backtesting
│   ├── realtime/            # Real-time trading
│   ├── performance/         # Analytics dashboard
│   ├── features/            # Feature browser
│   ├── settings/            # Configuration
│   ├── test/                # Testing interface
│   ├── layout.tsx           # Root layout
│   └── globals.css          # Global styles
├── components/              # React components
│   ├── ui/                  # Base UI components (shadcn/ui)
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   └── ...
│   ├── layout/              # Layout components
│   │   └── header.tsx       # Navigation header
│   ├── dashboard/           # Dashboard components
│   │   ├── quick-stats.tsx
│   │   ├── portfolio-chart.tsx
│   │   └── ...
│   ├── backtest/            # Backtesting components
│   │   ├── backtest-configuration.tsx
│   │   ├── backtest-progress.tsx
│   │   └── backtest-results.tsx
│   ├── realtime/            # Real-time components
│   ├── performance/         # Analytics components
│   ├── features/            # Feature browser components
│   ├── settings/            # Settings components
│   └── test/                # Testing components
├── lib/                     # Utilities and API
│   ├── utils.ts             # Utility functions
│   └── api.ts               # API client
├── package.json             # Dependencies and scripts
├── tailwind.config.js       # Tailwind CSS configuration
├── tsconfig.json            # TypeScript configuration
└── next.config.js           # Next.js configuration
```

## 🎨 UI Components

Built with **shadcn/ui** components for consistency and accessibility:

- **Button**: Various styles and sizes
- **Card**: Content containers with headers
- **Input**: Form inputs with validation
- **Badge**: Status indicators and labels
- **Progress**: Progress bars and loading states
- **Switch**: Toggle controls
- **Label**: Form labels
- **Select**: Dropdown selections

## 🔌 API Integration

The frontend communicates with the Python backend through a comprehensive API client:

```typescript
// lib/api.ts
export const api = {
  // Backtest endpoints
  runBacktest(config: BacktestConfig): Promise<BacktestResult>
  
  // Real-time trading
  startScanner(): Promise<{ success: boolean; message: string }>
  stopScanner(): Promise<{ success: boolean; message: string }>
  getSignals(): Promise<TradingSignal[]>
  getPositions(): Promise<Position[]>
  
  // System endpoints
  getSystemStatus(): Promise<{ status: string; exchanges: any[] }>
  
  // Configuration
  saveConfig(config: any): Promise<{ success: boolean }>
  getConfig(): Promise<any>
}
```

## 📱 Responsive Design

The interface is fully responsive and works across all device sizes:

- **Desktop**: Full-featured interface with multi-column layouts
- **Tablet**: Optimized layouts with collapsible sidebars
- **Mobile**: Touch-friendly interface with bottom navigation

## 🎯 Key Features

### Real-time Updates
- WebSocket connections for live data
- Automatic refresh of positions and signals
- Real-time chart updates

### Interactive Charts
- Built with Recharts for performance
- Responsive and touch-friendly
- Multiple chart types (line, bar, candlestick)

### Advanced Backtesting
- Multi-dimensional parameter selection
- Real-time progress tracking
- Comprehensive results visualization

### Modern UX
- Smooth animations and transitions
- Loading states and error handling
- Keyboard shortcuts and accessibility

## 🧪 Testing

### Manual Testing
Use the built-in test interface at `/test` to:
- Check backend connectivity
- Test API endpoints
- Validate data flow
- Monitor system health

### Development Testing
```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Build test
npm run build
```

## 🔧 Configuration

### Environment Variables
Create `.env.local` for custom configuration:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:5000

# Feature Flags
NEXT_PUBLIC_ENABLE_DEMO_MODE=true
NEXT_PUBLIC_ENABLE_LIVE_TRADING=false
```

### Customization
- **Themes**: Modify `globals.css` for custom styling
- **Components**: Extend or customize UI components
- **API**: Update `lib/api.ts` for custom endpoints

## 🚀 Deployment

### Development
```bash
npm run dev
```

### Production Build
```bash
npm run build
npm start
```

### Docker (Optional)
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🤝 Contributing

1. **Follow the existing code structure**
2. **Use TypeScript for type safety**
3. **Follow the component naming conventions**
4. **Add proper error handling**
5. **Test on multiple screen sizes**

### Code Style
- Use functional components with hooks
- Implement proper TypeScript types
- Follow the existing file structure
- Use shadcn/ui components when possible

## 📚 Documentation

- **Components**: Each component includes JSDoc comments
- **API**: Full API documentation in `lib/api.ts`
- **Types**: TypeScript interfaces for all data structures
- **Examples**: Usage examples in component files

## 🆘 Troubleshooting

### Common Issues

1. **Backend Connection Failed**:
   - Ensure Python backend is running on port 5000
   - Check CORS settings in Flask app
   - Verify API_URL environment variable

2. **Build Errors**:
   - Clear `.next` directory: `rm -rf .next`
   - Reinstall dependencies: `rm -rf node_modules && npm install`
   - Check TypeScript errors: `npm run type-check`

3. **Styling Issues**:
   - Ensure Tailwind CSS is properly configured
   - Check for conflicting CSS classes
   - Verify component imports

### Performance Optimization
- Use React.memo for expensive components
- Implement proper loading states
- Optimize API calls with caching
- Use Next.js Image component for images

---

**Built with ❤️ using Next.js, TypeScript, and shadcn/ui**