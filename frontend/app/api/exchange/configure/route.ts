import { NextRequest, NextResponse } from 'next/server'
import { pythonExecutor } from '@/lib/python-executor'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { exchange, config } = body
    
    // Test exchange connection with provided credentials
    const result = await pythonExecutor.executeExchangeOperation('test_connection', exchange, config)
    
    if (result.success) {
      // In a real implementation, you would save the credentials securely here
      return NextResponse.json({
        success: true,
        message: `${exchange} configured successfully`,
        exchange: exchange
      })
    } else {
      return NextResponse.json(
        { error: result.error || 'Failed to configure exchange' },
        { status: 400 }
      )
    }
  } catch (error) {
    console.error('Exchange configure API error:', error)
    return NextResponse.json(
      { error: 'Failed to configure exchange' },
      { status: 500 }
    )
  }
}