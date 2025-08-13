"use client"

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { TrendingUp } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

// Mock data for the chart
const generateMockData = (days: number) => {
  const data = []
  const baseValue = 10000
  let currentValue = baseValue
  
  for (let i = 0; i < days; i++) {
    const change = (Math.random() - 0.5) * 200
    currentValue += change
    data.push({
      date: new Date(Date.now() - (days - i) * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      portfolio: Math.max(currentValue, baseValue * 0.8),
      pnl: currentValue - baseValue,
      trades: Math.floor(Math.random() * 10) + 1
    })
  }
  return data
}

const timeRanges = [
  { label: '1D', days: 1 },
  { label: '1W', days: 7 },
  { label: '1M', days: 30 },
  { label: '3M', days: 90 },
  { label: '1Y', days: 365 },
  { label: 'ALL', days: 730 }
]

const chartTypes = [
  { label: 'Portfolio', key: 'portfolio' },
  { label: 'P&L', key: 'pnl' },
  { label: 'Trades', key: 'trades' }
]

export function PortfolioChart() {
  const [selectedRange, setSelectedRange] = useState('1M')
  const [selectedType, setSelectedType] = useState('portfolio')
  
  const currentRange = timeRanges.find(r => r.label === selectedRange) || timeRanges[2]
  const data = generateMockData(currentRange.days)
  
  const formatValue = (value: number) => {
    if (selectedType === 'portfolio' || selectedType === 'pnl') {
      return `$${value.toLocaleString()}`
    }
    return value.toString()
  }

  const getLineColor = () => {
    switch (selectedType) {
      case 'portfolio': return '#3b82f6'
      case 'pnl': return '#10b981'
      case 'trades': return '#f59e0b'
      default: return '#3b82f6'
    }
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-2 sm:space-y-0">
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="h-5 w-5" />
            <span>Portfolio Performance</span>
          </CardTitle>
          
          <div className="flex flex-wrap gap-2">
            {/* Time Range Buttons */}
            <div className="flex rounded-md border">
              {timeRanges.map((range) => (
                <Button
                  key={range.label}
                  variant={selectedRange === range.label ? "default" : "ghost"}
                  size="sm"
                  className="rounded-none first:rounded-l-md last:rounded-r-md"
                  onClick={() => setSelectedRange(range.label)}
                >
                  {range.label}
                </Button>
              ))}
            </div>
            
            {/* Chart Type Buttons */}
            <div className="flex rounded-md border">
              {chartTypes.map((type) => (
                <Button
                  key={type.key}
                  variant={selectedType === type.key ? "default" : "ghost"}
                  size="sm"
                  className="rounded-none first:rounded-l-md last:rounded-r-md"
                  onClick={() => setSelectedType(type.key)}
                >
                  {type.label}
                </Button>
              ))}
            </div>
          </div>
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
              <XAxis 
                dataKey="date" 
                tick={{ fontSize: 12 }}
                tickFormatter={(value) => {
                  const date = new Date(value)
                  return currentRange.days <= 7 
                    ? date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
                    : date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' })
                }}
              />
              <YAxis 
                tick={{ fontSize: 12 }}
                tickFormatter={formatValue}
              />
              <Tooltip 
                formatter={(value: number) => [formatValue(value), chartTypes.find(t => t.key === selectedType)?.label]}
                labelFormatter={(label) => new Date(label).toLocaleDateString()}
              />
              <Line 
                type="monotone" 
                dataKey={selectedType} 
                stroke={getLineColor()}
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}