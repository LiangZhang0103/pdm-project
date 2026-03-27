import { api } from './client'
import type { Product, ProductCreate, ProductUpdate, ProductFilters } from '@/types'

export const productsApi = {
  getAll: (filters?: ProductFilters) => {
    const params = new URLSearchParams()
    if (filters?.category) params.set('category', filters.category)
    if (filters?.status) params.set('status', filters.status)
    const query = params.toString()
    return api.get<Product[]>(`/products/${query ? `?${query}` : ''}`)
  },

  getById: (id: string) =>
    api.get<Product>(`/products/${id}`),

  create: (data: ProductCreate) =>
    api.post<Product>('/products/', data),

  update: (id: string, data: ProductUpdate) =>
    api.put<Product>(`/products/${id}`, data),

  delete: (id: string) =>
    api.delete(`/products/${id}`),
}
