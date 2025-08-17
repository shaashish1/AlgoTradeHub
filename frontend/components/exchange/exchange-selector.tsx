'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { AlertCircle, CheckCircle, Settings, TrendingUp } from 'lucide-react'

interface Exchange {
  id: string
  name: string
  status: 'working' | 'partial' | 'failed'
  markets: number
  features: string[]
  notes: string
}

interface ExchangeConfig {
  apiKey: string
  apiSecret: string
  passphrase?: string
  sandbox: boolean
}

export default function ExchangeSelector() {
  const [selectedExchange, setSelectedExchange] = useState<string>('')
  const [exchanges, setExchanges] = useState<Exchange[]>([])
  const [config, setConfig] = useState<ExchangeConfig>({
    apiKey: '',
    apiSecret: '',
    passphrase: '',
    sandbox: true
  })
  const [isConfiguring, setIsConfiguring] = useState(false)
  const [testResult, setTestResult] = useState<string>('')

  // Load available exchanges from API
  useEffect(() => {
    const loadExchanges = async () => {
      try {
        const { apiClient } = await import('@/lib/api-client')
        const response = await apiClient.getAvailableExchanges()
        
        const exchangeData: Exchange[] = response.exchanges.map(ex => ({
          id: ex.id,
          name: ex.name,
          status: ex.status,
          markets: ex.markets,
          features: ex.features,
          notes: ex.notes
        }))
        
        setExchanges(exchangeData)
      } catch (error) {
        console.error('Failed to load exchanges:', error)
        // Fallback to mock data
        const mockExchanges: Exchange[] = [
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
        setExchanges(mockExchanges)
      }
    }
    
    loadExchanges()
  }, [])

  const handleExchangeSelect = (exchangeId: string) => {
    setSelectedExchange(exchangeId)
    setIsConfiguring(false)
    setTestResult('')
  }

  const handleConfigSave = async () => {
    if (!selectedExchange) return

    try {
      // Save configuration using API client
      const { apiClient } = await import('@/lib/api-client')
      const response = await apiClient.configureExchange(selectedExchange, config)

      if (response.success) {
        setTestResult('Configuration saved successfully!')
        setIsConfiguring(false)
      } else {
        setTestResult('Failed to save configuration')
      }
    } catch (error) {
      setTestResult('Error saving configuration')
    }
  }

  const handleTestConnection = async () => {
    if (!selectedExchange) return

    try {
      setTestResult('Testing connection...')
      
      // Test connection using API client
      const { apiClient } = await import('@/lib/api-client')
      const result = await apiClient.testExchangeConnection(selectedExchange, config)
      
      if (result.success) {
        setTestResult(`✅ Connection successful! ${result.markets || 0} markets available`)
      } else {
        setTestResult(`❌ Connection failed: ${result.error || 'Check your credentials.'}`)
      }
    } catch (error) {
      setTestResult('❌ Connection test failed')
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'working':
        return <Badge className="bg-green-100 text-green-800">✅ Working</Badge>
      case 'partial':
        return <Badge className="bg-yellow-100 text-yellow-800">⚠️ Partial</Badge>
      case 'failed':
        return <Badge className="bg-red-100 text-red-800">❌ Failed</Badge>
      default:
        return <Badge>Unknown</Badge>
    }
  }

  const selectedExchangeData = exchanges.find(ex => ex.id === selectedExchange)

  return (
    <div className="space-y-6">
      {/* Exchange Selection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Select Trading Exchange
          </CardTitle>
          <CardDescription>
            Choose your preferred exchange for crypto trading. Only working exchanges are shown.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4">
            <Label htmlFor="exchange-select">Available Exchanges</Label>
            <Select value={selectedExchange} onValueChange={handleExchangeSelect}>
              <SelectTrigger>
                <SelectValue placeholder="Select an exchange..." />
              </SelectTrigger>
              <SelectContent>
                {exchanges.filter(ex => ex.status === 'working').map((exchange) => (
                  <SelectItem key={exchange.id} value={exchange.id}>
                    <div className="flex items-center justify-between w-full">
                      <span>{exchange.name}</span>
                      <span className="text-sm text-gray-500 ml-2">
                        {exchange.markets.toLocaleString()} markets
                      </span>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Exchange Details */}
          {selectedExchangeData && (
            <div className="p-4 bg-gray-50 rounded-lg space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold">{selectedExchangeData.name}</h3>
                {getStatusBadge(selectedExchangeData.status)}
              </div>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium">Markets:</span> {selectedExchangeData.markets.toLocaleString()}
                </div>
                <div>
                  <span className="font-medium">Features:</span> {selectedExchangeData.features.join(', ')}
                </div>
              </div>
              <p className="text-sm text-gray-600">{selectedExchangeData.notes}</p>
              
              <div className="flex gap-2">
                <Button 
                  onClick={() => setIsConfiguring(true)}
                  className="flex items-center gap-2"
                >
                  <Settings className="h-4 w-4" />
                  Configure API
                </Button>
                <Button 
                  variant="outline"
                  onClick={handleTestConnection}
                  disabled={!config.apiKey || !config.apiSecret}
                >
                  Test Connection
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* API Configuration */}
      {isConfiguring && selectedExchangeData && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Settings className="h-5 w-5" />
              Configure {selectedExchangeData.name} API
            </CardTitle>
            <CardDescription>
              Enter your API credentials. These will be stored securely and used only for trading.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-4">
              <div>
                <Label htmlFor="api-key">API Key</Label>
                <Input
                  id="api-key"
                  type="password"
                  placeholder="Enter your API key"
                  value={config.apiKey}
                  onChange={(e) => setConfig({...config, apiKey: e.target.value})}
                />
              </div>
              
              <div>
                <Label htmlFor="api-secret">API Secret</Label>
                <Input
                  id="api-secret"
                  type="password"
                  placeholder="Enter your API secret"
                  value={config.apiSecret}
                  onChange={(e) => setConfig({...config, apiSecret: e.target.value})}
                />
              </div>

              {(selectedExchange === 'okx' || selectedExchange === 'bitget') && (
                <div>
                  <Label htmlFor="passphrase">Passphrase</Label>
                  <Input
                    id="passphrase"
                    type="password"
                    placeholder="Enter your passphrase"
                    value={config.passphrase}
                    onChange={(e) => setConfig({...config, passphrase: e.target.value})}
                  />
                </div>
              )}

              <div className="flex items-center space-x-2">
                <Switch
                  id="sandbox"
                  checked={config.sandbox}
                  onCheckedChange={(checked) => setConfig({...config, sandbox: checked})}
                />
                <Label htmlFor="sandbox">Use Sandbox Mode (Recommended for testing)</Label>
              </div>
            </div>

            <div className="flex gap-2">
              <Button onClick={handleConfigSave}>
                Save Configuration
              </Button>
              <Button variant="outline" onClick={() => setIsConfiguring(false)}>
                Cancel
              </Button>
            </div>

            {testResult && (
              <div className={`p-3 rounded-lg ${
                testResult.includes('✅') ? 'bg-green-50 text-green-800' : 
                testResult.includes('❌') ? 'bg-red-50 text-red-800' : 
                'bg-blue-50 text-blue-800'
              }`}>
                {testResult}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Quick Stats */}
      <Card>
        <CardHeader>
          <CardTitle>Exchange Status Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-green-600">5</div>
              <div className="text-sm text-gray-600">Working Exchanges</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-blue-600">6,485+</div>
              <div className="text-sm text-gray-600">Trading Pairs</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-purple-600">
                {selectedExchange ? '1' : '0'}
              </div>
              <div className="text-sm text-gray-600">Configured</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}