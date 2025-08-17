import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    // Mock scanner start
    return NextResponse.json({
      success: true,
      message: 'Scanner started successfully',
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    console.error('Scanner start API error:', error)
    return NextResponse.json(
      { error: 'Failed to start scanner' },
      { status: 500 }
    )
  }
}