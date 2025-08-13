import { Header } from '@/components/layout/header'
import { SettingsConfiguration } from '@/components/settings/settings-configuration'

export default function SettingsPage() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container mx-auto px-4 py-6">
        <div className="space-y-6">
          {/* Header */}
          <div>
            <h1 className="text-3xl font-bold tracking-tight">⚙️ Settings & Configuration</h1>
            <p className="text-muted-foreground">
              Manage your trading preferences, API keys, and system settings
            </p>
          </div>

          {/* Settings Interface */}
          <SettingsConfiguration />
        </div>
      </main>
    </div>
  )
}