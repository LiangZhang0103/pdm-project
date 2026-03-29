# PDM 共享数据字典

## 文档信息

| 项目 | 内容 |
|------|------|
| 文档ID | SPEC-DD-001 |
| 版本 | v1.0.0 |
| 状态 | 已发布 |
| 创建日期 | 2026-03-29 |
| 用途 | SDD文档间共享的统一定义参考 |

---

## 1. 目的

本文档为所有SDD规格说明文档提供**统一的数据定义参考**，避免各文档重复定义导致的不一致问题。所有SDD文档中涉及以下共享概念时，应引用本文档作为权威来源。

---

## 2. 枚举类型定义

### 2.1 ProductStatus（产品状态）

| 状态值 | 中文名称 | 说明 | 后端定义 | 前端定义 |
|--------|----------|------|----------|----------|
| `draft` | 草稿 | 产品初始状态，尚未发布 | `models.py` ProductStatus.DRAFT | `product.ts` ProductStatus |
| `active` | 活跃 | 产品正在使用中 | `models.py` ProductStatus.ACTIVE | `product.ts` ProductStatus |
| `released` | 已发布 | 产品已正式发布 | `models.py` ProductStatus.RELEASED | `product.ts` ProductStatus |
| `archived` | 已归档 | 产品已归档，不再活跃 | `models.py` ProductStatus.ARCHIVED | `product.ts` ProductStatus |
| `obsolete` | 已废弃 | 产品已废弃，不再使用 | `models.py` ProductStatus.OBSOLETE | `product.ts` ProductStatus |

**后端实现**（`models.py`）：
```python
class ProductStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RELEASED = "released"
    ARCHIVED = "archived"
    OBSOLETE = "obsolete"
```

**后端Schema**（`schemas.py`）：
```python
ProductStatus = Literal["draft", "active", "released", "archived", "obsolete"]
```

**前端类型**（`types/product.ts`）：
```typescript
export type ProductStatus = 'draft' | 'active' | 'released' | 'archived' | 'obsolete'
```

### 2.2 UserRole（用户角色）

| 角色值 | 中文名称 | 说明 | 后端定义 |
|--------|----------|------|----------|
| `user` | 普通用户 | 标准用户权限 | `models.py` UserRole.USER |
| `admin` | 管理员 | 系统管理员权限 | `models.py` UserRole.ADMIN |

**后端实现**（`models.py`）：
```python
class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"
```

### 2.3 DocumentStatus（文档状态）

| 状态值 | 中文名称 | 说明 | 默认值 |
|--------|----------|------|--------|
| `active` | 活跃 | 文档正常状态 | ✅ 默认 |
| `archived` | 已归档 | 文档已归档 | - |

**定义位置**：`models.py` Document模型 `status` 字段，默认值 `"active"`

---

## 3. 通用数据类型

### 3.1 UUID标识符

| 属性 | 值 |
|------|-----|
| 类型 | UUID v4 |
| 生成方式 | `gen_random_uuid()`（PostgreSQL）/ `uuid.uuid4`（Python） |
| 存储类型 | PostgreSQL `UUID` / TypeScript `string` |
| 用途 | 所有实体的主键 |

### 3.2 时间戳格式

| 属性 | 值 |
|------|-----|
| 类型 | `datetime`（Python）/ `string`（TypeScript） |
| 格式 | ISO 8601（`2026-03-29T10:00:00Z`） |
| 自动生成 | `created_at` 默认 `now()` |
| 自动更新 | `updated_at` 默认 `now()`，`onupdate=now()` |

---

## 4. SDD通用术语

以下术语在所有SDD文档中统一使用，无需在各文档中重复定义：

| 术语 | 英文全称 | 定义 |
|------|----------|------|
| SDD | Specification-Driven Development | 规格驱动开发，先定义规格再实现的开发方法 |
| FR | Functional Requirement | 功能需求，描述系统应具备的功能 |
| NFR | Non-Functional Requirement | 非功能需求，描述系统的质量属性 |
| AC | Acceptance Criteria | 验收标准，用于验证需求是否满足 |
| TC | Technical Constraint | 技术约束，限制技术选择的条件 |
| P0/P1/P2 | Priority Level | 需求优先级，P0最高、P2最低 |

---

## 5. API通用规范

### 5.1 分页参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `skip` | integer | 0 | 跳过记录数 |
| `limit` | integer | 100 | 每页最大记录数 |

### 5.2 通用响应格式

```json
{
  "items": [],
  "total": 0,
  "skip": 0,
  "limit": 100
}
```

### 5.3 错误响应格式

```json
{
  "detail": "错误描述信息"
}
```

---

## 6. 技术栈版本（权威来源）

| 技术 | 版本要求 | 实际版本 | 定义位置 |
|------|----------|----------|----------|
| Python | ^3.11 | 3.11.x | Dockerfile |
| FastAPI | ^0.104.0 | 0.104.1 | requirements.txt |
| SQLAlchemy | ^2.0.0 | 2.0.36 | requirements.txt |
| React | ^18.2.0 | 18.2.0 | package.json |
| TypeScript | ^5.3.0 | 5.3.2 | package.json |
| Vite | ^5.4.0 | 5.4.19 | package.json |
| Tailwind CSS | ^3.3.0 | 3.3.6 | package.json |
| Zustand | ^4.4.0 | 4.4.7 | package.json |
| React Router | ^6.20.0 | 6.20.0 | package.json |
| Axios | ^1.6.0 | 1.6.2 | package.json |

---

## 7. 引用关系

以下SDD文档引用本数据字典：

| SDD文档 | 引用内容 |
|---------|----------|
| T001-github-repo-sdd.md | 术语定义 |
| T002-docker-env-sdd.md | 术语定义、技术栈版本 |
| T003-fastapi-framework-sdd.md | 术语定义、技术栈版本 |
| T004-frontend-sdd.md | 术语定义、ProductStatus、技术栈版本 |
| T005-data-model-sdd.md | 术语定义、ProductStatus、UserRole、DocumentStatus、UUID |
| T006-product-api-sdd.md | 术语定义、ProductStatus、分页参数、响应格式 |
| T007-frontend-products-sdd.md | 术语定义、ProductStatus |
| T008-code-quality-sdd.md | 术语定义、技术栈版本 |
| T009-testing-sdd.md | 术语定义 |
| T010-api-docs-sdd.md | 术语定义 |

---

## 8. 变更记录

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v1.0.0 | 2026-03-29 | 初始版本，提取全SDD共享定义为统一数据字典 |

---

*本文档为PDM项目所有SDD规格说明文档的共享参考基准。*
