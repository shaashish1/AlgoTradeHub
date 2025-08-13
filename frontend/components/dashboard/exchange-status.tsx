"use client"

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Building2, CheckCircle, XCircle, AlertCircle } from 'lucide-react'

interface Exchange {
  name: string
  status: 'online' | 'offline' | 'maintenance'
  mode: 'sandbox' | 'live'
  symbols: number
  lastPing: string
}

const mockExchanges: Exchange[] = [
  {
    name: 'Binance',
    status: 'online',
    mode: 'sandbox',
    symbols: 15,
    lastPing: '< 1s'
  },
  {
    name: 'Kraken',
    status: 'online',
    mode: 'live',
    symbols: 8,
    lastPing: '2s'
  },
  {
    name: 'Delta',
    status: 'offline',
    mode: 'sandbox',
    symbols: 0,
    lastPing: '5m ago'
  }
]

export function ExchangeStatus() {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'online':
        return <CheckCircle className="h-4 w-4 text-success" />
      case 'offline':
        return <XCircle className="h-4 w-4 text-danger" />
      case 'maintenance':
        return <AlertCircle className="h-4 w-4 text-warning" />
      default:
        return <XCircle className="h-4 w-4 text-muted-foreground" />
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'online':
        return <Badge variant="success" className="text-xs">Online</Badge>
      case 'offline':
        return <Badge variant="destructive" className="text-xs">Offline</Badge>
      case 'maintenance':
        return <Badge variant="warning" className="text-xs">Maintenance</Badge>
      default:
        return <Badge variant="secondary" className="text-xs">Unknown</Badge>
    }
  }

  const getModeBadge = (mode: string) => {
    return (
      <Badge 
        variant={mode === 'live' ? 'destructive' : 'secondary'} 
        className="text-xs"
      >
        {mode === 'live' ? 'Live' : 'Sandbox'}
      </Badge>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Building2 className="h-5 w-5" />
          <span>Active Exchanges</span>
        </CardTitle>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {mockExchanges.map((exchange, index) => (
          <div key={index} className="flex items-center justify-between p-3 rounded-lg border">
            <div className="flex items-center space-x-3">
              {getStatusIcon(exchange.status)}
              <div>
                <div className="font-medium">{exchange.name}</div>
                <div className="text-xs text-muted-foreground">
                  {exchange.symbols} symbols • {exchange.lastPing}
                </div>
              </div>
            </div>
            
            <div className="flex flex-col items-end space-y-1">
              {getStatusBadge(exchange.status)}
              {getModeBadge(exchange.mode)}
            </div>
          </div>
        ))}
        
        <div className="pt-2 border-t text-center">
          <p className="text-xs text-muted-foreground">
            {mockExchanges.filter(e => e.status === 'online').length} of {mockExchanges.length} exchanges online
          </p>
        </div>
      </CardContent>
    </Card>
  )
}