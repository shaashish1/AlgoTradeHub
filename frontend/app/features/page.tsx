import { Header } from '@/components/layout/header'
import { FeatureGrid } from '@/components/features/feature-grid'
import { AdvancedOptions } from '@/components/features/advanced-options'
import { QuickActions } from '@/components/features/quick-actions'

export default function FeaturesPage() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container py-6 space-y-8">
        {/* Hero Section */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold tracking-tight">AlgoTradeHub Features</h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Browse & Execute All Available Tools
          </p>
          <p className="text-muted-foreground">
            Discover powerful trading tools, advanced backtesting, and comprehensive analysis features
          </p>
        </div>

        {/* Feature Categories */}
        <FeatureGrid />

        {/* Advanced Options */}
        <AdvancedOptions />

        {/* Quick Actions */}
        <QuickActions />
      </main>
    </div>
  )
}