"use client"

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { 
  BarChart3, 
  Gamepad2, 
  Settings, 
  TrendingUp, 
  Activity, 
  BookOpen,
  Search,
  Star,
  Smartphone,
  Zap
} from 'lucide-react'

const quickActions = [
  {
    title: "Run Quick Backtest",
    description: "Fast strategy validation",
    icon: BarChart3,
    href: "/backtest/quick",
    variant: "default" as const
  },
  {
    title: "Start Demo Trading",
    description: "Practice with virtual money",
    icon: Gamepad2,
    href: "/realtime?mode=demo",
    variant: "outline" as const
  },
  {
    title: "Configuration",
    description: "System settings & preferences",
    icon: Settings,
    href: "/settings",
    variant: "outline" as const
  },
  {
    title: "View Performance",
    description: "Analyze trading results",
    icon: TrendingUp,
    href: "/performance",
    variant: "outline" as const
  },
  {
    title: "System Health",
    description: "Check system status",
    icon: Activity,
    href: "/health",
    variant: "outline" as const
  },
  {
    title: "Documentation",
    description: "Guides and tutorials",
    icon: BookOpen,
    href: "/docs",
    variant: "outline" as const
  },
  {
    title: "Search Features",
    description: "Find tools quickly",
    icon: Search,
    href: "/search",
    variant: "ghost" as const
  },
  {
    title: "My Favorites",
    description: "Frequently used tools",
    icon: Star,
    href: "/favorites",
    variant: "ghost" as const
  },
  {
    title: "Mobile App",
    description: "Download mobile version",
    icon: Smartphone,
    href: "/mobile",
    variant: "ghost" as const
  }
]

export function QuickActions() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Zap className="h-5 w-5" />
          <span>⚡ QUICK ACTIONS</span>
        </CardTitle>
      </CardHeader>
      
      <CardContent>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {quickActions.map((action, index) => {
            const Icon = action.icon
            return (
              <Link key={index} href={action.href}>
                <Button 
                  variant={action.variant} 
                  className="w-full justify-start h-auto p-4 text-left"
                >
                  <div className="flex items-center space-x-3">
                    <Icon className="h-5 w-5 flex-shrink-0" />
                    <div className="min-w-0">
                      <div className="font-medium truncate">{action.title}</div>
                      <div className="text-xs text-muted-foreground truncate">
                        {action.description}
                      </div>
                    </div>
                  </div>
                </Button>
              </Link>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}