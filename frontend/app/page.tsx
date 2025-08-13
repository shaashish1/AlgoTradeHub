import { Header } from '@/components/layout/header'
import { QuickStats } from '@/components/dashboard/quick-stats'
import { QuickActions } from '@/components/dashboard/quick-actions'
import { PortfolioChart } from '@/components/dashboard/portfolio-chart'
import { OpenPositions } from '@/components/dashboard/open-positions'
import { ExchangeStatus } from '@/components/dashboard/exchange-status'
import { RecentAlerts } from '@/components/dashboard/recent-alerts'

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container mx-auto px-4 py-6 space-y-6">
        {/* Hero Section */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">Welcome to AlgoTradeHub</h1>
          <p className="text-muted-foreground">Your comprehensive trading platform</p>
        </div>

        {/* Quick Stats */}
        <QuickStats 
          portfolioValue={10955}
          todayPnL={955}
          todayPnLPercentage={9.6}
          winRate={68}
          activePositions={3}
        />

        {/* Main Content Grid */}
        <div className="grid gap-6 lg:grid-cols-4">
          {/* Left Sidebar */}
          <div className="space-y-6 lg:col-span-1">
            <QuickActions />
            <ExchangeStatus />
            <RecentAlerts />
          </div>

          {/* Main Content */}
          <div className="space-y-6 lg:col-span-3">
            <PortfolioChart />
            <OpenPositions />
          </div>
        </div>
      </main>
    </div>
  )
}