export interface HealthCheck {
  status: string
  database: boolean
  minio: boolean
  timestamp: string
}

export interface ApiError {
  detail: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  skip: number
  limit: number
}
