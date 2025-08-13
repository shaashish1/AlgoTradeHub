"use client"

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Coins, RefreshCw, AlertTriangle } from 'lucide-react'
import { formatCurrency, formatPercentage, getPercentageColor } from '@/lib/utils'

interface Position {
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

const mockPositions: Position[] = [
  {
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
    symbol: 'ETH/USDT',
    side: 'SHORT',
    entryPrice: 2850,
    currentPrice: 2820,
    quantity: 1.5,
    pnl: 150,
    pnlPercentage: 1.1,
    duration: '45m',
    exchange: 'Binance'
  },
  {
    symbol: 'SOL/USDT',
    side: 'LONG',
    entryPrice: 98.50,
    currentPrice: 97.20,
    quantity: 5.0,
    pnl: -65,
    pnlPercentage: -1.3,
    duration: '1h 30m',
    exchange: 'Kraken'
  }
]

export function OpenPositions() {
  const totalPnL = mockPositions.reduce((sum, pos) => sum + pos.pnl, 0)
  const totalPnLPercentage = (totalPnL / 10000) * 100 // Assuming 10k portfolio

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center space-x-2">
            <Coins className="h-5 w-5" />
            <span>Open Positions</span>
            <Badge variant="secondary">{mockPositions.length}</Badge>
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
        {mockPositions.length > 0 ? (
          <div className="space-y-4">
            {/* Positions Table */}
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
                  {mockPositions.map((position, index) => (
                    <tr key={index} className="position-row">
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
            
            {/* Total P&L */}
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
            <Coins className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p>No open positions</p>
            <p className="text-sm">Positions will appear here when the scanner finds trading opportunities</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}