import { Header } from '@/components/layout/header'
import { ComprehensiveBacktest } from '@/components/backtest/comprehensive-backtest'

export default function ComprehensiveBacktestPage() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container mx-auto px-4 py-6">
        <div className="space-y-6">
          {/* Header */}
          <div>
            <h1 className="text-3xl font-bold tracking-tight">🚀 Comprehensive Backtesting Suite</h1>
            <p className="text-muted-foreground">
              Advanced multi-strategy, multi-asset backtesting with parallel execution
            </p>
          </div>

          {/* Comprehensive Backtest Interface */}
          <ComprehensiveBacktest />
        </div>
      </main>
    </div>
  )
}