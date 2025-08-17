import { Metadata } from 'next'
import MultiExchangePortfolio from '@/components/portfolio/multi-exchange-portfolio'

export const metadata: Metadata = {
  title: 'Portfolio - AlgoTradeHub',
  description: 'Track your portfolio across multiple exchanges',
}

export default function PortfolioPage() {
  return (
    <div className="container mx-auto py-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Multi-Exchange Portfolio</h1>
          <p className="text-muted-foreground">
            Monitor your investments across all configured exchanges
          </p>
        </div>
      </div>
      <MultiExchangePortfolio />
    </div>
  )
}