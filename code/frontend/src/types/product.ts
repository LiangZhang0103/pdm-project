export type ProductStatus = 'draft' | 'active' | 'released' | 'archived' | 'obsolete'

export interface Product {
  id: string
  product_code: string
  name: string
  description: string | null
  category: string | null
  status: ProductStatus
  version: number
  created_by: string | null
  created_at: string
  updated_at: string
}

export interface ProductCreate {
  product_code: string
  name: string
  description?: string | null
  category?: string | null
  status?: ProductStatus
}

export interface ProductUpdate {
  product_code?: string
  name?: string
  description?: string | null
  category?: string | null
  status?: ProductStatus
}

export interface ProductFilters {
  category?: string
  status?: ProductStatus
}
