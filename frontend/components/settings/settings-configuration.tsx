"use client"

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Badge } from '@/components/ui/badge'
import { 
  Key, 
  Database, 
  Bell, 
  Shield,
  Server,
  Mail,
  Smartphone,
  Save,
  RefreshCw,
  AlertTriangle
} from 'lucide-react'
import { apiClient } from '@/lib/api'

export function SettingsConfiguration() {
  const [apiKeys, setApiKeys] = useState<Record<string, { key: string; secret: string; sandbox: boolean }>>({
    binance: { key: '', secret: '', sandbox: true },
    kraken: { key: '', secret: '', sandbox: false }
  })
  const [notifications, setNotifications] = useState({
    email: true,
    push: false,
    trades: true,
    alerts: true
  })
  const [trading, setTrading] = useState({
    maxPositions: 5,
    riskPerTrade: 2,
    stopLoss: 5,
    takeProfit: 10
  })
  const [isSaving, setIsSaving] = useState(false)

  const handleSaveSettings = async () => {
    setIsSaving(true)
    try {
      // Save settings via API
      console.log('Saving settings:', { apiKeys, notifications, trading })
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
    } catch (error) {
      console.error('Failed to save settings:', error)
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* API Keys */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Key className="h-5 w-5" />
            API Keys
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {Object.entries(apiKeys).map(([exchange, config]) => (
            <div key={exchange} className="space-y-3 p-4 border rounded-lg">
              <div className="flex items-center justify-between">
                <h3 className="font-medium capitalize">{exchange}</h3>
                <Badge variant={config.sandbox ? "secondary" : "default"}>
                  {config.sandbox ? "Sandbox" : "Live"}
                </Badge>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>API Key</Label>
                  <Input
                    type="password"
                    placeholder="Enter API key..."
                    value={config.key}
                    onChange={(e) => setApiKeys(prev => ({
                      ...prev,
                      [exchange]: { ...prev[exchange], key: e.target.value }
                    }))}
                  />
                </div>
                <div>
                  <Label>Secret Key</Label>
                  <Input
                    type="password"
                    placeholder="Enter secret key..."
                    value={config.secret}
                    onChange={(e) => setApiKeys(prev => ({
                      ...prev,
                      [exchange]: { ...prev[exchange], secret: e.target.value }
                    }))}
                  />
                </div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Trading Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            Trading Settings
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Max Positions</Label>
              <Input
                type="number"
                value={trading.maxPositions}
                onChange={(e) => setTrading(prev => ({ ...prev, maxPositions: parseInt(e.target.value) }))}
              />
            </div>
            <div>
              <Label>Risk Per Trade (%)</Label>
              <Input
                type="number"
                step="0.1"
                value={trading.riskPerTrade}
                onChange={(e) => setTrading(prev => ({ ...prev, riskPerTrade: parseFloat(e.target.value) }))}
              />
            </div>
            <div>
              <Label>Stop Loss (%)</Label>
              <Input
                type="number"
                step="0.1"
                value={trading.stopLoss}
                onChange={(e) => setTrading(prev => ({ ...prev, stopLoss: parseFloat(e.target.value) }))}
              />
            </div>
            <div>
              <Label>Take Profit (%)</Label>
              <Input
                type="number"
                step="0.1"
                value={trading.takeProfit}
                onChange={(e) => setTrading(prev => ({ ...prev, takeProfit: parseFloat(e.target.value) }))}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Notifications */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bell className="h-5 w-5" />
            Notifications
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Mail className="h-4 w-4" />
              <Label>Email Notifications</Label>
            </div>
            <Switch
              checked={notifications.email}
              onCheckedChange={(checked) => 
                setNotifications(prev => ({ ...prev, email: checked }))
              }
            />
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Smartphone className="h-4 w-4" />
              <Label>Push Notifications</Label>
            </div>
            <Switch
              checked={notifications.push}
              onCheckedChange={(checked) => 
                setNotifications(prev => ({ ...prev, push: checked }))
              }
            />
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Server className="h-4 w-4" />
              <Label>Trade Notifications</Label>
            </div>
            <Switch
              checked={notifications.trades}
              onCheckedChange={(checked) => 
                setNotifications(prev => ({ ...prev, trades: checked }))
              }
            />
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="h-4 w-4" />
              <Label>Alert Notifications</Label>
            </div>
            <Switch
              checked={notifications.alerts}
              onCheckedChange={(checked) => 
                setNotifications(prev => ({ ...prev, alerts: checked }))
              }
            />
          </div>
        </CardContent>
      </Card>

      {/* Save Settings */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-sm text-muted-foreground">
              <AlertTriangle className="h-4 w-4" />
              <span>Changes will be applied immediately</span>
            </div>
            <div className="flex space-x-2">
              <Button variant="outline">
                <RefreshCw className="h-4 w-4 mr-2" />
                Reset
              </Button>
              <Button onClick={handleSaveSettings} disabled={isSaving}>
                <Save className="h-4 w-4 mr-2" />
                {isSaving ? 'Saving...' : 'Save Settings'}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}