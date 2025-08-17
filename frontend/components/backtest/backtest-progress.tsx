import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { Activity, CheckCircle, Clock } from 'lucide-react'

interface BacktestProgressProps {
  progress: number
  currentTest: string
  isRunning: boolean
  totalTests: number
  completedTests: number
}

export function BacktestProgress({ 
  progress, 
  currentTest, 
  isRunning, 
  totalTests, 
  completedTests 
}: BacktestProgressProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          {isRunning ? (
            <Activity className="h-5 w-5 animate-pulse text-blue-600" />
          ) : (
            <CheckCircle className="h-5 w-5 text-green-600" />
          )}
          Backtest Progress
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span>Overall Progress</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <Progress value={progress} className="w-full" />
        </div>
        
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-blue-600">{totalTests}</div>
            <div className="text-sm text-gray-600">Total Tests</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-green-600">{completedTests}</div>
            <div className="text-sm text-gray-600">Completed</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-orange-600">{totalTests - completedTests}</div>
            <div className="text-sm text-gray-600">Remaining</div>
          </div>
        </div>

        {isRunning && currentTest && (
          <div className="flex items-center gap-2 p-3 bg-blue-50 rounded-lg">
            <Clock className="h-4 w-4 text-blue-600" />
            <span className="text-sm">
              Currently running: <strong>{currentTest}</strong>
            </span>
          </div>
        )}

        <div className="flex justify-center">
          <Badge variant={isRunning ? "default" : "secondary"}>
            {isRunning ? "Running..." : "Completed"}
          </Badge>
        </div>
      </CardContent>
    </Card>
  )
}