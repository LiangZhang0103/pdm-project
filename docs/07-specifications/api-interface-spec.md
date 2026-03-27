# API 接口规格与错误码文档

## 文档信息

| 属性 | 值 |
|------|------|
| 版本 | 1.0 |
| 状态 | 草稿 |
| 创建日期 | 2026-03-27 |

---

## 1. API 接口规范

### 1.1 基础规范

| 项目 | 规范 |
|------|------|
| 协议 | HTTP/HTTPS |
| 编码 | UTF-8 |
| 路径前缀 | /api/v1 |
| 内容类型 | application/json |

### 1.2 认证方式

```
Header: Authorization: Bearer <token>
```

### 1.3 通用响应格式

**成功响应:**
```json
{
  "data": { ... },
  "message": "操作成功"
}
```

**列表响应:**
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "limit": 10
}
```

**错误响应:**
```json
{
  "detail": "错误描述",
  "code": "ERROR_CODE",
  "fields": [
    {
      "field": "field_name",
      "message": "具体错误"
    }
  ]
}
```

---

## 2. HTTP 状态码

### 2.1 状态码分类

| 状态码 | 含义 | 描述 |
|--------|------|------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 204 | No Content | 删除成功 |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未认证 |
| 403 | Forbidden | 无权限 |
| 404 | Not Found | 资源不存在 |
| 422 | Unprocessable | 验证错误 |
| 429 | Too Many Requests | 请求过于频繁 |
| 500 | Internal Server Error | 服务器错误 |
| 503 | Service Unavailable | 服务不可用 |

### 2.2 状态码使用场景

| 场景 | 状态码 |
|------|--------|
| 登录成功 | 200 |
| 创建产品成功 | 201 |
| 删除成功 | 204 |
| 无效的JSON | 400 |
| Token过期 | 401 |
| 权限不足 | 403 |
| 产品不存在 | 404 |
| 产品代码重复 | 422 |
| 服务器错误 | 500 |

---

## 3. 业务错误码

### 3.1 认证模块 (AUTH)

| 错误码 | HTTP状态 | 描述 | 说明 |
|--------|----------|------|------|
| AUTH_001 | 400 | invalid_request | 请求参数缺失 |
| AUTH_002 | 401 | invalid_credentials | 用户名或密码错误 |
| AUTH_003 | 401 | token_expired | Token已过期 |
| AUTH_004 | 401 | token_invalid | Token无效 |
| AUTH_005 | 400 | username_exists | 用户名已存在 |
| AUTH_006 | 400 | email_exists | 邮箱已注册 |
| AUTH_007 | 400 | password_weak | 密码强度不足 |
| AUTH_008 | 429 | login_attempts_exceeded | 登录尝试过多 |

### 3.2 产品模块 (PRODUCT)

| 错误码 | HTTP状态 | 描述 | 说明 |
|--------|----------|------|------|
| PROD_001 | 400 | invalid_product_code | 产品代码格式错误 |
| PROD_002 | 400 | product_code_exists | 产品代码已存在 |
| PROD_003 | 404 | product_not_found | 产品不存在 |
| PROD_004 | 400 | invalid_product_data | 产品数据验证失败 |
| PROD_005 | 400 | invalid_status | 状态值无效 |
| PROD_006 | 400 | cannot_delete_active | 无法删除活跃产品 |

### 3.3 文档模块 (DOCUMENT)

| 错误码 | HTTP状态 | 描述 | 说明 |
|--------|----------|------|------|
| DOC_001 | 400 | file_too_large | 文件大小超过限制 |
| DOC_002 | 400 | invalid_file_type | 文件类型不支持 |
| DOC_003 | 400 | upload_failed | 文件上传失败 |
| DOC_004 | 404 | document_not_found | 文档不存在 |
| DOC_005 | 400 | download_failed | 文件下载失败 |
| DOC_006 | 400 | file_corrupted | 文件已损坏 |
| DOC_007 | 400 | storage_full | 存储空间不足 |

### 3.4 BOM模块 (BOM)

| 错误码 | HTTP状态 | 描述 | 说明 |
|--------|----------|------|------|
| BOM_001 | 400 | invalid_parent | 父产品不存在 |
| BOM_002 | 400 | invalid_child | 子产品不存在 |
| BOM_003 | 400 | circular_reference | 循环引用检测 |
| BOM_004 | 400 | duplicate_relationship | 重复的BOM关系 |
| BOM_005 | 400 | invalid_quantity | 数量必须大于0 |
| BOM_006 | 404 | bom_item_not_found | BOM项不存在 |
| BOM_007 | 400 | self_reference | 不能引用自身 |

### 3.5 搜索模块 (SEARCH)

| 错误码 | HTTP状态 | 描述 | 说明 |
|--------|----------|------|------|
| SCH_001 | 400 | empty_query | 查询关键词为空 |
| SCH_002 | 400 | invalid_search_type | 搜索类型无效 |
| SCH_003 | 500 | search_service_error | 搜索服务异常 |

### 3.6 系统模块 (SYSTEM)

| 错误码 | HTTP状态 | 描述 | 说明 |
|--------|----------|------|------|
| SYS_001 | 503 | database_unavailable | 数据库不可用 |
| SYS_002 | 503 | storage_unavailable | 存储服务不可用 |
| SYS_003 | 429 | rate_limit_exceeded | 超过速率限制 |
| SYS_004 | 500 | internal_error | 内部错误 |

---

## 4. 字段级错误

### 4.1 字段验证规则

| 字段 | 规则 | 错误消息 |
|------|------|----------|
| username | 3-100字符 | 用户名长度需在3-100之间 |
| email | 有效邮箱格式 | 请输入有效的邮箱地址 |
| password | 最小6字符 | 密码长度至少6个字符 |
| product_code | 1-50字符 | 产品代码长度需在1-50之间 |
| name | 1-200字符 | 名称长度需在1-200之间 |
| quantity | 大于0 | 数量必须大于0 |

### 4.2 字段错误响应示例

```json
{
  "detail": "Validation Error",
  "code": "VALIDATION_ERROR",
  "fields": [
    {
      "field": "product_code",
      "message": "产品代码长度需在1-50之间"
    },
    {
      "field": "email",
      "message": "请输入有效的邮箱地址"
    }
  ]
}
```

---

## 5. 分页规范

### 5.1 分页参数

| 参数 | 类型 | 默认值 | 范围 | 说明 |
|------|------|--------|------|------|
| page | int | 1 | 1-1000 | 页码 |
| limit | int | 10 | 1-100 | 每页条数 |

### 5.2 分页响应

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "limit": 10,
  "pages": 10
}
```

---

## 6. 排序规范

### 6.1 排序参数

| 参数 | 说明 | 示例 |
|------|------|------|
| sort | 排序字段 | created_at, name, product_code |
| order | 排序方向 | asc, desc |

### 6.2 排序示例

```
GET /products?sort=created_at&order=desc
GET /products?sort=name&order=asc
```

---

## 7. 过滤规范

### 7.1 过滤参数

| 参数 | 类型 | 说明 |
|------|------|------|
| category | string | 按分类过滤 |
| status | string | 按状态过滤 |
| search | string | 搜索关键词 |

### 7.2 过滤示例

```
GET /products?status=draft
GET /products?category=Electronics&status=released
GET /products?search=关键字
```

---

## 8. 速率限制

### 8.1 限制规则

| 端点 | 限制 | 窗口 |
|------|------|------|
| /auth/login | 5次 | 5分钟 |
| /products | 100次 | 1分钟 |
| /documents | 20次 | 1分钟 |
| 其他 | 60次 | 1分钟 |

### 8.2 速率限制响应

```json
{
  "detail": "Rate limit exceeded",
  "code": "RATE_LIMIT_001",
  "retry_after": 60
}
```

响应头:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1234567890
```

---

## 9. 版本控制

### 9.1 URL版本控制

```
当前版本: v1
路径: /api/v1/products
```

### 9.2 版本迁移

| 版本 | 状态 | 说明 |
|------|------|------|
| v1 | 当前 | 初始版本 |

---

## 10. API 端点汇总

### 10.1 认证端点

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | /auth/register | 否 | 用户注册 |
| POST | /auth/login | 否 | 用户登录 |
| GET | /auth/me | 是 | 获取当前用户 |

### 10.2 产品端点

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| GET | /products | 是 | 产品列表 |
| POST | /products | 是 | 创建产品 |
| GET | /products/{id} | 是 | 产品详情 |
| PUT | /products/{id} | 是 | 更新产品 |
| DELETE | /products/{id} | 是(管理员) | 删除产品 |

### 10.3 文档端点

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| GET | /products/{id}/documents | 是 | 文档列表 |
| POST | /documents | 是 | 上传文档 |
| GET | /documents/{id} | 是 | 文档详情 |
| GET | /documents/{id}/download | 是 | 下载文档 |
| DELETE | /documents/{id} | 是 | 删除文档 |

### 10.4 BOM端点

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| GET | /products/{id}/bom | 是 | BOM树 |
| POST | /bom | 是 | 创建BOM项 |
| PUT | /bom/{id} | 是 | 更新BOM项 |
| DELETE | /bom/{id} | 是 | 删除BOM项 |

---

*文档版本: 1.0*
*最后更新: 2026-03-27*