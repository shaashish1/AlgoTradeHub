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
import { api } from '@/lib/api'

export function SettingsConfiguration() {
  const [apiKeys, setApiKeys] = useState({
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
      await api.saveConfig({
        apiKeys,
        notifications,
        trading
      })
    } catch (error) {
      console.error('Failed to save settings:', error)
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* API Configuration */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Key className="h-5 w-5" />
            <span>🔑 Exchange API Keys</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Binance */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium">Binance</h3>
              <div className="flex items-center space-x-2">
                <Badge variant={apiKeys.binance.sandbox ? "secondary" : "default"}>
                  {apiKeys.binance.sandbox ? "Sandbox" : "Live"}
                </Badge>
                <Switch
                  checked={apiKeys.binance.sandbox}
                  onCheckedChange={(checked) => 
                    setApiKeys(prev => ({
                      ...prev,
                      binance: { ...prev.binance, sandbox: checked }
                    }))
                  }
                />
              </div>
            </div>
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="binance-key">API Key</Label>
                <Input
                  id="binance-key"
                  type="password"
                  placeholder="Enter Binance API key"
                  value={apiKeys.binance.key}
                  onChange={(e) => 
                    setApiKeys(prev => ({
                      ...prev,
                      binance: { ...prev.binance, key: e.target.value }
                    }))
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="binance-secret">Secret Key</Label>
                <Input
                  id="binance-secret"
                  type="password"
                  placeholder="Enter Binance secret key"
                  value={apiKeys.binance.secret}
                  onChange={(e) => 
                    setApiKeys(prev => ({
                      ...prev,
                      binance: { ...prev.binance, secret: e.target.value }
                    }))
                  }
                />
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}    
  {/* Trading Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Shield className="h-5 w-5" />
            <span>🛡️ Trading Settings</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <div className="space-y-2">
              <Label htmlFor="max-positions">Max Positions</Label>
              <Input
                id="max-positions"
                type="number"
                value={trading.maxPositions}
                onChange={(e) => 
                  setTrading(prev => ({ ...prev, maxPositions: Number(e.target.value) }))
                }
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="risk-per-trade">Risk per Trade (%)</Label>
              <Input
                id="risk-per-trade"
                type="number"
                step="0.1"
                value={trading.riskPerTrade}
                onChange={(e) => 
                  setTrading(prev => ({ ...prev, riskPerTrade: Number(e.target.value) }))
                }
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="stop-loss">Stop Loss (%)</Label>
              <Input
                id="stop-loss"
                type="number"
                step="0.1"
                value={trading.stopLoss}
                onChange={(e) => 
                  setTrading(prev => ({ ...prev, stopLoss: Number(e.target.value) }))
                }
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="take-profit">Take Profit (%)</Label>
              <Input
                id="take-profit"
                type="number"
                step="0.1"
                value={trading.takeProfit}
                onChange={(e) => 
                  setTrading(prev => ({ ...prev, takeProfit: Number(e.target.value) }))
                }
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Notifications */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Bell className="h-5 w-5" />
            <span>🔔 Notifications</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Email Notifications</Label>
                <p className="text-sm text-muted-foreground">Receive alerts via email</p>
              </div>
              <Switch
                checked={notifications.email}
                onCheckedChange={(checked) => 
                  setNotifications(prev => ({ ...prev, email: checked }))
                }
              />
            </div>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Push Notifications</Label>
                <p className="text-sm text-muted-foreground">Browser push notifications</p>
              </div>
              <Switch
                checked={notifications.push}
                onCheckedChange={(checked) => 
                  setNotifications(prev => ({ ...prev, push: checked }))
                }
              />
            </div>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Trade Notifications</Label>
                <p className="text-sm text-muted-foreground">Alerts for executed trades</p>
              </div>
              <Switch
                checked={notifications.trades}
                onCheckedChange={(checked) => 
                  setNotifications(prev => ({ ...prev, trades: checked }))
                }
              />
            </div>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Signal Alerts</Label>
                <p className="text-sm text-muted-foreground">Notifications for trading signals</p>
              </div>
              <Switch
                checked={notifications.alerts}
                onCheckedChange={(checked) => 
                  setNotifications(prev => ({ ...prev, alerts: checked }))
                }
              />
            </div>
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