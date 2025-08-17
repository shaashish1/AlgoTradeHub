'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { TrendingUp, TrendingDown, RefreshCw, Wallet, BarChart3 } from 'lucide-react'

interface Position {
  symbol: string
  exchange: string
  side: 'long' | 'short'
  amount: number
  entryPrice: number
  currentPrice: number
  pnl: number
  pnlPercentage: number
  value: number
}

interface ExchangeBalance {
  exchange: string
  totalValue: number
  availableBalance: number
  inPositions: number
  currencies: { [key: string]: number }
}

export default function MultiExchangePortfolio() {
  const [positions, setPositions] = useState<Position[]>([])
  const [balances, setBalances] = useState<ExchangeBalance[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date())

  // Mock data (in real app, this would fetch from API)
  useEffect(() => {
    loadPortfolioData()
    const interval = setInterval(loadPortfolioData, 30000) // Update every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const loadPortfolioData = async () => {
    setIsLoading(true)
    try {
      // Mock positions data
      const mockPositions: Position[] = [
        {
          symbol: 'BTC/USDT',
          exchange: 'binance',
          side: 'long',
          amount: 0.1,
          entryPrice: 44500,
          currentPrice: 45200,
          pnl: 70,
          pnlPercentage: 1.57,
          value: 4520
        },
        {
          symbol: 'ETH/USDT',
          exchange: 'bybit',
          side: 'long',
          amount: 2.5,
          entryPrice: 2800,
          currentPrice: 2850,
          pnl: 125,
          pnlPercentage: 1.79,
          value: 7125
        },
        {
          symbol: 'SOL/USDT',
          exchange: 'delta',
          side: 'short',
          amount: 10,
          entryPrice: 95,
          currentPrice: 92,
          pnl: 30,
          pnlPercentage: 3.16,
          value: 920
        }
      ]

      // Mock balance data
      const mockBalances: ExchangeBalance[] = [
        {
          exchange: 'binance',
          totalValue: 5200,
          availableBalance: 680,
          inPositions: 4520,
          currencies: { USDT: 680, BTC: 0.1 }
        },
        {
          exchange: 'bybit',
          totalValue: 7500,
          availableBalance: 375,
          inPositions: 7125,
          currencies: { USDT: 375, ETH: 2.5 }
        },
        {
          exchange: 'delta',
          totalValue: 1200,
          availableBalance: 280,
          inPositions: 920,
          currencies: { INR: 25000, SOL: 10 }
        }
      ]

      setPositions(mockPositions)
      setBalances(mockBalances)
      setLastUpdate(new Date())
    } catch (error) {
      console.error('Error loading portfolio data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const getTotalPortfolioValue = () => {
    return balances.reduce((total, balance) => total + balance.totalValue, 0)
  }

  const getTotalPnL = () => {
    return positions.reduce((total, position) => total + position.pnl, 0)
  }

  const getTotalPnLPercentage = () => {
    const totalValue = getTotalPortfolioValue()
    const totalPnL = getTotalPnL()
    return totalValue > 0 ? (totalPnL / totalValue) * 100 : 0
  }

  const getExchangeBadge = (exchange: string) => {
    const colors = {
      binance: 'bg-yellow-100 text-yellow-800',
      bybit: 'bg-blue-100 text-blue-800',
      delta: 'bg-green-100 text-green-800',
      gate: 'bg-purple-100 text-purple-800',
      bitget: 'bg-red-100 text-red-800'
    }
    return colors[exchange as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  return (
    <div className="space-y-6">
      {/* Portfolio Overview */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Wallet className="h-5 w-5" />
                Multi-Exchange Portfolio
              </CardTitle>
              <CardDescription>
                Consolidated view of positions across all configured exchanges
              </CardDescription>
            </div>
            <Button 
              variant="outline" 
              size="sm" 
              onClick={loadPortfolioData}
              disabled={isLoading}
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-4">
            <div className="text-center">
              <div className="text-2xl font-bold">${getTotalPortfolioValue().toLocaleString()}</div>
              <div className="text-sm text-gray-600">Total Value</div>
            </div>
            <div className="text-center">
              <div className={`text-2xl font-bold ${getTotalPnL() >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                ${getTotalPnL().toFixed(2)}
              </div>
              <div className="text-sm text-gray-600">Total P&L</div>
            </div>
            <div className="text-center">
              <div className={`text-2xl font-bold ${getTotalPnLPercentage() >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {getTotalPnLPercentage() >= 0 ? '+' : ''}{getTotalPnLPercentage().toFixed(2)}%
              </div>
              <div className="text-sm text-gray-600">Total Return</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{positions.length}</div>
              <div className="text-sm text-gray-600">Open Positions</div>
            </div>
          </div>
          <div className="mt-4 text-xs text-gray-500">
            Last updated: {lastUpdate.toLocaleTimeString()}
          </div>
        </CardContent>
      </Card>

      {/* Detailed Views */}
      <Tabs defaultValue="positions" className="space-y-4">
        <TabsList>
          <TabsTrigger value="positions">Open Positions</TabsTrigger>
          <TabsTrigger value="balances">Exchange Balances</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
        </TabsList>

        {/* Positions Tab */}
        <TabsContent value="positions">
          <Card>
            <CardHeader>
              <CardTitle>Open Positions</CardTitle>
              <CardDescription>All active positions across exchanges</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {positions.map((position, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center space-x-4">
                      <div>
                        <div className="font-medium">{position.symbol}</div>
                        <div className="flex items-center gap-2">
                          <Badge className={getExchangeBadge(position.exchange)}>
                            {position.exchange}
                          </Badge>
                          <Badge variant={position.side === 'long' ? 'default' : 'secondary'}>
                            {position.side.toUpperCase()}
                          </Badge>
                        </div>
                      </div>
                      <div className="text-sm text-gray-600">
                        <div>Amount: {position.amount}</div>
                        <div>Entry: ${position.entryPrice.toLocaleString()}</div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-medium">${position.value.toLocaleString()}</div>
                      <div className={`text-sm flex items-center gap-1 ${
                        position.pnl >= 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {position.pnl >= 0 ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                        ${position.pnl.toFixed(2)} ({position.pnlPercentage >= 0 ? '+' : ''}{position.pnlPercentage.toFixed(2)}%)
                      </div>
                    </div>
                  </div>
                ))}
                {positions.length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    No open positions found
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Balances Tab */}
        <TabsContent value="balances">
          <Card>
            <CardHeader>
              <CardTitle>Exchange Balances</CardTitle>
              <CardDescription>Available balances across all exchanges</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {balances.map((balance, index) => (
                  <div key={index} className="p-4 border rounded-lg">
                    <div className="flex items-center justify-between mb-3">
                      <Badge className={getExchangeBadge(balance.exchange)}>
                        {balance.exchange.toUpperCase()}
                      </Badge>
                      <div className="text-right">
                        <div className="font-medium">${balance.totalValue.toLocaleString()}</div>
                        <div className="text-sm text-gray-600">Total Value</div>
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <div className="text-gray-600">Available</div>
                        <div className="font-medium">${balance.availableBalance.toLocaleString()}</div>
                      </div>
                      <div>
                        <div className="text-gray-600">In Positions</div>
                        <div className="font-medium">${balance.inPositions.toLocaleString()}</div>
                      </div>
                    </div>
                    <div className="mt-3 pt-3 border-t">
                      <div className="text-xs text-gray-600 mb-2">Holdings:</div>
                      <div className="flex flex-wrap gap-2">
                        {Object.entries(balance.currencies).map(([currency, amount]) => (
                          <Badge key={currency} variant="outline" className="text-xs">
                            {amount} {currency}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Performance Tab */}
        <TabsContent value="performance">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Performance Analytics
              </CardTitle>
              <CardDescription>Portfolio performance metrics and analysis</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 md:grid-cols-2">
                <div className="space-y-4">
                  <h3 className="font-medium">Exchange Performance</h3>
                  {balances.map((balance, index) => {
                    const exchangePositions = positions.filter(p => p.exchange === balance.exchange)
                    const exchangePnL = exchangePositions.reduce((sum, p) => sum + p.pnl, 0)
                    const exchangePnLPercentage = balance.totalValue > 0 ? (exchangePnL / balance.totalValue) * 100 : 0
                    
                    return (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <Badge className={getExchangeBadge(balance.exchange)}>
                          {balance.exchange}
                        </Badge>
                        <div className="text-right">
                          <div className={`font-medium ${exchangePnL >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                            ${exchangePnL.toFixed(2)}
                          </div>
                          <div className="text-sm text-gray-600">
                            {exchangePnLPercentage >= 0 ? '+' : ''}{exchangePnLPercentage.toFixed(2)}%
                          </div>
                        </div>
                      </div>
                    )
                  })}
                </div>
                
                <div className="space-y-4">
                  <h3 className="font-medium">Asset Allocation</h3>
                  {positions.map((position, index) => {
                    const allocation = (position.value / getTotalPortfolioValue()) * 100
                    return (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div>
                          <div className="font-medium">{position.symbol}</div>
                          <div className="text-sm text-gray-600">{position.exchange}</div>
                        </div>
                        <div className="text-right">
                          <div className="font-medium">{allocation.toFixed(1)}%</div>
                          <div className="text-sm text-gray-600">${position.value.toLocaleString()}</div>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}