"use client"

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Checkbox } from '@/components/ui/checkbox'
import { 
  Building2, 
  Brain, 
  Shield, 
  Bell, 
  Palette,
  Database,
  Key,
  Smartphone,
  Settings2,
  Save,
  RefreshCw,
  CheckCircle,
  XCircle
} from 'lucide-react'

interface ExchangeConfig {
  name: string
  active: boolean
  mode: 'sandbox' | 'live'
  apiKey: string
  secret: string
  status: 'connected' | 'disconnected' | 'error'
  symbols: number
}

const mockExchanges: ExchangeConfig[] = [
  {
    name: 'Binance',
    active: true,
    mode: 'sandbox',
    apiKey: 'test_api_key_***',
    secret: 'test_secret_***',
    status: 'connected',
    symbols: 15
  },
  {
    name: 'Kraken',
    active: false,
    mode: 'live',
    apiKey: '',
    secret: '',
    status: 'disconnected',
    symbols: 0
  },
  {
    name: 'Delta',
    active: false,
    mode: 'sandbox',
    apiKey: '',
    secret: '',
    status: 'error',
    symbols: 0
  }
]

export function SettingsInterface() {
  const [activeTab, setActiveTab] = useState('exchanges')
  const [exchanges, setExchanges] = useState<ExchangeConfig[]>(mockExchanges)
  const [settings, setSettings] = useState({
    riskManagement: {
      maxRiskPerTrade: 2,
      maxPortfolioRisk: 6,
      maxDrawdown: 15,
      stopLoss: 3,
      takeProfit: 6
    },
    notifications: {
      emailAlerts: true,
      pushNotifications: false,
      tradingSignals: true,
      systemAlerts: true
    },
    strategy: {
      defaultStrategy: 'rsi_strategy',
      rsiPeriod: 14,
      rsiOverbought: 70,
      rsiOversold: 30,
      scanInterval: 5
    }
  })

  const tabs = [
    { id: 'exchanges', label: 'Exchanges', icon: Building2 },
    { id: 'strategies', label: 'Strategies', icon: Brain },
    { id: 'risk', label: 'Risk Management', icon: Shield },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'interface', label: 'Interface', icon: Palette },
    { id: 'data', label: 'Data Sources', icon: Database },
    { id: 'security', label: 'Security', icon: Key },
    { id: 'mobile', label: 'Mobile', icon: Smartphone }
  ]

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'connected':
        return <CheckCircle className="h-4 w-4 text-success" />
      case 'disconnected':
        return <XCircle className="h-4 w-4 text-muted-foreground" />
      case 'error':
        return <XCircle className="h-4 w-4 text-danger" />
      default:
        return <XCircle className="h-4 w-4 text-muted-foreground" />
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'connected':
        return <Badge variant="success">Connected</Badge>
      case 'disconnected':
        return <Badge variant="secondary">Disconnected</Badge>
      case 'error':
        return <Badge variant="destructive">Error</Badge>
      default:
        return <Badge variant="secondary">Unknown</Badge>
    }
  }

  const toggleExchange = (index: number) => {
    setExchanges(prev => prev.map((exchange, i) => 
      i === index ? { ...exchange, active: !exchange.active } : exchange
    ))
  }

  const saveSettings = () => {
    // Here you would save to backend
    console.log('Saving settings...', { exchanges, settings })
  }

  const testConnection = (exchangeName: string) => {
    // Here you would test the exchange connection
    console.log(`Testing connection to ${exchangeName}...`)
  }

  const renderExchangesTab = () => (
    <div className="space-y-6">
      <div className="grid gap-6 md:grid-cols-2">
        {exchanges.map((exchange, index) => (
          <Card key={exchange.name} className={exchange.active ? 'border-primary/50' : ''}>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(exchange.status)}
                  <div>
                    <CardTitle className="text-lg">{exchange.name}</CardTitle>
                    <p className="text-sm text-muted-foreground">
                      {exchange.symbols} symbols • {exchange.mode} mode
                    </p>
                  </div>
                </div>
                <div className="flex flex-col items-end space-y-2">
                  {getStatusBadge(exchange.status)}
                  <Checkbox
                    checked={exchange.active}
                    onCheckedChange={() => toggleExchange(index)}
                  />
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>API Key</Label>
                <Input
                  type="password"
                  value={exchange.apiKey}
                  placeholder="Enter API key"
                  onChange={(e) => {
                    const newExchanges = [...exchanges]
                    newExchanges[index].apiKey = e.target.value
                    setExchanges(newExchanges)
                  }}
                />
              </div>
              
              <div className="space-y-2">
                <Label>Secret Key</Label>
                <Input
                  type="password"
                  value={exchange.secret}
                  placeholder="Enter secret key"
                  onChange={(e) => {
                    const newExchanges = [...exchanges]
                    newExchanges[index].secret = e.target.value
                    setExchanges(newExchanges)
                  }}
                />
              </div>

              <div className="flex space-x-2">
                <Button 
                  variant="outline" 
                  size="sm"
                  onClick={() => testConnection(exchange.name)}
                >
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Test Connection
                </Button>
                <Button variant="outline" size="sm">
                  <Settings2 className="h-4 w-4 mr-2" />
                  Configure
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Global Exchange Settings</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center space-x-2">
            <Checkbox id="rate-limit" defaultChecked />
            <Label htmlFor="rate-limit">Enable rate limiting</Label>
          </div>
          <div className="flex items-center space-x-2">
            <Checkbox id="auto-reconnect" defaultChecked />
            <Label htmlFor="auto-reconnect">Auto-reconnect on disconnect</Label>
          </div>
          <div className="flex items-center space-x-2">
            <Checkbox id="sandbox-default" defaultChecked />
            <Label htmlFor="sandbox-default">Use sandbox mode by default</Label>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Timeout (seconds)</Label>
              <Input type="number" defaultValue="30" />
            </div>
            <div className="space-y-2">
              <Label>Max retries</Label>
              <Input type="number" defaultValue="3" />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderStrategiesTab = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Default Strategy Configuration</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Active Strategy</Label>
            <select 
              className="w-full p-2 border rounded-md"
              value={settings.strategy.defaultStrategy}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                strategy: { ...prev.strategy, defaultStrategy: e.target.value }
              }))}
            >
              <option value="rsi_strategy">RSI Strategy</option>
              <option value="macd_strategy">MACD Strategy</option>
              <option value="bollinger_strategy">Bollinger Bands</option>
              <option value="multi_indicator_strategy">Multi-Indicator</option>
            </select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>RSI Period</Label>
              <Input 
                type="number" 
                value={settings.strategy.rsiPeriod}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  strategy: { ...prev.strategy, rsiPeriod: parseInt(e.target.value) }
                }))}
              />
            </div>
            <div className="space-y-2">
              <Label>Scan Interval (seconds)</Label>
              <Input 
                type="number" 
                value={settings.strategy.scanInterval}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  strategy: { ...prev.strategy, scanInterval: parseInt(e.target.value) }
                }))}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>RSI Overbought</Label>
              <Input 
                type="number" 
                value={settings.strategy.rsiOverbought}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  strategy: { ...prev.strategy, rsiOverbought: parseInt(e.target.value) }
                }))}
              />
            </div>
            <div className="space-y-2">
              <Label>RSI Oversold</Label>
              <Input 
                type="number" 
                value={settings.strategy.rsiOversold}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  strategy: { ...prev.strategy, rsiOversold: parseInt(e.target.value) }
                }))}
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderRiskTab = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Risk Management Settings</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Max Risk per Trade (%)</Label>
              <Input 
                type="number" 
                step="0.1"
                value={settings.riskManagement.maxRiskPerTrade}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  riskManagement: { ...prev.riskManagement, maxRiskPerTrade: parseFloat(e.target.value) }
                }))}
              />
            </div>
            <div className="space-y-2">
              <Label>Max Portfolio Risk (%)</Label>
              <Input 
                type="number" 
                step="0.1"
                value={settings.riskManagement.maxPortfolioRisk}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  riskManagement: { ...prev.riskManagement, maxPortfolioRisk: parseFloat(e.target.value) }
                }))}
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label>Max Drawdown (%)</Label>
              <Input 
                type="number" 
                step="0.1"
                value={settings.riskManagement.maxDrawdown}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  riskManagement: { ...prev.riskManagement, maxDrawdown: parseFloat(e.target.value) }
                }))}
              />
            </div>
            <div className="space-y-2">
              <Label>Stop Loss (%)</Label>
              <Input 
                type="number" 
                step="0.1"
                value={settings.riskManagement.stopLoss}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  riskManagement: { ...prev.riskManagement, stopLoss: parseFloat(e.target.value) }
                }))}
              />
            </div>
            <div className="space-y-2">
              <Label>Take Profit (%)</Label>
              <Input 
                type="number" 
                step="0.1"
                value={settings.riskManagement.takeProfit}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  riskManagement: { ...prev.riskManagement, takeProfit: parseFloat(e.target.value) }
                }))}
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderNotificationsTab = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Notification Preferences</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center space-x-2">
            <Checkbox 
              id="email-alerts" 
              checked={settings.notifications.emailAlerts}
              onCheckedChange={(checked) => setSettings(prev => ({
                ...prev,
                notifications: { ...prev.notifications, emailAlerts: checked === true }
              }))}
            />
            <Label htmlFor="email-alerts">Email alerts for trades and signals</Label>
          </div>
          
          <div className="flex items-center space-x-2">
            <Checkbox 
              id="push-notifications" 
              checked={settings.notifications.pushNotifications}
              onCheckedChange={(checked) => setSettings(prev => ({
                ...prev,
                notifications: { ...prev.notifications, pushNotifications: checked === true }
              }))}
            />
            <Label htmlFor="push-notifications">Push notifications</Label>
          </div>
          
          <div className="flex items-center space-x-2">
            <Checkbox 
              id="trading-signals" 
              checked={settings.notifications.tradingSignals}
              onCheckedChange={(checked) => setSettings(prev => ({
                ...prev,
                notifications: { ...prev.notifications, tradingSignals: checked === true }
              }))}
            />
            <Label htmlFor="trading-signals">Trading signal notifications</Label>
          </div>
          
          <div className="flex items-center space-x-2">
            <Checkbox 
              id="system-alerts" 
              checked={settings.notifications.systemAlerts}
              onCheckedChange={(checked) => setSettings(prev => ({
                ...prev,
                notifications: { ...prev.notifications, systemAlerts: checked === true }
              }))}
            />
            <Label htmlFor="system-alerts">System alerts and errors</Label>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderTabContent = () => {
    switch (activeTab) {
      case 'exchanges':
        return renderExchangesTab()
      case 'strategies':
        return renderStrategiesTab()
      case 'risk':
        return renderRiskTab()
      case 'notifications':
        return renderNotificationsTab()
      default:
        return (
          <Card>
            <CardContent className="pt-6">
              <div className="text-center py-8">
                <Settings2 className="h-16 w-16 mx-auto mb-4 text-muted-foreground opacity-50" />
                <h3 className="text-lg font-medium mb-2">{tabs.find(t => t.id === activeTab)?.label}</h3>
                <p className="text-muted-foreground">
                  This section is coming soon!
                </p>
              </div>
            </CardContent>
          </Card>
        )
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-4">
      {/* Sidebar */}
      <div className="space-y-2 lg:col-span-1">
        <Card>
          <CardHeader>
            <CardTitle>Settings Categories</CardTitle>
          </CardHeader>
          <CardContent className="space-y-1">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <Button
                  key={tab.id}
                  variant={activeTab === tab.id ? "default" : "ghost"}
                  className="w-full justify-start"
                  onClick={() => setActiveTab(tab.id)}
                >
                  <Icon className="h-4 w-4 mr-2" />
                  {tab.label}
                </Button>
              )
            })}
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <div className="space-y-6 lg:col-span-3">
        {renderTabContent()}
        
        {/* Save Button */}
        <div className="flex justify-end">
          <Button onClick={saveSettings}>
            <Save className="h-4 w-4 mr-2" />
            Save Settings
          </Button>
        </div>
      </div>
    </div>
  )
}