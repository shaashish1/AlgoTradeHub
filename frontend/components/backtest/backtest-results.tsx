import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  Percent, 
  Calendar,
  Download,
  BarChart3
} from 'lucide-react'

export interface BacktestResult {
  id: string
  strategy: string
  symbol: string
  timeframe: string
  startDate: string
  endDate: string
  initialCapital: number
  finalCapital: number
  totalReturn: number
  totalReturnPercent: number
  maxDrawdown: number
  sharpeRatio: number
  winRate: number
  totalTrades: number
  winningTrades: number
  losingTrades: number
  avgWin: number
  avgLoss: number
  profitFactor: number
  status: 'completed' | 'running' | 'failed'
}

interface BacktestResultsProps {
  results: BacktestResult[]
}

export function BacktestResults({ results }: BacktestResultsProps) {
  const exportResults = () => {
    const dataStr = JSON.stringify(results, null, 2)
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr)
    
    const exportFileDefaultName = `backtest_results_${new Date().toISOString().split('T')[0]}.json`
    
    const linkElement = document.createElement('a')
    linkElement.setAttribute('href', dataUri)
    linkElement.setAttribute('download', exportFileDefaultName)
    linkElement.click()
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return <Badge className="bg-green-100 text-green-800">✅ Completed</Badge>
      case 'running':
        return <Badge className="bg-blue-100 text-blue-800">🔄 Running</Badge>
      case 'failed':
        return <Badge className="bg-red-100 text-red-800">❌ Failed</Badge>
      default:
        return <Badge>Unknown</Badge>
    }
  }

  const getReturnColor = (returnPercent: number) => {
    return returnPercent >= 0 ? 'text-green-600' : 'text-red-600'
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5" />
              Backtest Results ({results.length})
            </CardTitle>
            <Button onClick={exportResults} variant="outline" size="sm">
              <Download className="h-4 w-4 mr-2" />
              Export Results
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {results.map((result) => (
              <div key={result.id} className="border rounded-lg p-4 space-y-4">
                {/* Header */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <h3 className="font-semibold">{result.strategy}</h3>
                    <Badge variant="outline">{result.symbol}</Badge>
                    <Badge variant="outline">{result.timeframe}</Badge>
                  </div>
                  {getStatusBadge(result.status)}
                </div>

                {/* Key Metrics */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className={`text-2xl font-bold ${getReturnColor(result.totalReturnPercent)}`}>
                      {result.totalReturnPercent >= 0 ? '+' : ''}{result.totalReturnPercent.toFixed(2)}%
                    </div>
                    <div className="text-sm text-gray-600">Total Return</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold">${result.finalCapital.toLocaleString()}</div>
                    <div className="text-sm text-gray-600">Final Capital</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-red-600">
                      -{result.maxDrawdown.toFixed(2)}%
                    </div>
                    <div className="text-sm text-gray-600">Max Drawdown</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold">{result.sharpeRatio.toFixed(2)}</div>
                    <div className="text-sm text-gray-600">Sharpe Ratio</div>
                  </div>
                </div>

                {/* Trading Statistics */}
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4 pt-4 border-t">
                  <div className="text-center">
                    <div className="text-lg font-semibold">{result.totalTrades}</div>
                    <div className="text-sm text-gray-600">Total Trades</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-semibold text-green-600">{result.winningTrades}</div>
                    <div className="text-sm text-gray-600">Winning</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-semibold text-red-600">{result.losingTrades}</div>
                    <div className="text-sm text-gray-600">Losing</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-semibold">{result.winRate.toFixed(1)}%</div>
                    <div className="text-sm text-gray-600">Win Rate</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-semibold">{result.profitFactor.toFixed(2)}</div>
                    <div className="text-sm text-gray-600">Profit Factor</div>
                  </div>
                </div>

                {/* Period */}
                <div className="flex items-center gap-2 text-sm text-gray-600 pt-2 border-t">
                  <Calendar className="h-4 w-4" />
                  <span>{result.startDate} to {result.endDate}</span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}