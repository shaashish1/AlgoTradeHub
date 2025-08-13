"use client"

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Play, 
  Server, 
  Database, 
  Activity,
  CheckCircle,
  XCircle,
  Clock,
  RefreshCw
} from 'lucide-react'
import { api, checkBackendHealth } from '@/lib/api'

export function TestInterface() {
  const [backendStatus, setBackendStatus] = useState<'unknown' | 'healthy' | 'unhealthy'>('unknown')
  const [testResults, setTestResults] = useState<any[]>([])
  const [isRunning, setIsRunning] = useState(false)

  const checkBackend = async () => {
    setIsRunning(true)
    try {
      const isHealthy = await checkBackendHealth()
      setBackendStatus(isHealthy ? 'healthy' : 'unhealthy')
    } catch (error) {
      setBackendStatus('unhealthy')
    } finally {
      setIsRunning(false)
    }
  }

  const runTest = async (testName: string, testFn: () => Promise<any>) => {
    setIsRunning(true)
    const startTime = Date.now()
    
    try {
      const result = await testFn()
      const duration = Date.now() - startTime
      
      setTestResults(prev => [...prev, {
        name: testName,
        status: 'success',
        duration,
        result,
        timestamp: new Date().toISOString()
      }])
    } catch (error) {
      const duration = Date.now() - startTime
      
      setTestResults(prev => [...prev, {
        name: testName,
        status: 'error',
        duration,
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      }])
    } finally {
      setIsRunning(false)
    }
  }

  const tests = [
    {
      name: 'System Status',
      description: 'Check system health and exchange connections',
      action: () => runTest('System Status', () => api.getSystemStatus())
    },
    {
      name: 'Quick Backtest',
      description: 'Run a simple backtest with default parameters',
      action: () => runTest('Quick Backtest', () => api.runBacktest({
        symbol: 'BTC/USDT',
        strategy: 'RSI Strategy',
        startDate: '2024-01-01',
        endDate: '2024-08-01',
        initialCapital: 10000,
        commission: 0.001
      }))
    },
    {
      name: 'Get Signals',
      description: 'Fetch current trading signals',
      action: () => runTest('Get Signals', () => api.getSignals())
    },
    {
      name: 'Get Positions',
      description: 'Retrieve current open positions',
      action: () => runTest('Get Positions', () => api.getPositions())
    },
    {
      name: 'Start Scanner',
      description: 'Start the real-time market scanner',
      action: () => runTest('Start Scanner', () => api.startScanner())
    },
    {
      name: 'Stop Scanner',
      description: 'Stop the real-time market scanner',
      action: () => runTest('Stop Scanner', () => api.stopScanner())
    }
  ]

  return (
    <div className="space-y-6">
      {/* Backend Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Server className="h-5 w-5" />
            <span>Backend Status</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2">
                {backendStatus === 'healthy' && <CheckCircle className="h-5 w-5 text-green-500" />}
                {backendStatus === 'unhealthy' && <XCircle className="h-5 w-5 text-red-500" />}
                {backendStatus === 'unknown' && <Clock className="h-5 w-5 text-gray-500" />}
                
                <Badge variant={
                  backendStatus === 'healthy' ? 'default' : 
                  backendStatus === 'unhealthy' ? 'destructive' : 
                  'secondary'
                }>
                  {backendStatus === 'healthy' ? 'Connected' : 
                   backendStatus === 'unhealthy' ? 'Disconnected' : 
                   'Unknown'}
                </Badge>
              </div>
              
              <p className="text-sm text-muted-foreground">
                {backendStatus === 'healthy' && 'Backend is running and accessible'}
                {backendStatus === 'unhealthy' && 'Backend is not responding (using demo mode)'}
                {backendStatus === 'unknown' && 'Backend status not checked'}
              </p>
            </div>
            
            <Button 
              variant="outline" 
              onClick={checkBackend}
              disabled={isRunning}
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${isRunning ? 'animate-spin' : ''}`} />
              Check Status
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Test Suite */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Activity className="h-5 w-5" />
            <span>API Test Suite</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {tests.map((test, index) => (
              <Card key={index} className="border-2">
                <CardContent className="pt-4">
                  <div className="space-y-3">
                    <div>
                      <h3 className="font-medium">{test.name}</h3>
                      <p className="text-sm text-muted-foreground">{test.description}</p>
                    </div>
                    
                    <Button 
                      size="sm" 
                      className="w-full"
                      onClick={test.action}
                      disabled={isRunning}
                    >
                      <Play className="h-4 w-4 mr-2" />
                      Run Test
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Test Results */}
      {testResults.length > 0 && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center space-x-2">
                <Database className="h-5 w-5" />
                <span>Test Results</span>
              </CardTitle>
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => setTestResults([])}
              >
                Clear Results
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {testResults.map((result, index) => (
                <div key={index} className="flex items-start justify-between p-3 rounded-lg border">
                  <div className="flex items-start space-x-3">
                    {result.status === 'success' ? (
                      <CheckCircle className="h-5 w-5 text-green-500 mt-0.5" />
                    ) : (
                      <XCircle className="h-5 w-5 text-red-500 mt-0.5" />
                    )}
                    
                    <div>
                      <h4 className="font-medium">{result.name}</h4>
                      <p className="text-sm text-muted-foreground">
                        {new Date(result.timestamp).toLocaleTimeString()} • {result.duration}ms
                      </p>
                      
                      {result.status === 'error' && (
                        <p className="text-sm text-red-600 mt-1">{result.error}</p>
                      )}
                      
                      {result.status === 'success' && result.result && (
                        <pre className="text-xs bg-muted p-2 rounded mt-2 overflow-x-auto">
                          {JSON.stringify(result.result, null, 2)}
                        </pre>
                      )}
                    </div>
                  </div>
                  
                  <Badge variant={result.status === 'success' ? 'default' : 'destructive'}>
                    {result.status}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}