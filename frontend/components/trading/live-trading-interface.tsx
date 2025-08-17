'use client'
import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { AlertCircle, TrendingUp, TrendingDown, DollarSign, Activity } from 'lucide-react'
import { apiClient } from '@/lib/api'

interface TradingPair {
  symbol: string
  price: number
  change24h: number
  volume: number
}

interface OrderData {
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

export default function LiveTradingInterface() {
  const [selectedExchange, setSelectedExchange] = useState<string>('')
  const [selectedPair, setSelectedPair] = useState<string>('')
  const [orderData, setOrderData] = useState<OrderData>({
    symbol: '',
    side: 'buy',
    type: 'market',
    amount: 0,
    exchange: ''
  })
  const [tradingPairs, setTradingPairs] = useState<TradingPair[]>([])
  const [orderResult, setOrderResult] = useState<OrderResult | null>(null)
  const [isExecuting, setIsExecuting] = useState(false)
  const [balance, setBalance] = useState<any>({})

  // Mock trading pairs (in real app, fetch from API)
  useEffect(() => {
    const mockPairs: TradingPair[] = [
      { symbol: 'BTC/USDT', price: 43250.50, change24h: 2.45, volume: 1250000 },
      { symbol: 'ETH/USDT', price: 2650.75, change24h: -1.23, volume: 850000 },
      { symbol: 'BNB/USDT', price: 315.20, change24h: 0.85, volume: 420000 },
      { symbol: 'ADA/USDT', price: 0.485, change24h: 3.12, volume: 180000 },
      { symbol: 'SOL/USDT', price: 98.45, change24h: -0.67, volume: 320000 }
    ]
    setTradingPairs(mockPairs)
  }, [])

  const handlePairSelect = (symbol: string) => {
    setSelectedPair(symbol)
    setOrderData(prev => ({ ...prev, symbol }))
  }

  const handleExecuteOrder = async () => {
    if (!selectedExchange || !orderData.symbol || !orderData.amount) {
      setOrderResult({
        success: false,
        message: 'Please fill all required fields'
      })
      return
    }

    setIsExecuting(true)
    setOrderResult(null)

    try {
      const result = await apiClient.executeOrder({
        ...orderData,
        exchange: selectedExchange
      })

      if (result.success) {
        const data = result.data as any
        setOrderResult({
          success: true,
          orderId: data?.orderId || 'DEMO_' + Date.now(),
          message: `Order executed successfully on ${selectedExchange}`,
          executedPrice: data?.executedPrice || tradingPairs.find(p => p.symbol === orderData.symbol)?.price,
          executedAmount: orderData.amount
        })
        // Refresh balance after successful order
        fetchBalance()
      } else {
        setOrderResult({
          success: false,
          message: result.error || 'Order execution failed'
        })
      }
    } catch (error) {
      setOrderResult({
        success: false,
        message: 'Network error: Unable to execute order'
      })
    } finally {
      setIsExecuting(false)
    }
  }

  const fetchBalance = async () => {
    if (!selectedExchange) return
    
    try {
      const result = await apiClient.getTradingBalance(selectedExchange)
      if (result.success) {
        setBalance(result.data || {})
      }
    } catch (error) {
      console.error('Failed to fetch balance:', error)
    }
  }

  const selectedPairData = tradingPairs.find(p => p.symbol === selectedPair)

  return (
    <div className="space-y-6">
      {/* Exchange Selection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-5 w-5" />
            Live Trading
          </CardTitle>
          <CardDescription>
            Execute real trades on your configured exchanges
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Exchange</Label>
              <Select value={selectedExchange} onValueChange={setSelectedExchange}>
                <SelectTrigger>
                  <SelectValue placeholder="Select exchange..." />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="binance">Binance</SelectItem>
                  <SelectItem value="bybit">Bybit</SelectItem>
                  <SelectItem value="delta">Delta Exchange</SelectItem>
                  <SelectItem value="gate">Gate.io</SelectItem>
                  <SelectItem value="bitget">Bitget</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Trading Pair</Label>
              <Select value={selectedPair} onValueChange={handlePairSelect}>
                <SelectTrigger>
                  <SelectValue placeholder="Select pair..." />
                </SelectTrigger>
                <SelectContent>
                  {tradingPairs.map((pair) => (
                    <SelectItem key={pair.symbol} value={pair.symbol}>
                      <div className="flex items-center justify-between w-full">
                        <span>{pair.symbol}</span>
                        <span className="text-sm text-gray-500 ml-2">
                          ${pair.price.toLocaleString()}
                        </span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Market Data */}
      {selectedPairData && (
        <Card>
          <CardHeader>
            <CardTitle>{selectedPairData.symbol}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold">${selectedPairData.price.toLocaleString()}</div>
                <div className="text-sm text-gray-600">Current Price</div>
              </div>
              <div className="text-center">
                <div className={`text-2xl font-bold flex items-center justify-center gap-1 ${
                  selectedPairData.change24h >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  {selectedPairData.change24h >= 0 ? 
                    <TrendingUp className="h-5 w-5" /> : 
                    <TrendingDown className="h-5 w-5" />
                  }
                  {selectedPairData.change24h.toFixed(2)}%
                </div>
                <div className="text-sm text-gray-600">24h Change</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">${selectedPairData.volume.toLocaleString()}</div>
                <div className="text-sm text-gray-600">24h Volume</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Order Form */}
      <Card>
        <CardHeader>
          <CardTitle>Place Order</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Order Side</Label>
              <Select 
                value={orderData.side} 
                onValueChange={(value: 'buy' | 'sell') => setOrderData(prev => ({ ...prev, side: value }))}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="buy">
                    <span className="text-green-600">Buy</span>
                  </SelectItem>
                  <SelectItem value="sell">
                    <span className="text-red-600">Sell</span>
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Order Type</Label>
              <Select 
                value={orderData.type} 
                onValueChange={(value: 'market' | 'limit') => setOrderData(prev => ({ ...prev, type: value }))}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="market">Market</SelectItem>
                  <SelectItem value="limit">Limit</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Amount</Label>
              <Input
                type="number"
                step="0.00001"
                placeholder="0.00"
                value={orderData.amount || ''}
                onChange={(e) => setOrderData(prev => ({ ...prev, amount: parseFloat(e.target.value) || 0 }))}
              />
            </div>
            {orderData.type === 'limit' && (
              <div>
                <Label>Price</Label>
                <Input
                  type="number"
                  step="0.01"
                  placeholder="0.00"
                  value={orderData.price || ''}
                  onChange={(e) => setOrderData(prev => ({ ...prev, price: parseFloat(e.target.value) || 0 }))}
                />
              </div>
            )}
          </div>

          <Button 
            onClick={handleExecuteOrder}
            disabled={isExecuting || !selectedExchange || !orderData.symbol || !orderData.amount}
            className={`w-full ${orderData.side === 'buy' ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700'}`}
          >
            {isExecuting ? 'Executing...' : `${orderData.side.toUpperCase()} ${orderData.symbol}`}
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
                    <div>Executed at: ${orderResult.executedPrice.toLocaleString()}</div>
                  )}
                  {orderResult.executedAmount && (
                    <div>Amount: {orderResult.executedAmount}</div>
                  )}
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Balance Display */}
      {Object.keys(balance).length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Account Balance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(balance).slice(0, 8).map(([currency, amount]: [string, any]) => (
                <div key={currency} className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="font-semibold">{currency}</div>
                  <div className="text-sm text-gray-600">
                    {typeof amount === 'object' ? amount.free || '0' : amount}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}