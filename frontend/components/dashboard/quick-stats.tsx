"use client"

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { TrendingUp, TrendingDown, Target, Activity } from 'lucide-react'
import { formatCurrency, formatPercentage, getPercentageColor } from '@/lib/utils'

interface QuickStatsProps {
  portfolioValue: number
  todayPnL: number
  todayPnLPercentage: number
  winRate: number
  activePositions: number
}

export function QuickStats({
  portfolioValue = 10955,
  todayPnL = 955,
  todayPnLPercentage = 9.6,
  winRate = 68,
  activePositions = 3
}: QuickStatsProps) {
  const stats = [
    {
      title: "Portfolio Value",
      value: formatCurrency(portfolioValue),
      icon: TrendingUp,
      description: "Total portfolio value"
    },
    {
      title: "Today's P&L",
      value: formatCurrency(todayPnL),
      change: formatPercentage(todayPnLPercentage),
      icon: todayPnL >= 0 ? TrendingUp : TrendingDown,
      description: "Daily profit & loss",
      valueColor: getPercentageColor(todayPnL)
    },
    {
      title: "Win Rate",
      value: `${winRate}%`,
      icon: Target,
      description: "Success rate of trades"
    },
    {
      title: "Active Positions",
      value: activePositions.toString(),
      icon: Activity,
      description: "Currently open positions"
    }
  ]

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat, index) => {
        const Icon = stat.icon
        return (
          <Card key={index} className="stat-card">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {stat.title}
              </CardTitle>
              <Icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="flex items-center space-x-2">
                <div className={`text-2xl font-bold ${stat.valueColor || ''}`}>
                  {stat.value}
                </div>
                {stat.change && (
                  <div className={`text-xs ${getPercentageColor(todayPnL)} flex items-center`}>
                    {todayPnL >= 0 ? (
                      <TrendingUp className="h-3 w-3 mr-1" />
                    ) : (
                      <TrendingDown className="h-3 w-3 mr-1" />
                    )}
                    {stat.change}
                  </div>
                )}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                {stat.description}
              </p>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}