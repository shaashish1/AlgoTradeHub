import { NextRequest, NextResponse } from 'next/server'
import { pythonExecutor } from '@/lib/python-executor'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Execute trading operation using Python script
    const result = await pythonExecutor.executeTradingOperation('execute_order', body)
    
    if (result.success) {
      return NextResponse.json(result.data)
    } else {
      return NextResponse.json(
        { error: result.error },
        { status: 500 }
      )
    }
  } catch (error) {
    console.error('Trading execute API error:', error)
    return NextResponse.json(
      { error: 'Failed to execute trade' },
      { status: 500 }
    )
  }
}