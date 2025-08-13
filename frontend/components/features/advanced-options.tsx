"use client"

import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Target, 
  TrendingUp, 
  BarChart3, 
  Search,
  Rocket,
  FileText,
  Video,
  Clock,
  Users,
  Zap
} from 'lucide-react'

export function AdvancedOptions() {
  return (
    <div className="space-y-6">
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-bold">🔧 ADVANCED OPTIONS</h2>
        <p className="text-muted-foreground">
          Powerful tools for comprehensive analysis and advanced trading strategies
        </p>
      </div>

      {/* Comprehensive Backtesting Suite - Featured */}
      <Card className="border-primary/50 bg-gradient-to-r from-primary/5 to-transparent">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="space-y-2">
              <CardTitle className="text-xl flex items-center space-x-2">
                <Target className="h-6 w-6 text-primary" />
                <span>A1: Comprehensive Backtesting Suite</span>
                <Badge variant="default" className="text-xs">Featured</Badge>
              </CardTitle>
              <CardDescription className="text-base">
                The ultimate backtesting solution with multi-dimensional analysis
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-3">
              <h4 className="font-medium">Key Features:</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-center space-x-2">
                  <BarChart3 className="h-4 w-4 text-primary" />
                  <span>Multi-timeframe analysis (1m to 1d)</span>
                </li>
                <li className="flex items-center space-x-2">
                  <Target className="h-4 w-4 text-primary" />
                  <span>Multi-strategy testing (9 built-in strategies)</span>
                </li>
                <li className="flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4 text-primary" />
                  <span>Multi-asset support (crypto & stocks)</span>
                </li>
                <li className="flex items-center space-x-2">
                  <Clock className="h-4 w-4 text-primary" />
                  <span>Maximum historical data usage</span>
                </li>
              </ul>
            </div>
            
            <div className="space-y-3">
              <h4 className="font-medium">Performance:</h4>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="space-y-1">
                  <p className="text-muted-foreground">Estimated Runtime:</p>
                  <p className="font-medium">15-20 minutes</p>
                </div>
                <div className="space-y-1">
                  <p className="text-muted-foreground">Total Tests:</p>
                  <p className="font-medium">2,835 combinations</p>
                </div>
                <div className="space-y-1">
                  <p className="text-muted-foreground">Memory Usage:</p>
                  <p className="font-medium">~2.5GB</p>
                </div>
                <div className="space-y-1">
                  <p className="text-muted-foreground">Parallel Workers:</p>
                  <p className="font-medium">4 threads</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="flex flex-wrap gap-3 pt-4 border-t">
            <Link href="/backtest/comprehensive">
              <Button size="lg" className="font-medium">
                <Rocket className="h-4 w-4 mr-2" />
                Launch Suite
              </Button>
            </Link>
            <Button variant="outline">
              <FileText className="h-4 w-4 mr-2" />
              Documentation
            </Button>
            <Button variant="outline">
              <Video className="h-4 w-4 mr-2" />
              Tutorial
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Other Advanced Options */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Strategy Performance Analysis */}
        <Card className="feature-card">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="h-5 w-5 text-primary" />
              <span>A2: Strategy Performance Analysis</span>
            </CardTitle>
            <CardDescription>
              Analyze which strategies work best for different assets and timeframes
            </CardDescription>
          </CardHeader>
          
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <h5 className="text-sm font-medium">Features:</h5>
              <ul className="text-xs text-muted-foreground space-y-1">
                <li>• Best strategy combinations</li>
                <li>• Asset-specific analysis</li>
                <li>• Timeframe optimization</li>
                <li>• Performance heatmaps</li>
              </ul>
            </div>
            
            <div className="flex items-center justify-between text-xs">
              <Badge variant="success">Ready</Badge>
              <span className="text-muted-foreground">~5 min runtime</span>
            </div>
            
            <div className="flex space-x-2">
              <Link href="/analysis/strategy-performance" className="flex-1">
                <Button variant="outline" className="w-full">
                  <Zap className="h-4 w-4 mr-2" />
                  Launch
                </Button>
              </Link>
              <Button variant="ghost" size="icon">
                <BarChart3 className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Market Data Analysis */}
        <Card className="feature-card">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <BarChart3 className="h-5 w-5 text-primary" />
              <span>A3: Market Data Analysis</span>
            </CardTitle>
            <CardDescription>
              Historical data analysis and trend detection with correlation studies
            </CardDescription>
          </CardHeader>
          
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <h5 className="text-sm font-medium">Features:</h5>
              <ul className="text-xs text-muted-foreground space-y-1">
                <li>• Historical trend analysis</li>
                <li>• Correlation detection</li>
                <li>• Volatility analysis</li>
                <li>• Market pattern recognition</li>
              </ul>
            </div>
            
            <div className="flex items-center justify-between text-xs">
              <Badge variant="success">Ready</Badge>
              <span className="text-muted-foreground">~3 min runtime</span>
            </div>
            
            <div className="flex space-x-2">
              <Link href="/analysis/market-data" className="flex-1">
                <Button variant="outline" className="w-full">
                  <Zap className="h-4 w-4 mr-2" />
                  Launch
                </Button>
              </Link>
              <Button variant="ghost" size="icon">
                <BarChart3 className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Pattern Recognition */}
        <Card className="feature-card opacity-75">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Search className="h-5 w-5 text-muted-foreground" />
              <span>A4: Pattern Recognition</span>
            </CardTitle>
            <CardDescription>
              AI-powered pattern detection and chart analysis (Coming Soon)
            </CardDescription>
          </CardHeader>
          
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <h5 className="text-sm font-medium">Planned Features:</h5>
              <ul className="text-xs text-muted-foreground space-y-1">
                <li>• AI-powered analysis</li>
                <li>• Chart pattern detection</li>
                <li>• Candlestick patterns</li>
                <li>• Support/resistance levels</li>
              </ul>
            </div>
            
            <div className="flex items-center justify-between text-xs">
              <Badge variant="secondary">Development</Badge>
              <span className="text-muted-foreground">Q2 2024</span>
            </div>
            
            <div className="flex space-x-2">
              <Button variant="outline" className="flex-1" disabled>
                Coming Soon
              </Button>
              <Button variant="ghost" size="icon">
                <Users className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}