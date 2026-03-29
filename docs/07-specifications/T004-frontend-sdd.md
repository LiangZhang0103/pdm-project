# T004: React前端基础框架 - SDD规格说明文档

## 文档信息

| 项目 | 内容 |
|------|------|
| 文档ID | SPEC-T004 |
| 版本 | v2.0.0 |
| 状态 | 已完成 |
| 创建日期 | 2026-03-29 |
| 最后更新 | 2026-03-29 |
| 关联任务 | T004 |

---

## 1. 概述

### 1.1 目的
本文档采用规格驱动开发（Specification-Driven Development, SDD）方法，定义React前端基础框架的功能需求、非功能需求、技术约束和验收标准。

### 1.2 范围
- React应用初始化
- 样式系统配置
- 路由管理
- API客户端
- 状态管理
- 类型系统

### 1.3 术语定义

| 术语 | 定义 |
|------|------|
| SDD | Specification-Driven Development，规格驱动开发 |
| FR | Functional Requirement，功能需求 |
| NFR | Non-Functional Requirement，非功能需求 |
| TC | Technical Constraint，技术约束 |

---

## 2. 功能需求规格

### FR-001: React应用初始化

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-001 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：创建React + TypeScript项目基础结构

**验收标准**：
- [x] AC-001.1: 使用Vite创建项目
- [x] AC-001.2: 配置TypeScript严格模式
- [x] AC-001.3: 应用可成功启动在 http://localhost:3000

**实现文件**：
- `/code/frontend/package.json`
- `/code/frontend/vite.config.ts`
- `/code/frontend/tsconfig.json`

---

### FR-002: 样式系统配置

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-002 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：集成Tailwind CSS作为主要样式方案

**验收标准**：
- [x] AC-002.1: Tailwind CSS正确配置
- [x] AC-002.2: 响应式断点正常工作
- [x] AC-002.3: 可在组件中使用tailwind类名

**实现文件**：
- `/code/frontend/tailwind.config.js`
- `/code/frontend/postcss.config.js`
- `/code/frontend/src/index.css`

---

### FR-003: 路由管理

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-003 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：实现前端路由管理，支持多页面导航

**验收标准**：
- [x] AC-003.1: React Router配置完成
- [x] AC-003.2: 至少有一个路由规则
- [x] AC-003.3: 404页面处理

**实现文件**：
- `/code/frontend/src/App.tsx`
- `/code/frontend/src/pages/NotFoundPage.tsx`

**实现代码**：
```typescript
// App.tsx - 404路由已配置
<Route path="*" element={<NotFoundPage />} />
```

---

### FR-004: API客户端

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-004 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：创建统一的HTTP客户端，处理API请求

**验收标准**：
- [x] AC-004.1: Axios实例配置
- [x] AC-004.2: 请求拦截器（添加Bearer Token）
- [x] AC-004.3: 响应拦截器（错误处理）
- [x] AC-004.4: 环境变量支持（`VITE_API_URL`）

**实现文件**：
- `/code/frontend/src/api/client.ts`
- `/code/frontend/src/api/products.ts`

**代码规格**：
```typescript
// API客户端配置
{
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
}
```

---

### FR-005: 状态管理

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-005 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：集成Zustand作为全局状态管理

**验收标准**：
- [x] AC-005.1: Zustand store创建
- [x] AC-005.2: DevTools集成
- [x] AC-005.3: 至少一个状态更新函数

**实现文件**：
- `/code/frontend/src/stores/products.ts`

**Store接口规格**：
```typescript
interface ProductsState {
  items: Product[]
  loading: boolean
  error: string | null
  filters: ProductFilters
  setFilters: (filters: ProductFilters) => void
  fetchProducts: () => Promise<void>
}
```

---

### FR-006: 错误边界

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-006 |
| **优先级** | P1 |
| **状态** | ✅ 已实现 |

**描述**：实现React错误边界组件

**验收标准**：
- [x] AC-006.1: ErrorBoundary组件实现
- [x] AC-006.2: 自定义fallback支持
- [x] AC-006.3: 在App.tsx中包裹应用

**实现文件**：
- `/code/frontend/src/components/ErrorBoundary.tsx`
- `/code/frontend/src/App.tsx`

**实现代码**：
```typescript
// App.tsx - ErrorBoundary已包裹整个应用
function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <Layout>
          <Routes>...</Routes>
        </Layout>
      </BrowserRouter>
    </ErrorBoundary>
  )
}
```

---

## 3. 非功能需求规格

### NFR-001: 类型安全

| 属性 | 值 |
|------|-----|
| **需求ID** | NFR-001 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：所有代码使用TypeScript类型

**验收标准**：
- [x] AC-N001.1: `tsconfig.json`严格模式开启
- [x] AC-N002.2: 无`any`类型使用
- [x] AC-N003.3: 类型定义完整（`src/types/`）

**TypeScript配置规格**：
```json
{
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "moduleResolution": "bundler"
  }
}
```

---

### NFR-002: 开发体验

| 属性 | 值 |
|------|-----|
| **需求ID** | NFR-002 |
| **优先级** | P1 |
| **状态** | ✅ 已实现 |

**描述**：提供良好的开发环境和工具支持

**验收标准**：
- [x] AC-N002.1: 热更新正常工作
- [x] AC-N002.2: 路径别名（`@/*`）配置
- [x] AC-N002.3: ESLint和Prettier配置（T008）

---

### NFR-003: 代码组织

| 属性 | 值 |
|------|-----|
| **需求ID** | NFR-003 |
| **优先级** | P1 |
| **状态** | ✅ 已实现 |

**描述**：采用模块化架构组织代码

**验收标准**：
- [x] AC-N003.1: 特性驱动开发结构
- [x] AC-N003.2: 组件、hooks、pages分离
- [x] AC-N003.3: 共享组件放在`components/`目录

---

## 4. 技术约束规格

### TC-001: 技术栈版本

| 技术 | 版本要求 | 实际版本 | 状态 |
|------|----------|----------|------|
| React | ^18.2.0 | 18.2.0 | ✅ |
| TypeScript | ^5.3.0 | 5.3.2 | ✅ |
| Vite | ^5.4.0 | 5.4.19 | ✅ |
| Tailwind CSS | ^3.3.0 | 3.3.6 | ✅ |
| Zustand | ^4.4.0 | 4.4.7 | ✅ |
| React Router | ^6.20.0 | 6.20.0 | ✅ |
| Axios | ^1.6.0 | 1.6.2 | ✅ |
| Lucide React | ^0.309.0 | 0.309.0 | ✅ |
| date-fns | ^3.0.0 | 3.0.6 | ✅ |

---

### TC-002: 项目结构规格

```
frontend/
├── src/
│   ├── api/                    # API层
│   │   ├── client.ts          # Axios实例 ✅
│   │   └── products.ts        # 产品API ✅
│   ├── components/            # 通用组件
│   │   ├── Layout.tsx         # 布局组件 ✅
│   │   ├── ErrorBoundary.tsx  # 错误边界 ✅
│   │   └── ui/                # UI组件库
│   │       └── StatusBadge.tsx ✅
│   ├── pages/                # 页面组件
│   │   └── NotFoundPage.tsx  # 404页面 ✅
│   ├── features/              # 功能模块
│   │   └── products/
│   │       ├── pages/         # 页面组件 ✅
│   │       ├── components/    # 功能组件 ✅
│   │       └── hooks/         # 自定义hooks ✅
│   ├── stores/                # Zustand stores ✅
│   ├── types/                 # TypeScript类型 ✅
│   ├── lib/                   # 工具函数 ✅
│   ├── App.tsx                # 应用入口 ✅
│   ├── main.tsx               # 渲染入口 ✅
│   └── index.css              # 全局样式 ✅
├── package.json               ✅
├── vite.config.ts             ✅
├── tsconfig.json              ✅
├── tailwind.config.js         ✅
└── postcss.config.js          ✅
```

---

## 5. 类型定义规格

### 5.1 ProductStatus枚举

**v1.1.0已修复**：前端已与后端保持5种状态一致

| 状态 | 后端 | 前端 | 状态 |
|------|------|------|------|
| draft | ✅ | ✅ | ✅ 匹配 |
| active | ✅ | ✅ | ✅ 匹配 |
| released | ✅ | ✅ | ✅ 匹配 |
| archived | ✅ | ✅ | ✅ 匹配 |
| obsolete | ✅ | ✅ | ✅ 匹配 |

**当前定义**（`types/product.ts`）：
```typescript
export type ProductStatus = 'draft' | 'active' | 'released' | 'archived' | 'obsolete'
```

### 5.2 完整类型规格

```typescript
// product.ts
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

// api.ts
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
```

---

## 6. 验收测试矩阵

| 需求ID | 验收标准 | 测试方法 | 状态 |
|--------|----------|----------|------|
| FR-001 | AC-001.1 | 检查package.json | ✅ |
| FR-001 | AC-001.2 | 检查tsconfig.json | ✅ |
| FR-001 | AC-001.3 | 启动开发服务器 | ✅ |
| FR-002 | AC-002.1 | 检查tailwind.config.js | ✅ |
| FR-002 | AC-002.2 | 测试响应式组件 | ✅ |
| FR-002 | AC-002.3 | 检查组件样式 | ✅ |
| FR-003 | AC-003.1 | 检查App.tsx | ✅ |
| FR-003 | AC-003.2 | 检查路由规则 | ✅ |
| FR-003 | AC-003.3 | 测试404路由 | ✅ 已实现 |
| FR-004 | AC-004.1 | 检查api/client.ts | ✅ |
| FR-004 | AC-004.2 | 检查请求拦截器 | ✅ |
| FR-004 | AC-004.3 | 检查响应拦截器 | ✅ |
| FR-004 | AC-004.4 | 测试环境变量 | ✅ |
| FR-005 | AC-005.1 | 检查stores/products.ts | ✅ |
| FR-005 | AC-005.2 | 检查devtools集成 | ✅ |
| FR-005 | AC-005.3 | 检查状态更新函数 | ✅ |
| FR-006 | AC-006.1 | 检查ErrorBoundary.tsx | ✅ |
| FR-006 | AC-006.2 | 测试fallback属性 | ✅ |
| FR-006 | AC-006.3 | 检查App.tsx包裹 | ✅ 已实现 |

---

## 7. 已知问题与改进计划

**v2.0.0状态**：所有已知问题均已修复，无待处理项。

### 7.1 历史问题（已关闭）

| 问题ID | 描述 | 影响 | 修复版本 | 状态 |
|--------|------|------|----------|------|
| BUG-001 | ProductStatus枚举不完整 | 状态显示错误 | v1.1.0 | ✅ 已关闭 |
| BUG-002 | ErrorBoundary未在App中使用 | 错误无法捕获 | v2.0.0 | ✅ 已关闭 |
| IMP-001 | 缺少404页面 | 用户体验 | v2.0.0 | ✅ 已关闭 |

---

## 8. 变更记录

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v1.0.0 | 2026-03-29 | 初始版本，基于代码审查创建SDD规格 |
| v1.1.0 | 2026-03-29 | 修复BUG-001（ProductStatus枚举完整） |
| v2.0.0 | 2026-03-29 | 修复BUG-002（ErrorBoundary包裹App）、IMP-001（404路由+NotFoundPage），所有验收标准通过 |

---

*本文档采用规格驱动开发（SDD）方法编写，作为T004任务的规格基准。*
