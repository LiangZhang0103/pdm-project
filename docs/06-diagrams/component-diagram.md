# 组件图 (Component Diagram) 设计文档

## 文档信息

| 属性 | 值 |
|------|------|
| 版本 | 1.0 |
| 状态 | 草稿 |
| 创建日期 | 2026-03-27 |

---

## 1. 系统级组件图

### 1.1 整体架构组件

```mermaid
graph TB
    subgraph "客户端层"
        FE[React SPA]
    end
    
    subgraph "API网关层"
        GW[FastAPI Gateway<br/>Port 8000]
    end
    
    subgraph "服务层"
        AUTH[Auth Service<br/>认证服务]
        PROD[Product Service<br/>产品服务]
        DOC[Document Service<br/>文档服务]
        BOM[BOM Service<br/>BOM服务]
        AI[AI Service<br/>AI服务]
    end
    
    subgraph "数据访问层"
        REPO[Repository<br/>仓储]
        ORM[SQLAlchemy ORM]
    end
    
    subgraph "外部服务"
        PG[(PostgreSQL<br/>Port 5432)]
        MINIO[(MinIO<br/>Port 9000)]
    end
    
    FE --"HTTP"--> GW
    GW --"路由"--> AUTH
    GW --"路由"--> PROD
    GW --"路由"--> DOC
    GW --"路由"--> BOM
    GW --"路由"--> AI
    
    AUTH --"查询"--> REPO
    PROD --"查询"--> REPO
    DOC --"查询"--> REPO
    BOM --"查询"--> REPO
    
    REPO --"操作"--> ORM
    ORM --"SQL"--> PG
    
    DOC --"文件操作"--> MINIO
```

---

## 2. 前端组件图

### 2.1 前端应用结构

```mermaid
graph TB
    subgraph "React应用"
        APP[App.tsx<br/>根组件]
        ROUTER[React Router<br/>路由]
        
        subgraph "页面组件"
            HOME[首页]
            PROD_LIST[产品列表]
            PROD_EDIT[产品编辑]
            DOCS[文档管理]
            BOM[BoM管理]
            LOGIN[登录/注册]
        end
        
        subgraph "公共组件"
            LAYOUT[Layout布局]
            HEADER[Header头部]
            SIDEBAR[Sidebar侧边栏]
            ERROR[ErrorBoundary]
        end
        
        subgraph "UI组件库"
            BTN[Button按钮]
            INPUT[Input输入框]
            TABLE[Table表格]
            MODAL[Modal模态框]
            TOAST[Toast提示]
        end
        
        subgraph "状态管理"
            STORE[Zustand Store]
            API[API Client]
        end
    end
    
    APP --> ROUTER
    ROUTER --> HOME
    ROUTER --> PROD_LIST
    ROUTER --> PROD_EDIT
    ROUTER --> DOCS
    ROUTER --> BOM
    ROUTER --> LOGIN
    
    PROD_LIST --> LAYOUT
    DOCS --> LAYOUT
    BOM --> LAYOUT
    
    LAYOUT --> HEADER
    LAYOUT --> SIDEBAR
    
    PROD_LIST --> TABLE
    PROD_EDIT --> INPUT
    PROD_EDIT --> BTN
    DOCS --> MODAL
    
    PROD_LIST --> STORE
    LOGIN --> STORE
    
    TABLE --> API
    INPUT --> API
```

### 2.2 前端组件职责

| 组件 | 职责 | 依赖 |
|------|------|------|
| App | 路由配置, 全局错误处理 | React Router |
| Layout | 页面布局结构 | Header, Sidebar |
| ProductList | 产品列表展示 | Table, Store |
| ProductForm | 产品表单 | Input, Button |
| DocumentUpload | 文件上传 | API, Modal |
| BOMTree | BOM树展示 | 递归组件 |

---

## 3. 后端组件图

### 3.1 后端服务架构

```mermaid
graph TB
    subgraph "FastAPI应用"
        MAIN[main.py<br/>应用入口]
        
        subgraph "中间件"
            CORS[CORS中间件]
            AUTH[认证中间件]
            LOG[日志中间件]
        end
        
        subgraph "路由层"
            PRODUCTS[products.py<br/>产品路由]
            DOCUMENTS[documents.py<br/>文档路由]
            BOM[bom.py<br/>BOM路由]
            AUTH[auth.py<br/>认证路由]
            SEARCH[search.py<br/>搜索路由]
        end
        
        subgraph "服务层"
            PROD_SVC[ProductService<br/>产品服务]
            DOC_SVC[DocumentService<br/>文档服务]
            BOM_SVC[BOMService<br/>BOM服务]
            AUTH_SVC[AuthService<br/>认证服务]
            AI_SVC[AIService<br/>AI服务]
        end
        
        subgraph "仓储层"
            PROD_REPO[ProductRepository]
            DOC_REPO[DocumentRepository]
            BOM_REPO[BOMRepository]
            USER_REPO[UserRepository]
        end
        
        subgraph "数据模型"
            MODELS[models.py<br/>SQLAlchemy模型]
            SCHEMAS[schemas.py<br/>Pydantic模型]
        end
        
        subgraph "依赖注入"
            DEPS[deps.py<br/>依赖定义]
        end
    end
    
    MAIN --> CORS
    MAIN --> AUTH
    MAIN --> LOG
    MAIN --> PRODUCTS
    MAIN --> DOCUMENTS
    MAIN --> BOM
    MAIN --> AUTH
    MAIN --> SEARCH
    
    PRODUCTS --> PROD_SVC
    DOCUMENTS --> DOC_SVC
    BOM --> BOM_SVC
    AUTH --> AUTH_SVC
    SEARCH --> AI_SVC
    
    PROD_SVC --> PROD_REPO
    DOC_SVC --> DOC_REPO
    BOM_SVC --> BOM_REPO
    AUTH_SVC --> USER_REPO
    
    PROD_REPO --> MODELS
    DOC_REPO --> MODELS
    BOM_REPO --> MODELS
    USER_REPO --> MODELS
    
    PRODUCTS --> SCHEMAS
    DOCUMENTS --> SCHEMAS
    BOM --> SCHEMAS
    AUTH --> SCHEMAS
    
    PRODUCTS --> DEPS
    DOCUMENTS --> DEPS
    BOM --> DEPS
    AUTH --> DEPS
```

### 3.2 后端组件职责

| 组件 | 职责 | 公开API |
|------|------|---------|
| main.py | 应用配置, 中间件注册 | - |
| routers/ | 请求路由, 响应处理 | HTTP端点 |
| services/ | 业务逻辑, 数据验证 | 业务方法 |
| repositories/ | 数据库操作, 查询 | 仓储方法 |
| models.py | 数据库表结构 | ORM模型 |
| schemas.py | 数据验证, 序列化 | Pydantic模型 |
| deps.py | 依赖注入, 认证 | FastAPI依赖 |

---

## 4. 组件关系图

### 4.1 产品模块组件

```mermaid
classDiagram
    class ProductRouter {
        +create_product()
        +read_products()
        +update_product()
        +delete_product()
    }
    
    class ProductService {
        +create()
        +update()
        +delete()
        +list()
        +get_by_id()
    }
    
    class ProductRepository {
        +create()
        +update()
        +delete()
        +find_all()
        +find_by_id()
        +find_by_code()
    }
    
    class Product {
        +id: UUID
        +product_code: str
        +name: str
        +category: str
        +status: str
    }
    
    class ProductSchema {
        +product_code: str
        +name: str
        +category: str
    }
    
    ProductRouter --> ProductService
    ProductService --> ProductRepository
    ProductRepository --> Product
    ProductRouter ..> ProductSchema
```

### 4.2 认证模块组件

```mermaid
classDiagram
    class AuthRouter {
        +login()
        +register()
    }
    
    class AuthService {
        +authenticate()
        +create_token()
        +verify_token()
    }
    
    class UserRepository {
        +create()
        +find_by_username()
        +find_by_email()
    }
    
    class User {
        +id: UUID
        +username: str
        +email: str
        +hashed_password: str
        +role: str
    }
    
    class TokenSchema {
        +access_token: str
        +token_type: str
    }
    
    class TokenData {
        +username: str
        +role: str
    }
    
    AuthRouter --> AuthService
    AuthService --> UserRepository
    UserRepository --> User
    AuthRouter ..> TokenSchema
    AuthService ..> TokenData
```

---

## 5. 数据流组件

### 5.1 文件上传组件

```mermaid
graph LR
    subgraph "文件上传流程"
        A[用户] --> B[FileUpload组件]
        B --> C[FormData]
        C --> D[API Client]
        D --> E[POST /documents]
        E --> F[Document Router]
        F --> G[Document Service]
        G --> H[MinIO Client]
        H --> I[MinIO Server]
        G --> J[Document Repository]
        J --> K[PostgreSQL]
        K --> J
        J --> G
        G --> F
        F --> D
        D --> B
    end
```

---

## 6. 模块交互图

### 6.1 组件时序图

```mermaid
sequenceDiagram
    participant Client
    participant Router
    participant Service
    participant Repository
    participant Database
    
    Client->>Router: POST /products
    Router->>Service: create(data)
    Service->>Repository: create(entity)
    Repository->>Database: INSERT
    Database-->>Repository: Result
    Repository-->>Service: entity
    Service-->>Router: schema
    Router-->>Client: Response
```

---

## 7. 基础设施组件

### 7.1 Docker容器

```mermaid
graph TB
    subgraph "Docker环境"
        subgraph "应用容器"
            FE[frontend<br/>:3000]
            BE[backend<br/>:8000]
        end
        
        subgraph "数据容器"
            PG[postgres<br/>:5432]
            MINIO[minio<br/>:9000,:9001]
            PGADMIN[pgadmin<br/>:5050]
        end
        
        subgraph "网络"
            NET[Bridge Network]
        end
        
        FE --> NET
        BE --> NET
        PG --> NET
        MINIO --> NET
        PGADMIN --> NET
    end
```

---

## 8. 组件依赖矩阵

| 组件 | 前端依赖 | 后端依赖 |
|------|----------|----------|
| React Router | - | 无 |
| Axios | React | 无 |
| Zustand | React | 无 |
| FastAPI | 无 | - |
| SQLAlchemy | 无 | Pydantic |
| MinIO | 无 | Boto3 |

---

*文档版本: 1.0*
*最后更新: 2026-03-27*