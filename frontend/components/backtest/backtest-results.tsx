"use client"

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Trophy, 
  TrendingUp, 
  BarChart3, 
  Download,
  Filter,
  RefreshCw,
  Save
} from 'lucide-react'

// Mock results data
const mockResults = [
  { rank: 1, strategy: 'MACD', asset: 'SOL/USDT', timeframe: '4h', return: 47.3, sharpe: 2.1, drawdown: -8.2, score: 95.2 },
  { rank: 2, strategy: 'RSI', asset: 'BTC/USDT', timeframe: '1d', return: 42.8, sharpe: 1.9, drawdown: -12.1, score: 91.7 },
  { rank: 3, strategy: 'Bollinger', asset: 'ETH/USDT', timeframe: '1h', return: 38.9, sharpe: 1.7, drawdown: -15.3, score: 87.4 },
  { rank: 4, strategy: 'Multi-Ind', asset: 'ADA/USDT', timeframe: '4h', return: 35.2, sharpe: 1.6, drawdown: -18.7, score: 84.1 },
  { rank: 5, strategy: 'SMA Cross', asset: 'DOT/USDT', timeframe: '1d', return: 32.1, sharpe: 1.5, drawdown: -14.2, score: 81.3 }
]

const strategyStats = [
  { strategy: 'MACD', avgReturn: 28.5, tests: 315 },
  { strategy: 'RSI', avgReturn: 26.8, tests: 315 },
  { strategy: 'Bollinger', avgReturn: 24.3, tests: 315 },
  { strategy: 'Multi-Ind', avgReturn: 22.1, tests: 315 },
  { strategy: 'SMA Cross', avgReturn: 20.9, tests: 315 }
]

export function BacktestResults() {
  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1: return '🥇'
      case 2: return '🥈'
      case 3: return '🥉'
      default: return `${rank}.`
    }
  }

  return (
    <div className="space-y-6">
      {/* Results Header */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center space-x-2">
              <Trophy className="h-5 w-5" />
              <span>📈 Comprehensive Results Analysis</span>
            </CardTitle>
            <div className="flex space-x-2">
              <Button variant="outline" size="sm">
                <Filter className="h-4 w-4 mr-2" />
                Filter
              </Button>
              <Button variant="outline" size="sm">
                <Download className="h-4 w-4 mr-2" />
                Export
              </Button>
              <Button variant="outline" size="sm">
                <Save className="h-4 w-4 mr-2" />
                Save
              </Button>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Top Performers */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Trophy className="h-5 w-5" />
            <span>🏆 Final Rankings</span>
          </CardTitle>
        </CardHeader>
        
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b text-sm text-muted-foreground">
                  <th className="text-left py-2">Rank</th>
                  <th className="text-left py-2">Strategy</th>
                  <th className="text-left py-2">Asset</th>
                  <th className="text-left py-2">TF</th>
                  <th className="text-right py-2">Return</th>
                  <th className="text-right py-2">Sharpe</th>
                  <th className="text-right py-2">Drawdown</th>
                  <th className="text-right py-2">Score</th>
                </tr>
              </thead>
              <tbody>
                {mockResults.map((result) => (
                  <tr key={result.rank} className="border-b hover:bg-muted/50">
                    <td className="py-3">
                      <div className="flex items-center space-x-2">
                        <span className="text-lg">{getRankIcon(result.rank)}</span>
                      </div>
                    </td>
                    <td className="py-3 font-medium">{result.strategy}</td>
                    <td className="py-3">{result.asset}</td>
                    <td className="py-3">
                      <Badge variant="outline" className="text-xs">
                        {result.timeframe}
                      </Badge>
                    </td>
                    <td className="text-right py-3 font-mono text-success">
                      +{result.return}%
                    </td>
                    <td className="text-right py-3 font-mono">
                      {result.sharpe}
                    </td>
                    <td className="text-right py-3 font-mono text-danger">
                      {result.drawdown}%
                    </td>
                    <td className="text-right py-3 font-mono font-bold">
                      {result.score}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          <div className="flex justify-center pt-4">
            <Button variant="outline">
              <BarChart3 className="h-4 w-4 mr-2" />
              View All 2,835 Results
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Analysis by Category */}
      <div className="grid gap-6 md:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center space-x-2">
              <TrendingUp className="h-4 w-4" />
              <span>🧠 By Strategy</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {strategyStats.map((stat, index) => (
              <div key={index} className="flex justify-between items-center">
                <span className="text-sm">{stat.strategy}:</span>
                <div className="text-right">
                  <div className="font-medium text-sm">{stat.avgReturn}% avg</div>
                  <div className="text-xs text-muted-foreground">({stat.tests} tests)</div>
                </div>
              </div>
            ))}
            <Button variant="outline" size="sm" className="w-full mt-3">
              <BarChart3 className="h-4 w-4 mr-2" />
              Details
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center space-x-2">
              <BarChart3 className="h-4 w-4" />
              <span>⏰ By Timeframe</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span>4h:</span>
              <span className="font-medium">31.2% avg</span>
            </div>
            <div className="flex justify-between">
              <span>1d:</span>
              <span className="font-medium">29.7% avg</span>
            </div>
            <div className="flex justify-between">
              <span>1h:</span>
              <span className="font-medium">25.8% avg</span>
            </div>
            <div className="flex justify-between">
              <span>30m:</span>
              <span className="font-medium">22.4% avg</span>
            </div>
            <div className="flex justify-between">
              <span>15m:</span>
              <span className="font-medium">19.8% avg</span>
            </div>
            <Button variant="outline" size="sm" className="w-full mt-3">
              <BarChart3 className="h-4 w-4 mr-2" />
              Details
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center space-x-2">
              <BarChart3 className="h-4 w-4" />
              <span>💰 By Asset</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span>SOL:</span>
              <span className="font-medium">35.1% avg</span>
            </div>
            <div className="flex justify-between">
              <span>BTC:</span>
              <span className="font-medium">32.4% avg</span>
            </div>
            <div className="flex justify-between">
              <span>ETH:</span>
              <span className="font-medium">28.9% avg</span>
            </div>
            <div className="flex justify-between">
              <span>ADA:</span>
              <span className="font-medium">26.7% avg</span>
            </div>
            <div className="flex justify-between">
              <span>DOT:</span>
              <span className="font-medium">24.2% avg</span>
            </div>
            <Button variant="outline" size="sm" className="w-full mt-3">
              <BarChart3 className="h-4 w-4 mr-2" />
              Details
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Key Insights */}
      <Card className="bg-gradient-to-r from-primary/5 to-transparent border-primary/20">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Trophy className="h-5 w-5" />
            <span>🎯 Key Insights & Recommendations</span>
          </CardTitle>
        </CardHeader>
        
        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-3">
              <div className="flex items-start space-x-2">
                <span className="text-lg">💡</span>
                <div>
                  <p className="font-medium">Best Overall:</p>
                  <p className="text-sm text-muted-foreground">
                    MACD strategy on SOL/USDT with 4h timeframe - Highest return with manageable drawdown
                  </p>
                </div>
              </div>
              
              <div className="flex items-start space-x-2">
                <span className="text-lg">💡</span>
                <div>
                  <p className="font-medium">Most Consistent:</p>
                  <p className="text-sm text-muted-foreground">
                    RSI strategy across multiple assets - Works well on BTC, ETH, and ADA
                  </p>
                </div>
              </div>
            </div>
            
            <div className="space-y-3">
              <div className="flex items-start space-x-2">
                <span className="text-lg">💡</span>
                <div>
                  <p className="font-medium">Timeframe Analysis:</p>
                  <p className="text-sm text-muted-foreground">
                    4h and 1d timeframes show best overall performance - Avoid 1m and 5m for most strategies
                  </p>
                </div>
              </div>
              
              <div className="flex items-start space-x-2">
                <span className="text-lg">⚠️</span>
                <div>
                  <p className="font-medium">Risk Warnings:</p>
                  <p className="text-sm text-muted-foreground">
                    Volume strategy shows high drawdowns on short timeframes
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="flex flex-wrap gap-3 pt-4 border-t">
            <Button>
              <BarChart3 className="h-4 w-4 mr-2" />
              Detailed Report
            </Button>
            <Button variant="outline">
              <RefreshCw className="h-4 w-4 mr-2" />
              Re-run with Optimizations
            </Button>
            <Button variant="outline">
              <Save className="h-4 w-4 mr-2" />
              Save Config
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}