import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    // Return working crypto exchanges
    const workingExchanges = [
      {
        id: 'binance',
        name: 'Binance',
        status: 'working',
        markets: 2069,
        features: ['Spot', 'Futures', 'Options'],
        notes: 'Full sandbox support'
      },
      {
        id: 'bybit',
        name: 'Bybit',
        status: 'working',
        markets: 2490,
        features: ['Spot', 'Derivatives'],
        notes: 'Full sandbox support'
      },
      {
        id: 'delta',
        name: 'Delta Exchange',
        status: 'working',
        markets: 552,
        features: ['Spot', 'Futures (INR)'],
        notes: 'Indian exchange'
      },
      {
        id: 'gate',
        name: 'Gate.io',
        status: 'working',
        markets: 1329,
        features: ['Spot', 'Futures'],
        notes: 'Good market coverage'
      },
      {
        id: 'bitget',
        name: 'Bitget',
        status: 'working',
        markets: 45,
        features: ['Spot', 'Futures'],
        notes: 'Limited markets'
      }
    ]
    
    return NextResponse.json({
      exchanges: workingExchanges,
      total_working: workingExchanges.length,
      total_markets: workingExchanges.reduce((sum, ex) => sum + ex.markets, 0)
    })
  } catch (error) {
    console.error('Exchanges available API error:', error)
    return NextResponse.json(
      { error: 'Failed to get available exchanges' },
      { status: 500 }
    )
  }
}