import { NextRequest, NextResponse } from 'next/server'
import { pythonExecutor } from '@/lib/python-executor'

export async function GET(
  request: NextRequest,
  { params }: { params: { exchange: string } }
) {
  try {
    const { exchange } = params
    
    // Get balance using Python script
    const result = await pythonExecutor.executeExchangeOperation('get_balance', exchange)
    
    if (result.success) {
      return NextResponse.json(result.data?.balance || {})
    } else {
      return NextResponse.json(
        { error: result.error },
        { status: 500 }
      )
    }
  } catch (error) {
    console.error('Trading balance API error:', error)
    return NextResponse.json(
      { error: 'Failed to get balance' },
      { status: 500 }
    )
  }
}