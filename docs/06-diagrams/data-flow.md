# 数据流图 (DFD) 设计文档

## 文档信息

| 属性 | 值 |
|------|------|
| 版本 | 1.0 |
| 状态 | 草稿 |
| 创建日期 | 2026-03-27 |

---

## 1. 系统上下文图 (Level 0)

### 1.1 上下文图定义

```mermaid
graph LR
    subgraph "PDM系统"
        PDM[PDM系统]
    end
    
    User((用户)) --> PDM
    Admin((管理员)) --> PDM
    
    PDM --> |产品数据| DB[(PostgreSQL)]
    PDM --> |文件存储| MinIO[(MinIO)]
    
    PDM --> |查询结果| User
    PDM --> |管理结果| Admin
```

### 1.2 外部实体说明

| 实体 | 类型 | 描述 |
|------|------|------|
| 用户 | 参与者 | 产品经理、工程师 |
| 管理员 | 参与者 | 系统管理员 |
| PostgreSQL | 外部系统 | 数据存储 |
| MinIO | 外部系统 | 文件存储 |

---

## 2. 一级数据流图 (Level 1)

### 2.1 主要功能

```mermaid
graph TB
    subgraph "PDM系统"
        Auth[认证模块] --> Products[产品模块]
        Auth --> Documents[文档模块]
        Auth --> BOM[BOM模块]
        Auth --> Search[搜索模块]
    end
    
    User((用户)) --> Auth
    User --> Products
    User --> Documents
    User --> BOM
    User --> Search
    
    Products --> DB[(数据库)]
    Documents --> DB
    Documents --> MinIO[(MinIO)]
    BOM --> DB
    Search --> DB
```

### 2.2 数据流说明

| 数据流 | 来源 | 目的 | 内容 |
|--------|------|------|------|
| 用户凭据 | 用户 | 认证模块 | username, password |
| 认证令牌 | 认证模块 | 用户 | JWT token |
| 产品请求 | 用户 | 产品模块 | CRUD操作 |
| 产品数据 | 产品模块 | 数据库 | 产品记录 |
| 文档上传 | 用户 | 文档模块 | 文件+元数据 |
| 文件存储 | 文档模块 | MinIO | 实际文件 |
| BOM查询 | 用户 | BOM模块 | 树形结构查询 |

---

## 3. 产品模块数据流 (Level 2)

### 3.1 产品CRUD流程

```mermaid
graph LR
    subgraph "产品模块"
        API[API端点] --> Val[验证]
        Val --> Serv[服务层]
        Serv --> Repo[仓储层]
        Repo --> DB[(数据库)]
    end
    
    User --创建产品--> API
    API --返回结果--> User
    
    User --查询产品--> API
    User --更新产品--> API
    User --删除产品--> API
```

### 3.2 产品创建数据流

```mermaid
sequenceDiagram
    participant U as 用户
    participant API as 产品API
    participant S as 服务层
    participant R as 仓储层
    participant DB as 数据库
    
    U->>API: POST /products (产品数据)
    API->>S: validate_and_create()
    S->>R: 检查唯一性
    R->>DB: 查询product_code
    DB-->>R: 结果
    R-->>S: 可用
    S->>R: 创建产品
    R->>DB: INSERT product
    DB-->>R: 创建成功
    R-->>S: 产品对象
    S-->>API: 产品对象
    API-->>U: 201 Created
```

---

## 4. 认证模块数据流

### 4.1 登录流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant API as 认证API
    participant S as 服务层
    participant R as 仓储层
    participant DB as 数据库
    
    U->>API: POST /auth/login
    API->>S: authenticate(username, password)
    S->>R: 查找用户
    R->>DB: SELECT user
    DB-->>R: 用户记录
    R-->>S: 用户对象
    S->>S: verify_password()
    S-->>S: 验证通过
    S->>S: create_jwt_token()
    S-->>API: JWT token
    API-->>U: {access_token, token_type}
```

### 4.2 令牌验证流程

```mermaid
graph TB
    subgraph "JWT验证"
        Req[请求] --> Mid[中间件]
        Mid --> Extr[提取Token]
        Extr --> Dec[解码]
        Dec --> Val[验证签名]
        Val --> Check[检查过期]
        Check --> Get[获取用户]
        Get --> Auth[注入依赖]
    end
    
    Auth --> Route[路由处理]
    Route --> Res[响应]
```

---

## 5. 文档模块数据流

### 5.1 文件上传流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant API as 文档API
    participant S as 服务层
    participant R as 仓储层
    participant M as MinIO
    participant DB as 数据库
    
    U->>API: POST /documents (multipart)
    API->>S: handle_upload(file, metadata)
    S->>S: generate_uuid_filename()
    S->>M: upload_file()
    M-->>S: 文件路径
    S->>R: 创建文档记录
    R->>DB: INSERT document
    DB-->>R: 文档对象
    R-->>S: 文档对象
    S-->>API: 文档对象
    API-->>U: 201 Created
```

### 5.2 文件下载流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant API as 文档API
    participant S as 服务层
    participant R as 仓储层
    participant M as MinIO
    
    U->>API: GET /documents/{id}/download
    API->>S: get_file(id)
    S->>R: 查找文档
    R-->>S: 文档对象
    S->>M: download_file(filepath)
    M-->>S: 文件流
    S-->>API: 文件流
    API-->>U: 文件下载
```

---

## 6. BOM模块数据流

### 6.1 BOM树查询

```mermaid
graph LR
    subgraph "BOM查询"
        Req[请求] --> API
        API --> Serv[服务层]
        Serv --> R[仓储层]
        R --> DB[(递归查询)]
        DB --> Rec[递归构建]
        Rec --> Tree[树形结构]
        Tree --> Res[响应]
    end
```

### 6.2 BOM创建

```mermaid
sequenceDiagram
    participant U as 用户
    participant API as BOM API
    participant S as 服务层
    participant R as 仓储层
    participant DB as 数据库
    
    U->>API: POST /bom
    API->>S: create_bom_item(data)
    S->>R: 验证父子关系
    R->>DB: 检查循环引用
    DB-->>R: 无循环
    R-->>S: 验证通过
    S->>R: 创建BOM项
    R->>DB: INSERT bom_item
    DB-->>R: BOM对象
    R-->>S: BOM对象
    S-->>API: BOM对象
    API-->>U: 201 Created
```

---

## 7. 搜索模块数据流 (Phase 2)

### 7.1 语义搜索流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant API as 搜索API
    participant S as 服务层
    participant V as 向量服务
    participant DB as 数据库
    
    U->>API: POST /search
    API->>S: semantic_search(query)
    S->>V: generate_embedding(query)
    V-->>S: 向量
    S->>DB: similarity_search(vector)
    DB-->>S: 结果
    S-->>API: 搜索结果
    API-->>U: 搜索结果
```

---

## 8. 数据存储流

### 8.1 数据存储对应

```mermaid
graph LR
    subgraph "存储层"
        P[(PostgreSQL)] --> |产品| Products
        P --> |用户| Users
        P --> |文档元数据| Docs
        P --> |BOM| BOMs
        P --> |向量| Embeddings
        
        M[(MinIO)] --> |实际文件| Files
    end
    
    Products --> P
    Users --> P
    Docs --> P
    BOMs --> P
    Embeddings --> P
    Files --> M
```

---

## 9. 数据字典

### 9.1 主要数据实体

| 实体 | 存储 | 主要字段 |
|------|------|----------|
| Product | PostgreSQL | product_code, name, category, status |
| User | PostgreSQL | username, email, hashed_password, role |
| Document | PostgreSQL + MinIO | filename, filepath, mime_type, product_id |
| BOMItem | PostgreSQL | parent_product_id, child_product_id, quantity |
| Embedding | PostgreSQL | entity_id, entity_type, vector |

---

## 10. 错误处理流

### 10.1 错误传播

```mermaid
graph TB
    subgraph "错误处理"
        Err[异常] --> Hand[处理器]
        Hand --> Log[日志记录]
        Log --> Map[错误映射]
        Map --> Resp[统一响应]
    end
    
    Resp --> 400[400 Bad Request]
    Resp --> 401[401 Unauthorized]
    Resp --> 403[403 Forbidden]
    Resp --> 404[404 Not Found]
    Resp --> 500[500 Internal Error]
```

---

*文档版本: 1.0*
*最后更新: 2026-03-27*