import { Header } from '@/components/layout/header'
import { RealTimeTrading } from '@/components/realtime/realtime-trading'

export default function RealTimePage() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container mx-auto px-4 py-6">
        <div className="space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">⚡ Real-time Trading</h1>
              <p className="text-muted-foreground">
                Live trading with real-time market data and automated strategies
              </p>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-sm">
                <div className="h-2 w-2 rounded-full bg-success animate-pulse" />
                <span className="text-muted-foreground">Scanner: ON</span>
              </div>
              <div className="flex items-center space-x-2 text-sm">
                <div className="h-2 w-2 rounded-full bg-warning" />
                <span className="text-muted-foreground">Mode: DEMO</span>
              </div>
            </div>
          </div>

          {/* Real-time Trading Interface */}
          <RealTimeTrading />
        </div>
      </main>
    </div>
  )
}