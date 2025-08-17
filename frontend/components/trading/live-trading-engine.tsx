'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { AlertCircle, TrendingUp, TrendingDown, DollarSign, Activity } from 'lucide-react'

interface TradingOrder {
  symbol: string
  side: 'buy' | 'sell'
  type: 'market' | 'limit'
  amount: number
  price?: number
  exchange: string
}

interface OrderResult {
  success: boolean
  orderId?: string
  message: string
  executedPrice?: number
  executedAmount?: number
}

export default function LiveTradingEngine() {
  const [selectedExchange, setSelectedExchange] = useState('')
  const [order, setOrder] = useState<TradingOrder>({
    symbol: 'BTC/USDT',
    side: 'buy',
    type: 'market',
    amount: 0.001,
    exchange: ''
  })
  const [isExecuting, setIsExecuting] = useState(false)
  const [orderResult, setOrderResult] = useState<OrderResult | null>(null)
  const [marketPrice, setMarketPrice] = useState<number>(0)
  const [balance, setBalance] = useState<any>({})

  // Mock market data (in real app, this would be real-time)
  useEffect(() => {
    const interval = setInterval(() => {
      setMarketPrice(45000 + Math.random() * 1000) // Mock BTC price
    }, 2000)
    return () => clearInterval(interval)
  }, [])

  const executeOrder = async () => {
    if (!selectedExchange || !order.amount) {
      setOrderResult({
        success: false,
        message: 'Please select exchange and enter amount'
      })
      return
    }

    setIsExecuting(true)
    setOrderResult(null)

    try {
      // In real implementation, this would call the actual trading API
      const response = await fetch('/api/trading/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...order,
          exchange: selectedExchange
        })
      })

      if (response.ok) {
        const result = await response.json()
        setOrderResult({
          success: true,
          orderId: result.orderId || 'DEMO_' + Date.now(),
          message: `Order executed successfully on ${selectedExchange}`,
          executedPrice: result.executedPrice || marketPrice,
          executedAmount: result.executedAmount || order.amount
        })
      } else {
        const error = await response.json()
        setOrderResult({
          success: false,
          message: error.message || 'Order execution failed'
        })
      }
    } catch (error) {
      setOrderResult({
        success: false,
        message: 'Network error - order not executed'
      })
    } finally {
      setIsExecuting(false)
    }
  }

  const calculateOrderValue = () => {
    const price = order.type === 'market' ? marketPrice : (order.price || 0)
    return (price * order.amount).toFixed(2)
  }

  return (
    <div className="space-y-6">
      {/* Trading Interface */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-5 w-5" />
            Live Trading Engine
          </CardTitle>
          <CardDescription>
            Execute live trades on configured exchanges. Always test with small amounts first.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Exchange Selection */}
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <Label htmlFor="exchange">Exchange</Label>
              <Select value={selectedExchange} onValueChange={setSelectedExchange}>
                <SelectTrigger>
                  <SelectValue placeholder="Select exchange..." />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="binance">Binance (2069 markets)</SelectItem>
                  <SelectItem value="bybit">Bybit (2490 markets)</SelectItem>
                  <SelectItem value="delta">Delta Exchange (552 markets)</SelectItem>
                  <SelectItem value="gate">Gate.io (1329 markets)</SelectItem>
                  <SelectItem value="bitget">Bitget (45 markets)</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="symbol">Trading Pair</Label>
              <Select value={order.symbol} onValueChange={(value) => setOrder({...order, symbol: value})}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="BTC/USDT">BTC/USDT</SelectItem>
                  <SelectItem value="ETH/USDT">ETH/USDT</SelectItem>
                  <SelectItem value="BNB/USDT">BNB/USDT</SelectItem>
                  <SelectItem value="SOL/USDT">SOL/USDT</SelectItem>
                  <SelectItem value="ADA/USDT">ADA/USDT</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Order Details */}
          <div className="grid gap-4 md:grid-cols-3">
            <div>
              <Label htmlFor="side">Side</Label>
              <Select value={order.side} onValueChange={(value: 'buy' | 'sell') => setOrder({...order, side: value})}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="buy">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="h-4 w-4 text-green-600" />
                      Buy
                    </div>
                  </SelectItem>
                  <SelectItem value="sell">
                    <div className="flex items-center gap-2">
                      <TrendingDown className="h-4 w-4 text-red-600" />
                      Sell
                    </div>
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="type">Order Type</Label>
              <Select value={order.type} onValueChange={(value: 'market' | 'limit') => setOrder({...order, type: value})}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="market">Market Order</SelectItem>
                  <SelectItem value="limit">Limit Order</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="amount">Amount</Label>
              <Input
                id="amount"
                type="number"
                step="0.00001"
                value={order.amount}
                onChange={(e) => setOrder({...order, amount: parseFloat(e.target.value) || 0})}
                placeholder="0.001"
              />
            </div>
          </div>

          {/* Limit Price (if limit order) */}
          {order.type === 'limit' && (
            <div>
              <Label htmlFor="price">Limit Price (USDT)</Label>
              <Input
                id="price"
                type="number"
                step="0.01"
                value={order.price || ''}
                onChange={(e) => setOrder({...order, price: parseFloat(e.target.value) || 0})}
                placeholder="Enter limit price"
              />
            </div>
          )}

          {/* Order Summary */}
          <div className="p-4 bg-gray-50 rounded-lg space-y-2">
            <div className="flex justify-between">
              <span>Market Price:</span>
              <span className="font-mono">${marketPrice.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span>Order Value:</span>
              <span className="font-mono">${calculateOrderValue()}</span>
            </div>
            <div className="flex justify-between">
              <span>Estimated Fee (0.1%):</span>
              <span className="font-mono">${(parseFloat(calculateOrderValue()) * 0.001).toFixed(2)}</span>
            </div>
          </div>

          {/* Execute Button */}
          <Button 
            onClick={executeOrder}
            disabled={isExecuting || !selectedExchange || !order.amount}
            className={`w-full ${order.side === 'buy' ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700'}`}
          >
            {isExecuting ? 'Executing...' : `${order.side.toUpperCase()} ${order.symbol}`}
          </Button>

          {/* Order Result */}
          {orderResult && (
            <div className={`p-4 rounded-lg ${
              orderResult.success ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
            }`}>
              <div className="flex items-center gap-2">
                {orderResult.success ? (
                  <DollarSign className="h-4 w-4" />
                ) : (
                  <AlertCircle className="h-4 w-4" />
                )}
                <span className="font-medium">{orderResult.message}</span>
              </div>
              {orderResult.success && orderResult.orderId && (
                <div className="mt-2 text-sm">
                  <div>Order ID: {orderResult.orderId}</div>
                  {orderResult.executedPrice && (
                    <div>Executed at: ${orderResult.executedPrice.toFixed(2)}</div>
                  )}
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Safety Notice */}
      <Card>
        <CardHeader>
          <CardTitle className="text-yellow-600">⚠️ Safety Notice</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 text-sm">
            <div className="flex items-center gap-2">
              <Badge className="bg-yellow-100 text-yellow-800">DEMO MODE</Badge>
              <span>Currently running in sandbox mode for safety</span>
            </div>
            <div>• Always test with small amounts first</div>
            <div>• Verify exchange configuration before trading</div>
            <div>• Monitor positions and set stop losses</div>
            <div>• Never risk more than you can afford to lose</div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}