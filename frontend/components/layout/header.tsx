"use client"

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { 
  Rocket, 
  Menu, 
  Settings, 
  User, 
  HelpCircle,
  BarChart3,
  Activity,
  Zap,
  TrendingUp,
  PieChart
} from 'lucide-react'
import { cn } from '@/lib/utils'

const navigation = [
  { name: 'Dashboard', href: '/', icon: BarChart3 },
  { name: 'Exchanges', href: '/exchanges', icon: Settings },
  { name: 'Trading', href: '/trading', icon: TrendingUp },
  { name: 'Portfolio', href: '/portfolio', icon: PieChart },
  { name: 'Backtest', href: '/backtest', icon: Activity },
  { name: 'Features', href: '/features', icon: Zap },
]

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const pathname = usePathname()

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center space-x-2">
          <Rocket className="h-6 w-6 text-primary" />
          <span className="text-xl font-bold">AlgoTradeHub</span>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center space-x-6">
          {navigation.map((item) => {
            const Icon = item.icon
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "flex items-center space-x-2 text-sm font-medium transition-colors hover:text-primary",
                  pathname === item.href
                    ? "text-primary"
                    : "text-muted-foreground"
                )}
              >
                <Icon className="h-4 w-4" />
                <span>{item.name}</span>
              </Link>
            )
          })}
        </nav>

        {/* Status Indicators */}
        <div className="hidden lg:flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-sm">
            <div className="h-2 w-2 rounded-full bg-success animate-pulse-success" />
            <span className="text-muted-foreground">Scanner: ON</span>
          </div>
          <div className="flex items-center space-x-2 text-sm">
            <div className="h-2 w-2 rounded-full bg-warning" />
            <span className="text-muted-foreground">Mode: DEMO</span>
          </div>
        </div>

        {/* Right Side Actions */}
        <div className="flex items-center space-x-2">
          <Button variant="ghost" size="icon" className="hidden md:flex">
            <HelpCircle className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="icon" className="hidden md:flex">
            <Settings className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="icon" className="hidden md:flex">
            <User className="h-4 w-4" />
          </Button>
          
          {/* Mobile Menu Button */}
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            <Menu className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t bg-background">
          <div className="container py-4 space-y-2">
            {navigation.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    "flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                    pathname === item.href
                      ? "bg-primary/10 text-primary"
                      : "text-muted-foreground hover:text-primary hover:bg-muted"
                  )}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.name}</span>
                </Link>
              )
            })}
            
            {/* Mobile Status */}
            <div className="pt-4 border-t space-y-2">
              <div className="flex items-center justify-between px-3 py-2">
                <span className="text-sm text-muted-foreground">Scanner Status</span>
                <div className="flex items-center space-x-2">
                  <div className="h-2 w-2 rounded-full bg-success animate-pulse-success" />
                  <span className="text-sm font-medium text-success">ON</span>
                </div>
              </div>
              <div className="flex items-center justify-between px-3 py-2">
                <span className="text-sm text-muted-foreground">Trading Mode</span>
                <div className="flex items-center space-x-2">
                  <div className="h-2 w-2 rounded-full bg-warning" />
                  <span className="text-sm font-medium text-warning">DEMO</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </header>
  )
}