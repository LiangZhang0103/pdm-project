# T005: 产品数据模型设计 - SDD规格说明文档

## 文档信息

| 项目 | 内容 |
|------|------|
| 文档ID | SPEC-T005 |
| 版本 | v1.0.0 |
| 状态 | 已完成 |
| 创建日期 | 2026-03-29 |
| 关联任务 | T005 |
| 完成日期 | 2026-03-27 |

---

## 1. 概述

### 1.1 目的
定义PDM系统的数据模型层，包括SQLAlchemy ORM模型、Pydantic验证模式和数据库初始化脚本。

### 1.2 范围
- SQLAlchemy ORM模型（Product, Document, BOMItem, User）
- Pydantic请求/响应模式
- 数据库初始化SQL脚本
- 枚举类型定义
- 索引策略

---

## 2. 功能需求规格

### FR-001: Product数据模型

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-001 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：定义产品核心数据表

**验收标准**：
- [x] AC-001.1: UUID主键（自动生成）
- [x] AC-001.2: `product_code` 唯一约束，长度≤50
- [x] AC-001.3: `name` 必填，长度≤200
- [x] AC-001.4: `description` 可选文本字段
- [x] AC-001.5: `category` 可选，长度≤100
- [x] AC-001.6: `status` 枚举（draft/active/released/archived/obsolete），默认draft
- [x] AC-001.7: `version` 整数，默认1
- [x] AC-001.8: 自动时间戳（created_at, updated_at）

**字段规格**：

| 字段 | 类型 | 约束 | 默认值 |
|------|------|------|--------|
| id | UUID | PK | gen_random_uuid() |
| product_code | String(50) | UNIQUE NOT NULL | - |
| name | String(200) | NOT NULL | - |
| description | Text | NULL | - |
| category | String(100) | NULL | - |
| version | Integer | - | 1 |
| status | String(50) | - | "draft" |
| created_by | String(100) | NULL | - |
| created_at | DateTime | - | now() |
| updated_at | DateTime | - | now(), onupdate=now() |

---

### FR-002: Document数据模型

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-002 |
| **优先级** | P1 |
| **状态** | ✅ 已实现 |

**描述**：定义文档管理数据表，关联产品

**验收标准**：
- [x] AC-002.1: UUID主键
- [x] AC-002.2: 外键关联 `products.id`（CASCADE删除）
- [x] AC-002.3: 文件元数据（filename, filepath, file_size, mime_type）
- [x] AC-002.4: JSON元数据列（doc_metadata）
- [x] AC-002.5: OCR文本存储字段（ocr_text）
- [x] AC-002.6: 向量嵌入字段（embedding），用于AI语义搜索

**完整字段规格**：

| 字段 | 类型 | 约束 | 默认值 |
|------|------|------|--------|
| id | UUID | PK | gen_random_uuid() |
| filename | String(255) | NOT NULL | - |
| filepath | String(500) | NULL | - |
| file_size | Integer | NULL | - |
| mime_type | String(100) | NULL | - |
| product_id | UUID | FK→products(id) CASCADE | - |
| version | Integer | - | 1 |
| status | String(50) | - | "active" |
| doc_metadata | JSON | NULL | - |
| uploaded_by | String(100) | NULL | - |
| uploaded_at | DateTime | - | now() |
| ocr_text | Text | NULL | - |
| embedding | Text | NULL | - |

---

### FR-003: BOMItem数据模型

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-003 |
| **优先级** | P1 |
| **状态** | ✅ 已实现 |

**描述**：定义BOM（物料清单）条目，支持多层级产品结构

**验收标准**：
- [x] AC-003.1: UUID主键
- [x] AC-003.2: parent_product_id 外键（CASCADE）
- [x] AC-003.3: child_product_id 外键（CASCADE）
- [x] AC-003.4: quantity（DECIMAL 10,3）、unit、reference、notes

---

### FR-004: User数据模型

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-004 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：定义用户账户模型

**验收标准**：
- [x] AC-004.1: UUID主键
- [x] AC-004.2: username/email 唯一约束
- [x] AC-004.3: bcrypt密码存储
- [x] AC-004.4: 角色枚举（user/admin）

---

### FR-005: Pydantic验证模式

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-005 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：定义请求/响应数据验证模式

**验收标准**：
- [x] AC-005.1: ProductCreate（必填验证：product_code, name）
- [x] AC-005.2: ProductUpdate（所有字段可选）
- [x] AC-005.3: Product响应模式（包含id, timestamps）
- [x] AC-005.4: ProductStatus Literal类型约束
- [x] AC-005.5: Field验证（min_length, max_length）

**模式规格**：

| 模式 | 用途 | 关键约束 |
|------|------|----------|
| ProductBase | 共享属性 | product_code: 1-50字符, name: 1-200字符 |
| ProductCreate | 创建请求 | 继承ProductBase, status默认"draft" |
| ProductUpdate | 更新请求 | 所有字段Optional |
| Product | 响应 | 包含id, version, timestamps |
| ProductStatus | 状态枚举 | Literal["draft","active","released","archived","obsolete"] |

---

### FR-006: 数据库初始化脚本

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-006 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：提供init-db.sql用于数据库初始化

**验收标准**：
- [x] AC-006.1: 所有4张表创建（IF NOT EXISTS）
- [x] AC-006.2: 索引创建（product_code, category, product_id, email）
- [x] AC-006.3: 默认admin用户插入
- [x] AC-006.4: 示例产品数据
- [x] AC-006.5: ON CONFLICT DO NOTHING 防止重复插入

---

## 3. 非功能需求规格

### NFR-001: 数据完整性

| 属性 | 值 |
|------|-----|
| **需求ID** | NFR-001 |
| **状态** | ✅ 已满足 |

**验收标准**：
- [x] 唯一约束：product_code, username, email
- [x] 外键级联删除：产品删除→关联文档/BOM自动删除
- [x] NOT NULL约束：关键字段不允许空值

---

### NFR-002: 索引性能

| 属性 | 值 |
|------|-----|
| **需求ID** | NFR-002 |
| **状态** | ✅ 已满足 |

**索引列表**：

| 索引 | 表 | 字段 |
|------|-----|------|
| idx_products_product_code | products | product_code |
| idx_products_category | products | category |
| idx_documents_product_id | documents | product_id |
| idx_bom_items_parent_product_id | bom_items | parent_product_id |
| idx_users_email | users | email |

---

## 4. 验证矩阵

| 需求ID | 验证方法 | 结果 |
|--------|----------|------|
| FR-001 | 数据库表结构检查 | ✅ |
| FR-002 | 外键关联测试 | ✅ |
| FR-003 | BOM关系验证 | ✅ |
| FR-004 | 用户表约束检查 | ✅ |
| FR-005 | Pydantic验证测试（T009覆盖） | ✅ |
| FR-006 | init-db.sql执行 | ✅ |

---

## 5. 实现文件

| 文件 | 职责 |
|------|------|
| `/code/backend/models.py` | SQLAlchemy ORM模型 |
| `/code/backend/schemas.py` | Pydantic验证模式 |
| `/code/init-db.sql` | 数据库初始化SQL |

---

## 6. 变更记录

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v1.0.0 | 2026-03-29 | 初始版本，基于已完成代码追溯创建 |

---

*本文档采用规格驱动开发（SDD）方法编写，作为T005任务的规格基准。*
