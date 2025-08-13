"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Gamepad2, 
  RotateCcw, 
  BarChart3, 
  Globe, 
  Brain, 
  TestTube,
  Star,
  ExternalLink,
  Clock
} from 'lucide-react'

interface Feature {
  id: string
  name: string
  description: string
  icon: any
  status: 'ready' | 'beta' | 'development'
  lastUsed?: string
  category: 'crypto' | 'core' | 'testing'
  features: string[]
  isFavorite?: boolean
}

const features: Feature[] = [
  // Crypto Features
  {
    id: 'interactive-crypto',
    name: 'Interactive Crypto Demo',
    description: 'Interactive cryptocurrency trading demo with real-time data',
    icon: Gamepad2,
    status: 'ready',
    lastUsed: '2h',
    category: 'crypto',
    features: ['Real-time data', 'Live trading', 'Interactive UI'],
    isFavorite: true
  },
  {
    id: 'batch-runner',
    name: 'Batch Runner Demo',
    description: 'Batch processing for multiple strategy testing',
    icon: RotateCcw,
    status: 'ready',
    lastUsed: '1d',
    category: 'crypto',
    features: ['Multi-strategy', 'Parallel execution', 'Batch processing']
  },
  {
    id: 'delta-backtest',
    name: 'Delta Exchange Backtesting',
    description: 'Advanced backtesting with Delta Exchange integration',
    icon: BarChart3,
    status: 'ready',
    lastUsed: '3h',
    category: 'crypto',
    features: ['Advanced backtesting', 'Exchange API', 'Historical data']
  },
  
  // Core Features
  {
    id: 'backtest-engine',
    name: 'Backtest Engine',
    description: 'Standalone backtesting engine with comprehensive analysis',
    icon: BarChart3,
    status: 'ready',
    lastUsed: '1h',
    category: 'core',
    features: ['Historical analysis', 'Multiple timeframes', 'Performance metrics']
  },
  {
    id: 'web-dashboard',
    name: 'Web Dashboard',
    description: 'Web-based trading dashboard with real-time updates',
    icon: Globe,
    status: 'beta',
    lastUsed: '30m',
    category: 'core',
    features: ['Web interface', 'Real-time UI', 'Responsive design']
  },
  {
    id: 'strategy-testing',
    name: 'Strategy Testing',
    description: 'Individual strategy testing and optimization',
    icon: Brain,
    status: 'ready',
    lastUsed: '4h',
    category: 'core',
    features: ['Individual testing', 'Custom parameters', 'Optimization']
  },
  
  // Testing Features
  {
    id: 'feature-demo',
    name: 'Feature Demo',
    description: 'Comprehensive feature demonstration and testing',
    icon: TestTube,
    status: 'ready',
    lastUsed: '2d',
    category: 'testing',
    features: ['Feature showcase', 'Demo mode', 'Testing suite']
  },
  {
    id: 'quick-test',
    name: 'Quick Test',
    description: 'Quick system functionality test and validation',
    icon: TestTube,
    status: 'ready',
    lastUsed: '1d',
    category: 'testing',
    features: ['Quick validation', 'System check', 'Health monitoring']
  },
  {
    id: 'all-features-test',
    name: 'All Features Test',
    description: 'Complete system testing suite with full coverage',
    icon: TestTube,
    status: 'ready',
    lastUsed: '3d',
    category: 'testing',
    features: ['Complete testing', 'Full coverage', 'System validation']
  }
]

const categoryConfig = {
  crypto: {
    title: '🪙 CRYPTO FEATURES',
    description: 'Cryptocurrency-specific trading tools and demos'
  },
  core: {
    title: '🔧 CORE FEATURES', 
    description: 'Essential trading platform functionality'
  },
  testing: {
    title: '🧪 TESTING FEATURES',
    description: 'Testing, validation, and demonstration tools'
  }
}

export function FeatureGrid() {
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'ready':
        return <Badge variant="success" className="text-xs">Ready</Badge>
      case 'beta':
        return <Badge variant="warning" className="text-xs">Beta</Badge>
      case 'development':
        return <Badge variant="secondary" className="text-xs">Dev</Badge>
      default:
        return <Badge variant="secondary" className="text-xs">Unknown</Badge>
    }
  }

  const handleLaunch = (featureId: string) => {
    console.log(`Launching feature: ${featureId}`)
    // Here you would implement the actual feature launch logic
  }

  const toggleFavorite = (featureId: string) => {
    console.log(`Toggling favorite for: ${featureId}`)
    // Here you would implement the favorite toggle logic
  }

  const categories = ['crypto', 'core', 'testing'] as const

  return (
    <div className="space-y-8">
      {categories.map((category) => {
        const categoryFeatures = features.filter(f => f.category === category)
        const config = categoryConfig[category]
        
        return (
          <div key={category} className="space-y-4">
            <div className="text-center space-y-2">
              <h2 className="text-2xl font-bold">{config.title}</h2>
              <p className="text-muted-foreground">{config.description}</p>
            </div>
            
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {categoryFeatures.map((feature) => {
                const Icon = feature.icon
                return (
                  <Card key={feature.id} className="feature-card group">
                    <CardHeader className="pb-3">
                      <div className="flex items-start justify-between">
                        <div className="flex items-center space-x-3">
                          <div className="p-2 rounded-lg bg-primary/10">
                            <Icon className="h-5 w-5 text-primary" />
                          </div>
                          <div>
                            <CardTitle className="text-lg">{feature.name}</CardTitle>
                            <div className="flex items-center space-x-2 mt-1">
                              {getStatusBadge(feature.status)}
                              {feature.lastUsed && (
                                <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                                  <Clock className="h-3 w-3" />
                                  <span>{feature.lastUsed}</span>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                        
                        <Button
                          variant="ghost"
                          size="icon"
                          className="opacity-0 group-hover:opacity-100 transition-opacity"
                          onClick={() => toggleFavorite(feature.id)}
                        >
                          <Star 
                            className={`h-4 w-4 ${feature.isFavorite ? 'fill-yellow-400 text-yellow-400' : ''}`} 
                          />
                        </Button>
                      </div>
                    </CardHeader>
                    
                    <CardContent className="space-y-4">
                      <CardDescription className="text-sm">
                        {feature.description}
                      </CardDescription>
                      
                      <div className="space-y-2">
                        <p className="text-xs font-medium text-muted-foreground">Features:</p>
                        <div className="flex flex-wrap gap-1">
                          {feature.features.map((feat, index) => (
                            <Badge key={index} variant="outline" className="text-xs">
                              {feat}
                            </Badge>
                          ))}
                        </div>
                      </div>
                      
                      <div className="flex space-x-2 pt-2">
                        <Button 
                          className="flex-1"
                          onClick={() => handleLaunch(feature.id)}
                        >
                          <ExternalLink className="h-4 w-4 mr-2" />
                          Launch
                        </Button>
                        <Button variant="outline" size="icon">
                          <Star className="h-4 w-4" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                )
              })}
            </div>
          </div>
        )
      })}
    </div>
  )
}