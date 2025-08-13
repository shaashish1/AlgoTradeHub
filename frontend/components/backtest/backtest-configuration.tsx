"use client"

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { 
  Brain, 
  Clock, 
  DollarSign, 
  Calendar, 
  Settings2, 
  Target,
  Rocket,
  BarChart3
} from 'lucide-react'
import { api, BacktestConfig } from '@/lib/api'

const strategies = [
  'RSI Strategy',
  'MACD',
  'Bollinger Bands',
  'Multi-Indicator',
  'SMA Crossover',
  'EMA Strategy',
  'Momentum',
  'Volume Breakout',
  'Stochastic'
]

const timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d']

const assets = [
  'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'ADA/USDT', 'DOT/USDT',
  'MATIC/USDT', 'AVAX/USDT', 'LINK/USDT', 'UNI/USDT', 'ATOM/USDT'
]

interface BacktestConfigurationProps {
  onStartBacktest?: (config: any) => void
}

export function BacktestConfiguration({ onStartBacktest }: BacktestConfigurationProps) {
  const [selectedStrategies, setSelectedStrategies] = useState<string[]>(['RSI Strategy', 'MACD', 'Bollinger Bands'])
  const [selectedTimeframes, setSelectedTimeframes] = useState<string[]>(['1h', '4h', '1d'])
  const [selectedAssets, setSelectedAssets] = useState<string[]>(['BTC/USDT', 'ETH/USDT', 'SOL/USDT'])
  const [useMaxData, setUseMaxData] = useState(true)
  const [parallelExec, setParallelExec] = useState(true)
  const [saveResults, setSaveResults] = useState(true)
  const [isRunning, setIsRunning] = useState(false)
  const [initialCapital, setInitialCapital] = useState(10000)
  const [commission, setCommission] = useState(0.1)
  const [startDate, setStartDate] = useState('2022-01-01')
  const [endDate, setEndDate] = useState('2024-12-31')

  const totalTests = selectedStrategies.length * selectedTimeframes.length * selectedAssets.length
  const estimatedTime = Math.ceil(totalTests * 0.5) // 0.5 minutes per test

  const handleStartBacktest = async () => {
    if (totalTests === 0) return
    
    setIsRunning(true)
    
    try {
      const config = {
        strategies: selectedStrategies,
        timeframes: selectedTimeframes,
        assets: selectedAssets,
        startDate: useMaxData ? '2020-01-01' : startDate,
        endDate: useMaxData ? new Date().toISOString().split('T')[0] : endDate,
        initialCapital,
        commission: commission / 100,
        parallelExecution: parallelExec,
        saveResults
      }
      
      if (onStartBacktest) {
        onStartBacktest(config)
      } else {
        // Run individual backtests for each combination
        for (const strategy of selectedStrategies) {
          for (const asset of selectedAssets) {
            const backtestConfig: BacktestConfig = {
              symbol: asset,
              strategy,
              startDate: config.startDate,
              endDate: config.endDate,
              initialCapital,
              commission: commission / 100
            }
            
            await api.runBacktest(backtestConfig)
          }
        }
      }
    } catch (error) {
      console.error('Backtest failed:', error)
    } finally {
      setIsRunning(false)
    }
  }

  const handleStrategyToggle = (strategy: string) => {
    setSelectedStrategies(prev => 
      prev.includes(strategy) 
        ? prev.filter(s => s !== strategy)
        : [...prev, strategy]
    )
  }

  const handleTimeframeToggle = (timeframe: string) => {
    setSelectedTimeframes(prev => 
      prev.includes(timeframe) 
        ? prev.filter(t => t !== timeframe)
        : [...prev, timeframe]
    )
  }

  const handleAssetToggle = (asset: string) => {
    setSelectedAssets(prev => 
      prev.includes(asset) 
        ? prev.filter(a => a !== asset)
        : [...prev, asset]
    )
  }

  const selectAllStrategies = () => setSelectedStrategies([...strategies])
  const clearAllStrategies = () => setSelectedStrategies([])
  
  const selectAllTimeframes = () => setSelectedTimeframes([...timeframes])
  const clearAllTimeframes = () => setSelectedTimeframes([])
  
  const selectAllAssets = () => setSelectedAssets([...assets])
  const clearAllAssets = () => setSelectedAssets([])

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Settings2 className="h-5 w-5" />
          <span>⚙️ Configuration Panel</span>
        </CardTitle>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Selection Grid */}
        <div className="grid gap-6 lg:grid-cols-3">
          {/* Strategies */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-lg flex items-center space-x-2">
                <Brain className="h-4 w-4" />
                <span>🧠 Strategies</span>
                <Badge variant="secondary">{selectedStrategies.length}</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {strategies.map((strategy) => (
                  <div key={strategy} className="flex items-center space-x-2">
                    <Checkbox
                      id={strategy}
                      checked={selectedStrategies.includes(strategy)}
                      onCheckedChange={() => handleStrategyToggle(strategy)}
                    />
                    <Label htmlFor={strategy} className="text-sm cursor-pointer">
                      {strategy}
                    </Label>
                  </div>
                ))}
              </div>
              <div className="flex space-x-2 pt-2 border-t">
                <Button variant="outline" size="sm" onClick={selectAllStrategies}>
                  Select All
                </Button>
                <Button variant="outline" size="sm" onClick={clearAllStrategies}>
                  Clear All
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Timeframes */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-lg flex items-center space-x-2">
                <Clock className="h-4 w-4" />
                <span>⏰ Timeframes</span>
                <Badge variant="secondary">{selectedTimeframes.length}</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="grid grid-cols-2 gap-2">
                {timeframes.map((timeframe) => (
                  <div key={timeframe} className="flex items-center space-x-2">
                    <Checkbox
                      id={timeframe}
                      checked={selectedTimeframes.includes(timeframe)}
                      onCheckedChange={() => handleTimeframeToggle(timeframe)}
                    />
                    <Label htmlFor={timeframe} className="text-sm cursor-pointer">
                      {timeframe}
                    </Label>
                  </div>
                ))}
              </div>
              <div className="flex space-x-2 pt-2 border-t">
                <Button variant="outline" size="sm" onClick={selectAllTimeframes}>
                  Select All
                </Button>
                <Button variant="outline" size="sm" onClick={clearAllTimeframes}>
                  Clear All
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Assets */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-lg flex items-center space-x-2">
                <DollarSign className="h-4 w-4" />
                <span>💰 Assets</span>
                <Badge variant="secondary">{selectedAssets.length}</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {assets.map((asset) => (
                  <div key={asset} className="flex items-center space-x-2">
                    <Checkbox
                      id={asset}
                      checked={selectedAssets.includes(asset)}
                      onCheckedChange={() => handleAssetToggle(asset)}
                    />
                    <Label htmlFor={asset} className="text-sm cursor-pointer">
                      {asset}
                    </Label>
                  </div>
                ))}
              </div>
              <div className="flex space-x-2 pt-2 border-t">
                <Button variant="outline" size="sm" onClick={selectAllAssets}>
                  Select All
                </Button>
                <Button variant="outline" size="sm" onClick={clearAllAssets}>
                  Clear All
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Parameters Grid */}
        <div className="grid gap-6 lg:grid-cols-3">
          {/* Date Range */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-lg flex items-center space-x-2">
                <Calendar className="h-4 w-4" />
                <span>📅 Date Range</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="space-y-2">
                <Label htmlFor="start-date">From:</Label>
                <Input
                  id="start-date"
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  disabled={useMaxData}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="end-date">To:</Label>
                <Input
                  id="end-date"
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  disabled={useMaxData}
                />
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="max-data"
                  checked={useMaxData}
                  onCheckedChange={(checked) => setUseMaxData(checked === true)}
                />
                <Label htmlFor="max-data" className="text-sm">
                  Use Max Data
                </Label>
              </div>
              <Button variant="outline" size="sm" className="w-full">
                <BarChart3 className="h-4 w-4 mr-2" />
                Data Check
              </Button>
            </CardContent>
          </Card>

          {/* Parameters */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-lg flex items-center space-x-2">
                <Settings2 className="h-4 w-4" />
                <span>💵 Parameters</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="space-y-2">
                <Label htmlFor="initial-capital">Initial Capital ($):</Label>
                <Input
                  id="initial-capital"
                  type="number"
                  value={initialCapital}
                  onChange={(e) => setInitialCapital(Number(e.target.value))}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="commission">Commission (%):</Label>
                <Input
                  id="commission"
                  type="number"
                  step="0.001"
                  value={commission}
                  onChange={(e) => setCommission(Number(e.target.value))}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="slippage">Slippage (%):</Label>
                <Input
                  id="slippage"
                  type="number"
                  step="0.001"
                  defaultValue="0.05"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="risk">Risk per Trade (%):</Label>
                <Input
                  id="risk"
                  type="number"
                  step="0.1"
                  defaultValue="2"
                />
              </div>
            </CardContent>
          </Card>

          {/* Options */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-lg flex items-center space-x-2">
                <Target className="h-4 w-4" />
                <span>🎯 Options</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="parallel-exec"
                    checked={parallelExec}
                    onCheckedChange={(checked) => setParallelExec(checked === true)}
                  />
                  <Label htmlFor="parallel-exec" className="text-sm">
                    Parallel Execution
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="save-results"
                    checked={saveResults}
                    onCheckedChange={(checked) => setSaveResults(checked === true)}
                  />
                  <Label htmlFor="save-results" className="text-sm">
                    Save Results
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox id="generate-pdf" />
                  <Label htmlFor="generate-pdf" className="text-sm">
                    Generate PDF
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox id="email-report" />
                  <Label htmlFor="email-report" className="text-sm">
                    Email Report
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox id="compare-mode" />
                  <Label htmlFor="compare-mode" className="text-sm">
                    Compare Mode
                  </Label>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Launch Section */}
        <Card className="bg-gradient-to-r from-primary/5 to-transparent border-primary/20">
          <CardContent className="pt-6">
            <div className="text-center space-y-4">
              <div className="space-y-2">
                <h3 className="text-xl font-bold">Ready to Launch</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                  <div className="space-y-1">
                    <p className="text-muted-foreground">Estimated Time:</p>
                    <p className="font-medium">{estimatedTime} minutes</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-muted-foreground">Total Tests:</p>
                    <p className="font-medium">{totalTests.toLocaleString()} combinations</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-muted-foreground">Memory Required:</p>
                    <p className="font-medium">~2.5GB</p>
                  </div>
                </div>
              </div>
              
              <Button 
                size="lg" 
                className="font-medium px-8"
                disabled={totalTests === 0 || isRunning}
                onClick={handleStartBacktest}
              >
                <Rocket className="h-5 w-5 mr-2" />
                {isRunning ? '⏳ Running...' : '🚀 Start Backtesting'}
              </Button>
              
              {totalTests === 0 && (
                <p className="text-sm text-muted-foreground">
                  Please select at least one strategy, timeframe, and asset to continue
                </p>
              )}
            </div>
          </CardContent>
        </Card>
      </CardContent>
    </Card>
  )
}