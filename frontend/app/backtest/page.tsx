import { Header } from '@/components/layout/header'
import { BacktestInterface } from '@/components/backtest/backtest-interface'

export default function BacktestPage() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container mx-auto px-4 py-6">
        <div className="space-y-6">
          {/* Header */}
          <div className="text-center space-y-2">
            <h1 className="text-3xl font-bold tracking-tight">📊 Strategy Backtesting</h1>
            <p className="text-muted-foreground">
              Test your trading strategies on historical data
            </p>
          </div>

          {/* Backtest Interface */}
          <BacktestInterface />
        </div>
      </main>
    </div>
  )
}