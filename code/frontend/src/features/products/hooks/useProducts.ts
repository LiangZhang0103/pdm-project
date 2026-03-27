import { useEffect } from 'react'
import { useProductsStore } from '@/stores/products'

export function useProducts() {
  const { items, loading, error, filters, setFilters, fetchProducts } = useProductsStore()

  useEffect(() => {
    fetchProducts()
  }, [fetchProducts])

  return { products: items, loading, error, filters, setFilters, refetch: fetchProducts }
}
