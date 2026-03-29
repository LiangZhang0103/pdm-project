import { api } from './client'
import type { Product, ProductCreate, ProductUpdate, ProductFilters } from '@/types'

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  skip: number
  limit: number
}

export const productsApi = {
  getAll: (filters?: ProductFilters & { skip?: number; limit?: number }) => {
    const params = new URLSearchParams()
    if (filters?.category) params.set('category', filters.category)
    if (filters?.status) params.set('status', filters.status)
    if (filters?.skip !== undefined) params.set('skip', String(filters.skip))
    if (filters?.limit !== undefined) params.set('limit', String(filters.limit))
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
