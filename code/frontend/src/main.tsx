import ReactDOM from 'react-dom/client'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import App from './App'
import './index.css'

const rootElement = document.getElementById('root')
if (!rootElement) throw new Error('Root element not found')

ReactDOM.createRoot(rootElement).render(
  <ErrorBoundary>
    <App />
  </ErrorBoundary>
)
