import { Metadata } from 'next'
import ExchangeSelector from '@/components/exchange/exchange-selector'

export const metadata: Metadata = {
  title: 'Exchange Configuration - AlgoTradeHub',
  description: 'Configure and manage your trading exchanges',
}

export default function ExchangesPage() {
  return (
    <div className="container mx-auto py-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Exchange Configuration</h1>
          <p className="text-muted-foreground">
            Configure your trading exchanges and API credentials
          </p>
        </div>
      </div>

      <ExchangeSelector />
    </div>
  )
}