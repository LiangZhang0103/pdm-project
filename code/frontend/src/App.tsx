import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Layout } from '@/components/Layout'
import ProductListPage from '@/features/products/pages/ProductListPage'

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<ProductListPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
