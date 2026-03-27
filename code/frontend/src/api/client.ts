import axios, { AxiosError, type AxiosInstance } from 'axios'

const createApiClient = (): AxiosInstance => {
  const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    headers: {
      'Content-Type': 'application/json',
    },
    timeout: 10000,
  })

  api.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('authToken')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    (error) => Promise.reject(error)
  )

  api.interceptors.response.use(
    (response) => response,
    (error: AxiosError<{ detail?: string }>) => {
      if (error.response) {
        switch (error.response.status) {
          case 401:
            localStorage.removeItem('authToken')
            console.error('Unauthorized - please login again')
            break
          case 403:
            console.error('Forbidden - insufficient permissions')
            break
          case 404:
            console.error('Resource not found')
            break
          case 500:
            console.error('Server error - please try again later')
            break
        }
      } else if (error.request) {
        console.error('Network error - please check your connection')
      }
      return Promise.reject(error)
    }
  )

  return api
}

export const api = createApiClient()
