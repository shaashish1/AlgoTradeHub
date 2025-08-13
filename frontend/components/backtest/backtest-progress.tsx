"use client"

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { 
  BarChart3, 
  Pause, 
  Square, 
  Info,
  Cpu,
  HardDrive,
  Wifi,
  Users
} from 'lucide-react'

export function BacktestProgress() {
  return (
    <div className="space-y-6">
      {/* Progress Header */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <BarChart3 className="h-5 w-5" />
            <span>📊 Progress & Status</span>
          </CardTitle>
        </CardHeader>
        
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>Current Test: MACD Strategy - SOL/USDT - 4h timeframe</span>
              <span>67% Complete</span>
            </div>
            <Progress value={67} className="h-2" />
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>Completed: 1,900 / 2,835 tests</span>
              <span>ETA: 6m 15s</span>
            </div>
          </div>
          
          <div className="flex justify-between text-sm">
            <span>Elapsed: 12m 34s</span>
            <span>Remaining: ~6m 15s</span>
          </div>
        </CardContent>
      </Card>

      {/* System Status */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-lg flex items-center space-x-2">
              <Cpu className="h-4 w-4" />
              <span>🖥️ System Status</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span>CPU:</span>
              <span className="font-medium">78%</span>
            </div>
            <div className="flex justify-between">
              <span>Memory:</span>
              <span className="font-medium">2.1GB</span>
            </div>
            <div className="flex justify-between">
              <span>Disk:</span>
              <span className="font-medium">45MB/s</span>
            </div>
            <div className="flex justify-between">
              <span>Network:</span>
              <span className="font-medium">12MB/s</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-lg flex items-center space-x-2">
              <BarChart3 className="h-4 w-4" />
              <span>📈 Performance</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span>Tests/sec:</span>
              <span className="font-medium">4.2</span>
            </div>
            <div className="flex justify-between">
              <span>Success:</span>
              <span className="font-medium text-success">98.5%</span>
            </div>
            <div className="flex justify-between">
              <span>Errors:</span>
              <span className="font-medium text-warning">29</span>
            </div>
            <div className="flex justify-between">
              <span>Avg Time:</span>
              <span className="font-medium">2.3s</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-lg flex items-center space-x-2">
              <Users className="h-4 w-4" />
              <span>🔧 Workers</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span>Active:</span>
              <span className="font-medium text-success">4/4</span>
            </div>
            <div className="flex justify-between">
              <span>Queue:</span>
              <span className="font-medium">935</span>
            </div>
            <div className="flex justify-between">
              <span>Failed:</span>
              <span className="font-medium">0</span>
            </div>
            <div className="flex justify-between">
              <span>Idle:</span>
              <span className="font-medium">0</span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Controls */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Badge variant="success" className="animate-pulse">
                Running smoothly
              </Badge>
            </div>
            
            <div className="flex space-x-2">
              <Button variant="outline" size="sm">
                <Pause className="h-4 w-4 mr-2" />
                Pause
              </Button>
              <Button variant="outline" size="sm">
                <Square className="h-4 w-4 mr-2" />
                Stop
              </Button>
              <Button variant="outline" size="sm">
                <Info className="h-4 w-4 mr-2" />
                Details
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}