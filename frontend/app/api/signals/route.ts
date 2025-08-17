import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    // Generate mock signals for demo
    const symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'ADA/USDT', 'DOT/USDT']
    const indicators = ['RSI: 28', 'MACD: Bullish', 'BB: Oversold', 'SMA: Cross', 'Volume: High']
    
    const signals = []
    const numSignals = Math.floor(Math.random() * 3) + 1 // 1-3 signals
    
    for (let i = 0; i < numSignals; i++) {
      signals.push({
        symbol: symbols[Math.floor(Math.random() * symbols.length)],
        type: Math.random() > 0.5 ? 'BUY' : 'SELL',
        price: Math.random() * 30000 + 20000, // Random price between 20k-50k
        indicator: indicators[Math.floor(Math.random() * indicators.length)],
        strength: Math.floor(Math.random() * 25) + 70, // 70-95
        timestamp: new Date().toISOString()
      })
    }
    
    return NextResponse.json(signals)
  } catch (error) {
    console.error('Signals API error:', error)
    return NextResponse.json(
      { error: 'Failed to get signals' },
      { status: 500 }
    )
  }
}