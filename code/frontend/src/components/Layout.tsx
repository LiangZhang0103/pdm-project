import { type ReactNode } from 'react'
import { Package } from 'lucide-react'

interface LayoutProps {
  children: ReactNode
}

export function Layout({ children }: LayoutProps) {
  const title = import.meta.env.VITE_APP_TITLE || 'PDM System'

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-3">
          <Package className="h-7 w-7 text-blue-600" />
          <h1 className="text-xl font-bold text-gray-900">{title}</h1>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-6 py-8">
        {children}
      </main>
    </div>
  )
}
