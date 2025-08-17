import { Metadata } from 'next'
import LiveTradingInterface from '@/components/trading/live-trading-interface'

export const metadata: Metadata = {
  title: 'Live Trading - AlgoTradeHub',
  description: 'Execute live trades across multiple exchanges',
}

export default function TradingPage() {
  return (
    <div className="container mx-auto py-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Live Trading</h1>
          <p className="text-muted-foreground">
            Execute trades across your configured exchanges
          </p>
        </div>
      </div>
      <LiveTradingInterface />
    </div>
  )
}