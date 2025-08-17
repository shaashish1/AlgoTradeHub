import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    // Mock positions data
    const positions = [
      {
        symbol: 'BTC/USDT',
        side: 'BUY',
        entryPrice: 42000,
        currentPrice: 43250,
        quantity: 0.5,
        pnl: 625,
        pnlPercentage: 2.98,
        timestamp: new Date(Date.now() - 3600000).toISOString() // 1 hour ago
      },
      {
        symbol: 'ETH/USDT',
        side: 'BUY',
        entryPrice: 2700,
        currentPrice: 2650,
        quantity: 8.2,
        pnl: -410,
        pnlPercentage: -1.85,
        timestamp: new Date(Date.now() - 7200000).toISOString() // 2 hours ago
      },
      {
        symbol: 'SOL/USDT',
        side: 'SELL',
        entryPrice: 100,
        currentPrice: 98.45,
        quantity: 120,
        pnl: 186,
        pnlPercentage: 1.55,
        timestamp: new Date(Date.now() - 1800000).toISOString() // 30 minutes ago
      }
    ]
    
    return NextResponse.json(positions)
  } catch (error) {
    console.error('Positions API error:', error)
    return NextResponse.json(
      { error: 'Failed to get positions' },
      { status: 500 }
    )
  }
}