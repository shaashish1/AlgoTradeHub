"use client"

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { 
  Play, 
  BarChart3, 
  Zap, 
  Settings,
  TrendingUp,
  Activity
} from 'lucide-react'

export function QuickActions() {
  const actions = [
    {
      title: "Start Trading",
      description: "Begin real-time trading",
      icon: Play,
      href: "/realtime",
      variant: "default" as const
    },
    {
      title: "Run Backtest",
      description: "Test strategies on historical data",
      icon: BarChart3,
      href: "/backtest",
      variant: "outline" as const
    },
    {
      title: "View Features",
      description: "Browse all available tools",
      icon: Zap,
      href: "/features",
      variant: "outline" as const
    },
    {
      title: "Configuration",
      description: "Manage settings and preferences",
      icon: Settings,
      href: "/settings",
      variant: "outline" as const
    }
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Zap className="h-5 w-5" />
          <span>Quick Actions</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {actions.map((action, index) => {
          const Icon = action.icon
          return (
            <Link key={index} href={action.href}>
              <Button 
                variant={action.variant} 
                className="w-full justify-start h-auto p-4"
              >
                <div className="flex items-center space-x-3">
                  <Icon className="h-5 w-5" />
                  <div className="text-left">
                    <div className="font-medium">{action.title}</div>
                    <div className="text-xs text-muted-foreground">
                      {action.description}
                    </div>
                  </div>
                </div>
              </Button>
            </Link>
          )
        })}
      </CardContent>
    </Card>
  )
}