import { format } from 'date-fns'
import type { Product } from '@/types'
import { StatusBadge } from '@/components/ui/StatusBadge'

interface ProductTableProps {
  products: Product[]
}

export function ProductTable({ products }: ProductTableProps) {
  if (products.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p className="text-lg">No products found</p>
      </div>
    )
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200" aria-label="Products list">
        <thead className="bg-gray-50">
          <tr>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Code
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Name
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Category
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Status
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Version
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Created
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {products.map((product) => (
            <tr key={product.id} className="hover:bg-gray-50 transition-colors">
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {product.product_code}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {product.name}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {product.category || '-'}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <StatusBadge status={product.status} />
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                v{product.version}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <time dateTime={product.created_at}>
                  {format(new Date(product.created_at), 'yyyy-MM-dd HH:mm')}
                </time>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
