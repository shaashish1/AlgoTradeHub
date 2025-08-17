'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { CheckCircle, Clock, AlertCircle, Settings } from 'lucide-react'

interface StatusItem {
  task: string
  status: 'completed' | 'in-progress' | 'pending'
  priority: 'P1' | 'P2' | 'P3'
  description: string
}

export default function ImplementationStatus() {
  const statusItems: StatusItem[] = [
    {
      task: 'Exchange Testing Framework',
      status: 'completed',
      priority: 'P1',
      description: '5 crypto exchanges tested and working'
    },
    {
      task: 'Exchange Selection UI',
      status: 'completed',
      priority: 'P1',
      description: 'Frontend component for exchange selection'
    },
    {
      task: 'API Configuration Interface',
      status: 'completed',
      priority: 'P1',
      description: 'Secure API credential management'
    },
    {
      task: 'Backend API Endpoints',
      status: 'completed',
      priority: 'P1',
      description: 'Exchange configuration and testing APIs'
    },
    {
      task: 'Live Trading Execution',
      status: 'completed',
      priority: 'P1',
      description: 'Real order execution with configured exchanges'
    },
    {
      task: 'Portfolio Integration',
      status: 'completed',
      priority: 'P1',
      description: 'Multi-exchange portfolio tracking'
    },
    {
      task: 'Zerodha Stock Integration',
      status: 'pending',
      priority: 'P2',
      description: 'KiteConnect API integration for stocks'
    },
    {
      task: 'Risk Management',
      status: 'pending',
      priority: 'P2',
      description: 'Position sizing and risk controls'
    }
  ]

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-600" />
      case 'in-progress':
        return <Clock className="h-4 w-4 text-yellow-600" />
      case 'pending':
        return <AlertCircle className="h-4 w-4 text-gray-400" />
      default:
        return <Settings className="h-4 w-4" />
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return <Badge className="bg-green-100 text-green-800">✅ Done</Badge>
      case 'in-progress':
        return <Badge className="bg-yellow-100 text-yellow-800">🔄 In Progress</Badge>
      case 'pending':
        return <Badge className="bg-gray-100 text-gray-600">⏳ Pending</Badge>
      default:
        return <Badge>Unknown</Badge>
    }
  }

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case 'P1':
        return <Badge variant="destructive">P1</Badge>
      case 'P2':
        return <Badge variant="secondary">P2</Badge>
      case 'P3':
        return <Badge variant="outline">P3</Badge>
      default:
        return <Badge>P?</Badge>
    }
  }

  const completedTasks = statusItems.filter(item => item.status === 'completed').length
  const totalTasks = statusItems.length
  const progressPercentage = Math.round((completedTasks / totalTasks) * 100)

  return (
    <div className="space-y-6">
      {/* Progress Overview */}
      <Card>
        <CardHeader>
          <CardTitle>Implementation Progress</CardTitle>
          <CardDescription>
            Current status of Priority 1 tasks and overall development progress
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Overall Progress</span>
              <span className="text-sm text-muted-foreground">{completedTasks}/{totalTasks} tasks</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-600 h-2 rounded-full transition-all duration-300" 
                style={{ width: `${progressPercentage}%` }}
              />
            </div>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-green-600">{completedTasks}</div>
                <div className="text-sm text-gray-600">Completed</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-yellow-600">0</div>
                <div className="text-sm text-gray-600">In Progress</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-gray-600">{totalTasks - completedTasks}</div>
                <div className="text-sm text-gray-600">Pending</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Task List */}
      <Card>
        <CardHeader>
          <CardTitle>Task Status</CardTitle>
          <CardDescription>
            Detailed breakdown of implementation tasks by priority
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {statusItems.map((item, index) => (
              <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(item.status)}
                  <div>
                    <div className="font-medium">{item.task}</div>
                    <div className="text-sm text-gray-600">{item.description}</div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  {getPriorityBadge(item.priority)}
                  {getStatusBadge(item.status)}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* What's Working Now */}
      <Card>
        <CardHeader>
          <CardTitle className="text-green-600">✅ What's Working Now</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-3">
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <span>5 crypto exchanges tested and ready (Binance, Bybit, Delta, Gate.io, Bitget)</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <span>6,485+ trading pairs available across all exchanges</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <span>Exchange selection UI with API configuration</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <span>Sandbox mode testing for safe development</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <span>Backend APIs for exchange management</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <span>Live trading interface with order execution</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <span>Multi-exchange portfolio tracking</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <span>Unified frontend at port 3000 with API proxy</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Next Steps */}
      <Card>
        <CardHeader>
          <CardTitle className="text-blue-600">🚀 Next Steps</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="p-3 bg-green-50 rounded-lg">
              <div className="font-medium text-green-800">✅ Priority 1 Complete</div>
              <div className="text-sm text-green-600">
                All Priority 1 tasks completed! Ready for live crypto trading at port 3000
              </div>
            </div>
            <div className="p-3 bg-blue-50 rounded-lg">
              <div className="font-medium text-blue-800">Ready to Trade</div>
              <div className="text-sm text-blue-600">
                Configure your API credentials and start live trading on the Trading page
              </div>
            </div>
            <div className="p-3 bg-purple-50 rounded-lg">
              <div className="font-medium text-purple-800">Stock Trading</div>
              <div className="text-sm text-purple-600">
                Custom integration required for Indian stock brokers (2-4 weeks estimated)
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}