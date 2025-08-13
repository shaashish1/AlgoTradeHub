"use client"

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Bell, TrendingUp, TrendingDown, DollarSign, AlertTriangle } from 'lucide-react'

interface Alert {
  id: string
  type: 'buy' | 'sell' | 'profit' | 'loss' | 'warning'
  message: string
  symbol?: string
  price?: number
  time: string
  isNew?: boolean
}

const mockAlerts: Alert[] = [
  {
    id: '1',
    type: 'buy',
    message: 'BUY signal: SOL/USDT @ 97.50',
    symbol: 'SOL/USDT',
    price: 97.50,
    time: '14:35',
    isNew: true
  },
  {
    id: '2',
    type: 'sell',
    message: 'SELL signal: ETH/USDT @ 2,845',
    symbol: 'ETH/USDT',
    price: 2845,
    time: '14:32',
    isNew: true
  },
  {
    id: '3',
    type: 'profit',
    message: 'Take profit hit: ADA/USDT +3.5%',
    symbol: 'ADA/USDT',
    time: '14:28'
  },
  {
    id: '4',
    type: 'loss',
    message: 'Stop loss triggered: BNB/USDT -2.3%',
    symbol: 'BNB/USDT',
    time: '14:25'
  }
]

export function RecentAlerts() {
  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'buy':
        return <TrendingUp className="h-4 w-4 text-success" />
      case 'sell':
        return <TrendingDown className="h-4 w-4 text-danger" />
      case 'profit':
        return <DollarSign className="h-4 w-4 text-success" />
      case 'loss':
        return <AlertTriangle className="h-4 w-4 text-danger" />
      default:
        return <Bell className="h-4 w-4 text-muted-foreground" />
    }
  }

  const getAlertColor = (type: string) => {
    switch (type) {
      case 'buy':
      case 'profit':
        return 'border-l-success'
      case 'sell':
      case 'loss':
        return 'border-l-danger'
      case 'warning':
        return 'border-l-warning'
      default:
        return 'border-l-muted'
    }
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center space-x-2">
            <Bell className="h-5 w-5" />
            <span>Recent Alerts</span>
            {mockAlerts.filter(a => a.isNew).length > 0 && (
              <Badge variant="destructive" className="text-xs">
                {mockAlerts.filter(a => a.isNew).length}
              </Badge>
            )}
          </CardTitle>
          <Button variant="ghost" size="sm" className="text-xs">
            View All
          </Button>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-3">
        {mockAlerts.length > 0 ? (
          mockAlerts.map((alert) => (
            <div 
              key={alert.id} 
              className={`flex items-start space-x-3 p-3 rounded-lg border-l-2 bg-muted/30 ${getAlertColor(alert.type)}`}
            >
              <div className="flex-shrink-0 mt-0.5">
                {getAlertIcon(alert.type)}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium truncate">
                    {alert.message}
                  </p>
                  {alert.isNew && (
                    <Badge variant="destructive" className="text-xs ml-2">
                      New
                    </Badge>
                  )}
                </div>
                <div className="flex items-center justify-between mt-1">
                  <p className="text-xs text-muted-foreground">
                    {alert.time}
                  </p>
                  {alert.symbol && (
                    <Badge variant="outline" className="text-xs">
                      {alert.symbol}
                    </Badge>
                  )}
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-6 text-muted-foreground">
            <Bell className="h-8 w-8 mx-auto mb-2 opacity-50" />
            <p className="text-sm">No recent alerts</p>
            <p className="text-xs">Trading signals will appear here</p>
          </div>
        )}
        
        <div className="pt-2 border-t">
          <div className="flex justify-between">
            <Button variant="outline" size="sm" className="text-xs">
              Settings
            </Button>
            <Button variant="outline" size="sm" className="text-xs">
              Clear All
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}