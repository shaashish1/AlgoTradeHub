import { NextRequest, NextResponse } from 'next/server'
import { pythonExecutor } from '@/lib/python-executor'

export async function POST(request: NextRequest) {
  try {
    // Get portfolio data from all configured exchanges
    const exchanges = ['binance', 'bybit', 'delta', 'gate', 'bitget']
    const result = await pythonExecutor.getPortfolioData(exchanges)
    
    if (result.success) {
      // Mock portfolio data for demo
      const mockData = {
        positions: [
          {
            symbol: 'BTC/USDT',
            exchange: 'binance',
            amount: 0.5,
            averagePrice: 42000,
            currentPrice: 43250,
            value: 21625,
            pnl: 625,
            pnlPercentage: 2.98
          },
          {
            symbol: 'ETH/USDT',
            exchange: 'bybit',
            amount: 8.2,
            averagePrice: 2700,
            currentPrice: 2650,
            value: 21730,
            pnl: -410,
            pnlPercentage: -1.85
          }
        ],
        balances: [
          {
            exchange: 'binance',
            totalValue: 35800,
            currencies: {'USDT': 15000, 'BTC': 0.5, 'BNB': 45},
            status: 'connected'
          },
          {
            exchange: 'bybit',
            totalValue: 21730,
            currencies: {'USDT': 5000, 'ETH': 8.2},
            status: 'connected'
          }
        ],
        totalValue: 57530,
        totalPnL: 215
      }
      
      return NextResponse.json(mockData)
    } else {
      return NextResponse.json(
        { error: result.error },
        { status: 500 }
      )
    }
  } catch (error) {
    console.error('Portfolio refresh API error:', error)
    return NextResponse.json(
      { error: 'Failed to refresh portfolio' },
      { status: 500 }
    )
  }
}