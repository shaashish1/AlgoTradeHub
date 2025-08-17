import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    // Mock scanner stop
    return NextResponse.json({
      success: true,
      message: 'Scanner stopped successfully',
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    console.error('Scanner stop API error:', erro