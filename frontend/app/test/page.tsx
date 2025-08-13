import { Header } from '@/components/layout/header'
import { TestInterface } from '@/components/test/test-interface'

export default function TestPage() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container mx-auto px-4 py-6">
        <div className="space-y-6">
          {/* Header */}
          <div>
            <h1 className="text-3xl font-bold tracking-tight">🧪 Test Interface</h1>
            <p className="text-muted-foreground">
              Test backend connectivity and run feature demonstrations
            </p>
          </div>

          {/* Test Interface */}
          <TestInterface />
        </div>
      </main>
    </div>
  )
}