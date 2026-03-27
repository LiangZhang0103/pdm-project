import { RefreshCw } from 'lucide-react'
import { useProducts } from '../hooks/useProducts'
import { ProductTable } from '../components/ProductTable'

export default function ProductListPage() {
  const { products, loading, error, refetch } = useProducts()

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Products</h2>
        <button
          onClick={refetch}
          disabled={loading}
          aria-busy={loading}
          aria-label="Refresh products list"
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors inline-flex items-center gap-2"
        >
          <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          <span>{loading ? 'Loading...' : 'Refresh'}</span>
        </button>
      </div>

      {error && (
        <div role="alert" aria-live="polite" className="mb-4 p-4 bg-red-50 border border-red-200 rounded text-red-700">
          <p className="font-medium">Error loading products</p>
          <p className="text-sm mt-1">{error}</p>
        </div>
      )}

      {loading && products.length === 0 ? (
        <div className="text-center py-12 text-gray-500" aria-live="polite">
          <RefreshCw className="h-8 w-8 mx-auto mb-4 animate-spin" />
          <p>Loading products...</p>
        </div>
      ) : (
        <ProductTable products={products} />
      )}
    </div>
  )
}
