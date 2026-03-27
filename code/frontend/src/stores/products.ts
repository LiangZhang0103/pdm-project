import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import { productsApi } from '@/api/products'
import type { Product, ProductFilters } from '@/types'

interface ProductsState {
  items: Product[]
  loading: boolean
  error: string | null
  filters: ProductFilters
  setFilters: (filters: ProductFilters) => void
  fetchProducts: () => Promise<void>
}

export const useProductsStore = create<ProductsState>()(
  devtools(
    (set, get) => ({
      items: [],
      loading: false,
      error: null,
      filters: {},

      setFilters: (filters) => {
        set({ filters })
        get().fetchProducts()
      },

      fetchProducts: async () => {
        set({ loading: true, error: null })
        try {
          const response = await productsApi.getAll(get().filters)
          set({ items: response.data, loading: false })
        } catch (err) {
          set({
            error: err instanceof Error ? err.message : 'Failed to load products',
            loading: false,
          })
        }
      },
    }),
    { name: 'products-store' }
  )
)
