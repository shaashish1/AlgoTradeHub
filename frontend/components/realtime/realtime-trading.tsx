"use client"

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Play, 
  Square, 
  Settings, 
  Activity, 
  TrendingUp,
  TrendingDown,
  RefreshCw,
  AlertTriangle,
  Gamepad2,
  DollarSign
} from 'lucide-react'
import { formatCurrency, formatPercentage, getPercentageColor } from '@/lib/utils'

interface Position {
  id: string
  symbol: string
  side: 'LONG' | 'SHORT'
  entryPrice: number
  currentPrice: number
  quantity: number
  pnl: number
  pnlPercentage: number
  duration: string
  exchange: string
}

interface Signal {
  id: string
  type: 'BUY' | 'SELL' | 'WAIT'
  symbol: string
  price: number
  indicator: string
  strength: number
  time: string
}

const mockPositions: Position[] = [
  {
    id: '1',
    symbol: 'BTC/USDT',
    side: 'LONG',
    entryPrice: 45230,
    currentPrice: 46100,
    quantity: 0.1,
    pnl: 870,
    pnlPercentage: 1.9,
    duration: '2h 15m',
    exchange: 'Binance'
  },
  {
    id: '2',
    symbol: 'ETH/USDT',
    side: 'SHORT',
    entryPrice: 2850,
    currentPrice: 2820,
    quantity: 1.5,
    pnl: 150,
    pnlPercentage: 1.1,
    duration: '45m',
    exchange: 'Binance'
  }
]

const mockSignals: Signal[] = [
  {
    id: '1',
    type: 'SELL',
    symbol: 'ETH/USDT',
    price: 2845,
    indicator: 'RSI: 78',
    strength: 85,
    time: '14:35'
  },
  {
    id: '2',
    type: 'BUY',
    symbol: 'SOL/USDT',
    price: 97.50,
    indicator: 'Bollinger: Oversold',
    strength: 72,
    time: '14:32'
  },
  {
    id: '3',
    type: 'WAIT',
    symbol: 'BTC/USDT',
    price: 45230,
    indicator: 'MACD: Neutral',
    strength: 45,
    time: '14:30'
  }
]

export function RealTimeTrading() {
  const [scannerRunning, setScannerRunning] = useState(true)
  const [tradingMode, setTradingMode] = useState<'DEMO' | 'LIVE'>('DEMO')
  const [positions, setPositions] = useState<Position[]>(mockPositions)
  const [signals, setSignals] = useState<Signal[]>(mockSignals)
  const [lastUpdate, setLastUpdate] = useState(new Date())

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      // Update positions with small price changes
      setPositions(prev => prev.map(pos => {
        const priceChange = (Math.random() - 0.5) * pos.currentPrice * 0.001
        const newPrice = pos.currentPrice + priceChange
        const pnl = (newPrice - pos.entryPrice) * pos.quantity * (pos.side === 'LONG' ? 1 : -1)
        const pnlPercentage = (pnl / (pos.entryPrice * pos.quantity)) * 100
        
        return {
          ...pos,
          currentPrice: newPrice,
          pnl,
          pnlPercentage
        }
      }))
      
      setLastUpdate(new Date())
    }, 2000)

    return () => clearInterval(interval)
  }, [])

  const totalPnL = positions.reduce((sum, pos) => sum + pos.pnl, 0)
  const totalPnLPercentage = (totalPnL / 10000) * 100

  const startScanner = async () => {
    setScannerRunning(true)
    // Here you would call the backend API
    console.log('Starting scanner...')
  }

  const stopScanner = async () => {
    setScannerRunning(false)
    // Here you would call the backend API
    console.log('Stopping scanner...')
  }

  const toggleTradingMode = () => {
    if (tradingMode === 'DEMO') {
      // Show warning for live trading
      if (confirm('⚠️ WARNING: Live trading uses real money. Are you sure?')) {
        setTradingMode('LIVE')
      }
    } else {
      setTradingMode('DEMO')
    }
  }

  const getSignalIcon = (type: string) => {
    switch (type) {
      case 'BUY':
        return <TrendingUp className="h-4 w-4 text-success" />
      case 'SELL':
        return <TrendingDown className="h-4 w-4 text-danger" />
      default:
        return <Activity className="h-4 w-4 text-muted-foreground" />
    }
  }

  const getSignalColor = (type: string) => {
    switch (type) {
      case 'BUY':
        return 'success'
      case 'SELL':
        return 'destructive'
      default:
        return 'secondary'
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-4">
      {/* Control Panel */}
      <div className="space-y-6 lg:col-span-1">
        {/* Scanner Control */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Play className="h-5 w-5" />
              <span>Scanner Control</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Button 
                className="w-full" 
                variant={scannerRunning ? "destructive" : "default"}
                onClick={scannerRunning ? stopScanner : startScanner}
              >
                {scannerRunning ? (
                  <>
                    <Square className="h-4 w-4 mr-2" />
                    Stop Scanner
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4 mr-2" />
                    Start Scanner
                  </>
                )}
              </Button>
              
              <Button variant="outline" className="w-full">
                <Settings className="h-4 w-4 mr-2" />
                Settings
              </Button>
            </div>
            
            <div className="pt-4 border-t">
              <h4 className="font-medium mb-2">Trading Mode</h4>
              <Button 
                variant={tradingMode === 'LIVE' ? "destructive" : "secondary"}
                className="w-full"
                onClick={toggleTradingMode}
              >
                <Gamepad2 className="h-4 w-4 mr-2" />
                {tradingMode} Mode
              </Button>
              <p className="text-xs text-muted-foreground mt-2">
                {tradingMode === 'LIVE' 
                  ? '⚠️ Live trading uses real money!' 
                  : '🎮 Demo mode - no real money involved'
                }
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Strategy Status */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Activity className="h-5 w-5" />
              <span>Strategy Status</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div>
                <h4 className="font-medium">RSI Strategy</h4>
                <p className="text-sm text-muted-foreground">Active</p>
              </div>
              
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>RSI Period:</span>
                  <span>14</span>
                </div>
                <div className="flex justify-between">
                  <span>Overbought:</span>
                  <span>70</span>
                </div>
                <div className="flex justify-between">
                  <span>Oversold:</span>
                  <span>30</span>
                </div>
                <div className="flex justify-between">
                  <span>Scan Interval:</span>
                  <span>5s</span>
                </div>
              </div>
              
              <div className="pt-2 border-t">
                <Button variant="outline" size="sm" className="w-full">
                  Configure Strategy
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <div className="space-y-6 lg:col-span-3">
        {/* Live Signals */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center space-x-2">
                <Activity className="h-5 w-5" />
                <span>Live Trading Signals</span>
              </CardTitle>
              <div className="flex items-center space-x-2">
                <Badge variant={scannerRunning ? "success" : "secondary"}>
                  {scannerRunning ? 'ACTIVE' : 'STOPPED'}
                </Badge>
                <Button variant="outline" size="sm" onClick={() => setLastUpdate(new Date())}>
                  <RefreshCw className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {signals.map((signal) => (
                <div key={signal.id} className="flex items-center justify-between p-3 rounded-lg border">
                  <div className="flex items-center space-x-3">
                    {getSignalIcon(signal.type)}
                    <div>
                      <div className="font-medium">
                        {signal.type} {signal.symbol}
                      </div>
                      <div className="text-sm text-muted-foreground">
                        {signal.indicator} • Strength: {signal.strength}%
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-mono text-sm">
                      {formatCurrency(signal.price)}
                    </div>
                    <div className="text-xs text-muted-foreground">
                      {signal.time}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Open Positions */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center space-x-2">
                <DollarSign className="h-5 w-5" />
                <span>Open Positions</span>
                <Badge variant="secondary">{positions.length}</Badge>
              </CardTitle>
              <div className="flex items-center space-x-2">
                <Button variant="outline" size="sm">
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Refresh
                </Button>
                <Button variant="outline" size="sm">
                  <AlertTriangle className="h-4 w-4 mr-2" />
                  Close All
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            {positions.length > 0 ? (
              <div className="space-y-4">
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b text-sm text-muted-foreground">
                        <th className="text-left py-2">Symbol</th>
                        <th className="text-left py-2">Side</th>
                        <th className="text-right py-2">Entry</th>
                        <th className="text-right py-2">Current</th>
                        <th className="text-right py-2">P&L</th>
                        <th className="text-right py-2">P&L%</th>
                        <th className="text-right py-2">Duration</th>
                      </tr>
                    </thead>
                    <tbody>
                      {positions.map((position) => (
                        <tr key={position.id} className="border-b hover:bg-muted/50">
                          <td className="py-3">
                            <div>
                              <div className="font-medium">{position.symbol}</div>
                              <div className="text-xs text-muted-foreground">{position.exchange}</div>
                            </div>
                          </td>
                          <td className="py-3">
                            <Badge 
                              variant={position.side === 'LONG' ? 'default' : 'destructive'}
                              className="text-xs"
                            >
                              {position.side}
                            </Badge>
                          </td>
                          <td className="text-right py-3 font-mono text-sm">
                            {formatCurrency(position.entryPrice)}
                          </td>
                          <td className="text-right py-3 font-mono text-sm">
                            {formatCurrency(position.currentPrice)}
                          </td>
                          <td className={`text-right py-3 font-mono text-sm ${getPercentageColor(position.pnl)}`}>
                            {formatCurrency(position.pnl)}
                          </td>
                          <td className={`text-right py-3 font-mono text-sm ${getPercentageColor(position.pnl)}`}>
                            {formatPercentage(position.pnlPercentage)}
                          </td>
                          <td className="text-right py-3 text-sm text-muted-foreground">
                            {position.duration}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                
                <div className="flex justify-between items-center pt-4 border-t">
                  <span className="font-medium">Total P&L:</span>
                  <div className="text-right">
                    <div className={`font-bold ${getPercentageColor(totalPnL)}`}>
                      {formatCurrency(totalPnL)}
                    </div>
                    <div className={`text-sm ${getPercentageColor(totalPnL)}`}>
                      {formatPercentage(totalPnLPercentage)}
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                <DollarSign className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>No open positions</p>
                <p className="text-sm">Positions will appear when the scanner finds opportunities</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Status Footer */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center space-x-4">
                <span className="text-muted-foreground">Last Update:</span>
                <span>{lastUpdate.toLocaleTimeString()}</span>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-muted-foreground">Status:</span>
                <Badge variant={scannerRunning ? "success" : "secondary"}>
                  {scannerRunning ? 'Running' : 'Stopped'}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}