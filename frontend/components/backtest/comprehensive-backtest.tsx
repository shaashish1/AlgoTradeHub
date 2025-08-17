"use client"

import { useState } from 'react'
import { BacktestConfiguration } from './backtest-configuration'
import { BacktestProgress } from './backtest-progress'
import { BacktestResults, BacktestResult } from './backtest-results'

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
            symbol: asset,
            timeframe,
            startDate: config.startDate,
            endDate: config.endDate,
            initialCapital: config.initialCapital,
            finalCapital: config.initialCapital,
            totalReturn: 0,
            totalReturnPercent: 0,
            maxDrawdown: 0,
            sharpeRatio: 0,
            winRate: 0,
            totalTrades: 0,
            winningTrades: 0,
            losingTrades: 0,
            avgWin: 0,
            avgLoss: 0,
            profitFactor: 1,
            status: 'running'
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
      setCurrentTest(`${test.strategy} - ${test.symbol} (${test.timeframe})`)
      
      // Update status to running
      setResults(prev => prev.map(r => 
        r.id === test.id ? { ...r, status: 'running' as const } : r
      ))
      
      // Simulate test execution time
      await new Promise(resolve => setTimeout(resolve, Math.random() * 2000 + 500))
      
      // Generate mock results
      const totalReturnPercent = Math.random() * 100 - 20 // -20% to 80%
      const finalCapital = config.initialCapital * (1 + totalReturnPercent / 100)
      const totalTrades = Math.floor(Math.random() * 300) + 20 // 20 to 320
      const winRate = Math.random() * 50 + 30 // 30% to 80%
      const winningTrades = Math.floor(totalTrades * winRate / 100)
      const losingTrades = totalTrades - winningTrades
      
      const mockResult = {
        totalReturn: finalCapital - config.initialCapital,
        totalReturnPercent,
        finalCapital,
        sharpeRatio: Math.random() * 3 + 0.2, // 0.2 to 3.2
        maxDrawdown: Math.random() * 30, // 0% to 30%
        winRate,
        totalTrades,
        winningTrades,
        losingTrades,
        avgWin: Math.random() * 500 + 100, // $100 to $600
        avgLoss: Math.random() * -300 - 50, // -$50 to -$350
        profitFactor: Math.random() * 2 + 0.5 // 0.5 to 2.5
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