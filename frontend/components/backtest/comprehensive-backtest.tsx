"use client"

import { useState } from 'react'
import { BacktestConfiguration } from './backtest-configuration'
import { BacktestProgress } from './backtest-progress'
import { BacktestResults } from './backtest-results'

export interface BacktestResult {
  id: string
  strategy: string
  asset: string
  timeframe: string
  totalReturn: number
  sharpeRatio: number
  maxDrawdown: number
  winRate: number
  totalTrades: number
  finalPortfolio: number
  status: 'pending' | 'running' | 'completed' | 'failed'
}

export function ComprehensiveBacktest() {
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<BacktestResult[]>([])
  const [progress, setProgress] = useState(0)
  const [currentTest, setCurrentTest] = useState('')

  const handleStartBacktest = async (config: any) => {
    setIsRunning(true)
    setResults([])
    setProgress(0)
    
    // Generate all test combinations
    const testCombinations: BacktestResult[] = []
    let testId = 1
    
    for (const strategy of config.strategies) {
      for (const asset of config.assets) {
        for (const timeframe of config.timeframes) {
          testCombinations.push({
            id: `test-${testId++}`,
            strategy,
            asset,
            timeframe,
            totalReturn: 0,
            sharpeRatio: 0,
            maxDrawdown: 0,
            winRate: 0,
            totalTrades: 0,
            finalPortfolio: config.initialCapital,
            status: 'pending'
          })
        }
      }
    }
    
    setResults(testCombinations)
    
    // Simulate running tests
    const totalTests = testCombinations.length
    let completedTests = 0
    
    for (let i = 0; i < testCombinations.length; i++) {
      const test = testCombinations[i]
      setCurrentTest(`${test.strategy} - ${test.asset} (${test.timeframe})`)
      
      // Update status to running
      setResults(prev => prev.map(r => 
        r.id === test.id ? { ...r, status: 'running' as const } : r
      ))
      
      // Simulate test execution time
      await new Promise(resolve => setTimeout(resolve, Math.random() * 2000 + 500))
      
      // Generate mock results
      const mockResult = {
        totalReturn: Math.random() * 100 - 20, // -20% to 80%
        sharpeRatio: Math.random() * 3 + 0.2, // 0.2 to 3.2
        maxDrawdown: Math.random() * -30, // 0% to -30%
        winRate: Math.random() * 50 + 30, // 30% to 80%
        totalTrades: Math.floor(Math.random() * 300) + 20, // 20 to 320
        finalPortfolio: config.initialCapital * (1 + (Math.random() * 100 - 20) / 100)
      }
      
      // Update results
      setResults(prev => prev.map(r => 
        r.id === test.id 
          ? { ...r, ...mockResult, status: 'completed' as const }
          : r
      ))
      
      completedTests++
      setProgress((completedTests / totalTests) * 100)
    }
    
    setIsRunning(false)
    setCurrentTest('')
  }

  return (
    <div className="space-y-6">
      {/* Configuration */}
      <BacktestConfiguration onStartBacktest={handleStartBacktest} />
      
      {/* Progress */}
      {(isRunning || results.length > 0) && (
        <BacktestProgress 
          progress={progress}
          currentTest={currentTest}
          isRunning={isRunning}
          totalTests={results.length}
          completedTests={results.filter(r => r.status === 'completed').length}
        />
      )}
      
      {/* Results */}
      {results.length > 0 && (
        <BacktestResults results={results} />
      )}
    </div>
  )
}