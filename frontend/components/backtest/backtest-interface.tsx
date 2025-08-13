"use client"

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  Play, 
  BarChart3, 
  Settings, 
  TrendingUp,
  Calendar,
  DollarSign,
  Target,
  Rocket
} from 'lucide-react'
import { formatCurrency, formatPercentage } from '@/lib/utils'

interface BacktestResult {
  totalReturn: number
  sharpeRatio: number
  maxDrawdown: number
  winRate: number
  totalTrades: number
  finalPortfolio: number
}

export function BacktestInterface() {
  const [isRunning, setIsRunning] = useState(false)
  const [progress, setProgress] = useState(0)
  const [results, setResults] = useState<BacktestResult | null>(null)
  const [config, setConfig] = useState({
    symbol: 'BTC/USDT',
    strategy: 'rsi_strategy',
    startDate: '2023-01-01',
    endDate: '2024-01-01',
    initialCapital: 10000,
    commission: 0.001
  })

  const strategies = [
    { value: 'rsi_strategy', label: 'RSI Strategy' },
    { value: 'macd_strategy', label: 'MACD Strategy' },
    { value: 'bollinger_strategy', label: 'Bollinger Bands' },
    { value: 'multi_indicator_strategy', label: 'Multi-Indicator' },
    { value: 'sma_crossover_strategy', label: 'SMA Crossover' }
  ]

  const symbols = [
    'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'SOL/USDT',
    'DOT/USDT', 'MATIC/USDT', 'AVAX/USDT', 'LINK/USDT', 'UNI/USDT'
  ]

  const runBacktest = async () => {
    setIsRunning(true)
    setProgress(0)
    setResults(null)

    // Simulate backtest progress
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval)
          return 100
        }
        return prev + Math.random() * 10
      })
    }, 200)

    // Simulate API call to backend
    try {
      // This would be replaced with actual API call
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      // Mock results
      const mockResults: BacktestResult = {
        totalReturn: Math.random() * 50 - 10, // -10% to 40%
        sharpeRatio: Math.random() * 2 + 0.5, // 0.5 to 2.5
        maxDrawdown: Math.random() * -20, // 0% to -20%
        winRate: Math.random() * 40 + 40, // 40% to 80%
        totalTrades: Math.floor(Math.random() * 200) + 50, // 50 to 250
        finalPortfolio: config.initialCapital * (1 + (Math.random() * 50 - 10) / 100)
      }
      
      setResults(mockResults)
    } catch (error) {
      console.error('Backtest failed:', error)
    } finally {
      setIsRunning(false)
      clearInterval(progressInterval)
    }
  }

  const handleConfigChange = (key: string, value: string | number) => {
    setConfig(prev => ({ ...prev, [key]: value }))
  }

  return (
    <div className="grid gap-6 lg:grid-cols-3">
      {/* Configuration Panel */}
      <div className="space-y-6 lg:col-span-1">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Settings className="h-5 w-5" />
              <span>Configuration</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Strategy Selection */}
            <div className="space-y-2">
              <Label htmlFor="strategy">Strategy</Label>
              <select
                id="strategy"
                className="w-full p-2 border rounded-md"
                value={config.strategy}
                onChange={(e) => handleConfigChange('strategy', e.target.value)}
              >
                {strategies.map((strategy) => (
                  <option key={strategy.value} value={strategy.value}>
                    {strategy.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Symbol Selection */}
            <div className="space-y-2">
              <Label htmlFor="symbol">Trading Pair</Label>
              <select
                id="symbol"
                className="w-full p-2 border rounded-md"
                value={config.symbol}
                onChange={(e) => handleConfigChange('symbol', e.target.value)}
              >
                {symbols.map((symbol) => (
                  <option key={symbol} value={symbol}>
                    {symbol}
                  </option>
                ))}
              </select>
            </div>

            {/* Date Range */}
            <div className="grid grid-cols-2 gap-2">
              <div className="space-y-2">
                <Label htmlFor="startDate">Start Date</Label>
                <Input
                  id="startDate"
                  type="date"
                  value={config.startDate}
                  onChange={(e) => handleConfigChange('startDate', e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="endDate">End Date</Label>
                <Input
                  id="endDate"
                  type="date"
                  value={config.endDate}
                  onChange={(e) => handleConfigChange('endDate', e.target.value)}
                />
              </div>
            </div>

            {/* Capital and Commission */}
            <div className="space-y-2">
              <Label htmlFor="capital">Initial Capital ($)</Label>
              <Input
                id="capital"
                type="number"
                value={config.initialCapital}
                onChange={(e) => handleConfigChange('initialCapital', parseFloat(e.target.value))}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="commission">Commission (%)</Label>
              <Input
                id="commission"
                type="number"
                step="0.001"
                value={config.commission}
                onChange={(e) => handleConfigChange('commission', parseFloat(e.target.value))}
              />
            </div>

            {/* Run Button */}
            <Button 
              className="w-full" 
              onClick={runBacktest}
              disabled={isRunning}
            >
              {isRunning ? (
                <>
                  <BarChart3 className="h-4 w-4 mr-2 animate-spin" />
                  Running...
                </>
              ) : (
                <>
                  <Rocket className="h-4 w-4 mr-2" />
                  Run Backtest
                </>
              )}
            </Button>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Button variant="outline" className="w-full justify-start">
              <Target className="h-4 w-4 mr-2" />
              Comprehensive Suite
            </Button>
            <Button variant="outline" className="w-full justify-start">
              <TrendingUp className="h-4 w-4 mr-2" />
              Strategy Comparison
            </Button>
            <Button variant="outline" className="w-full justify-start">
              <Calendar className="h-4 w-4 mr-2" />
              Historical Analysis
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Results Panel */}
      <div className="space-y-6 lg:col-span-2">
        {/* Progress */}
        {isRunning && (
          <Card>
            <CardHeader>
              <CardTitle>Running Backtest</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Progress</span>
                  <span>{Math.round(progress)}%</span>
                </div>
                <Progress value={progress} className="h-2" />
                <p className="text-sm text-muted-foreground">
                  Testing {config.strategy.replace('_', ' ')} on {config.symbol}...
                </p>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Results */}
        {results && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="h-5 w-5" />
                <span>Backtest Results</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <div className="space-y-2">
                  <p className="text-sm text-muted-foreground">Total Return</p>
                  <p className={`text-2xl font-bold ${results.totalReturn >= 0 ? 'text-success' : 'text-danger'}`}>
                    {formatPercentage(results.totalReturn)}
                  </p>
                </div>
                
                <div className="space-y-2">
                  <p className="text-sm text-muted-foreground">Sharpe Ratio</p>
                  <p className="text-2xl font-bold">
                    {results.sharpeRatio.toFixed(2)}
                  </p>
                </div>
                
                <div className="space-y-2">
                  <p className="text-sm text-muted-foreground">Max Drawdown</p>
                  <p className="text-2xl font-bold text-danger">
                    {formatPercentage(results.maxDrawdown)}
                  </p>
                </div>
                
                <div className="space-y-2">
                  <p className="text-sm text-muted-foreground">Win Rate</p>
                  <p className="text-2xl font-bold">
                    {results.winRate.toFixed(1)}%
                  </p>
                </div>
                
                <div className="space-y-2">
                  <p className="text-sm text-muted-foreground">Total Trades</p>
                  <p className="text-2xl font-bold">
                    {results.totalTrades}
                  </p>
                </div>
                
                <div className="space-y-2">
                  <p className="text-sm text-muted-foreground">Final Portfolio</p>
                  <p className="text-2xl font-bold">
                    {formatCurrency(results.finalPortfolio)}
                  </p>
                </div>
              </div>

              <div className="mt-6 pt-6 border-t">
                <div className="flex justify-between items-center">
                  <span className="font-medium">Performance Summary</span>
                  <Badge variant={results.totalReturn >= 0 ? "success" : "destructive"}>
                    {results.totalReturn >= 0 ? 'Profitable' : 'Loss'}
                  </Badge>
                </div>
                <p className="text-sm text-muted-foreground mt-2">
                  Strategy: {config.strategy.replace('_', ' ')} • 
                  Symbol: {config.symbol} • 
                  Period: {config.startDate} to {config.endDate}
                </p>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Default State */}
        {!isRunning && !results && (
          <Card>
            <CardContent className="pt-6">
              <div className="text-center py-12">
                <BarChart3 className="h-16 w-16 mx-auto mb-4 text-muted-foreground opacity-50" />
                <h3 className="text-lg font-medium mb-2">Ready to Backtest</h3>
                <p className="text-muted-foreground mb-4">
                  Configure your strategy parameters and click "Run Backtest" to see results
                </p>
                <Button onClick={runBacktest}>
                  <Rocket className="h-4 w-4 mr-2" />
                  Start Your First Backtest
                </Button>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}