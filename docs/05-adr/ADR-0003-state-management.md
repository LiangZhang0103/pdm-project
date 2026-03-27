# ADR-0003: 前端状态管理选型

## ADR 信息

| 属性 | 值 |
|------|-----|
| 编号 | ADR-0003 |
| 标题 | 前端状态管理: Zustand + React Query |
| 状态 | 已通过 (Accepted) |
| 日期 | 2026-03-27 |
| 决策者 | 项目所有者 |

---

## 1. 背景

前端需要管理两种类型的状态：服务器状态 (API数据) 和客户端状态 (UI状态)。需要选择合适的状态管理方案。

## 2. 考虑选项

### 选项 A: Redux Toolkit
- **优点**:
  - 功能强大
  - 生态完善
  - DevTools强大
- **缺点**:
  - 学习曲线陡峭
  - 代码量大
  - 过度设计

### 选项 B: Zustand
- **优点**:
  - 简单轻量
  - API简洁
  - 体积小
  - TypeScript友好
- **缺点**:
  - 社区较小
  - 功能相对简单

### 选项 C: React Context + useState
- **优点**:
  - 原生方案
  - 无额外依赖
- **缺点**:
  - 性能问题 (频繁重渲染)
  - 不适合复杂状态

### 选项 D: React Query + Context
- **优点**:
  - 专注服务器状态
  - 内置缓存
  - 自动重试
- **缺点**:
  - 仅处理服务器状态

## 3. 决策

**选择**: Zustand (客户端状态) + React Query (服务器状态)

**理由**:
1. Zustand - 简洁API，易于学习，适合本项目规模
2. React Query - 处理服务器状态的标准方案，内置缓存和同步
3. 组合 - 职责分离，各司其职
4. 学习价值 - 两个都是现代React推荐方案

## 4. 实现规范

### Zustand使用场景
- 用户登录状态
- UI主题设置
- 侧边栏展开状态
- 表单临时数据

### React Query使用场景
- 产品列表数据
- 文档列表
- API响应缓存

### 代码示例
```typescript
// stores/products.ts - Zustand
interface ProductStore {
  products: Product[]
  setProducts: (products: Product[]) => void
}

export const useProductStore = create<ProductStore>((set) => ({
  products: [],
  setProducts: (products) => set({ products })
}))

// hooks/useProducts.ts - React Query
export function useProducts() {
  return useQuery({
    queryKey: ['products'],
    queryFn: fetchProducts
  })
}
```

## 5. 后果

### 正面
- 代码简洁
- 学习曲线平缓
- 职责清晰
- 性能优化内置

### 负面
- 需要管理两个库
- 团队经验可能不足

## 6. 相关文档

- 技术栈: `/resources/tech-stack.md`
- 系统架构: `/docs/architecture/system-architecture.md`

---

*状态: 已通过 - 2026-03-27*
*审查周期: 12个月或重大变更时*