import type { ProductStatus } from '@/types'
import { cn } from '@/lib/utils'

const statusStyles: Record<ProductStatus, string> = {
  draft: 'bg-yellow-100 text-yellow-800',
  released: 'bg-green-100 text-green-800',
  obsolete: 'bg-gray-100 text-gray-800',
}

interface StatusBadgeProps {
  status: ProductStatus
}

export function StatusBadge({ status }: StatusBadgeProps) {
  return (
    <span
      className={cn(
        'px-2 inline-flex text-xs leading-5 font-semibold rounded-full',
        statusStyles[status] ?? statusStyles.draft
      )}
    >
      {status}
    </span>
  )
}
