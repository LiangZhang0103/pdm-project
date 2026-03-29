# T003: FastAPI基础框架搭建 - SDD规格说明文档

## 文档信息

| 项目 | 内容 |
|------|------|
| 文档ID | SPEC-T003 |
| 版本 | v1.0.0 |
| 状态 | 已完成 |
| 创建日期 | 2026-03-29 |
| 关联任务 | T003 |
| 完成日期 | 2026-03-27 |

---

## 1. 概述

### 1.1 目的
本文档采用规格驱动开发（SDD）方法，定义FastAPI基础框架的功能需求、非功能需求、技术约束和验收标准。

### 1.2 范围
- FastAPI应用初始化与配置
- 配置管理系统（pydantic-settings）
- 数据库连接管理（SQLAlchemy）
- CORS中间件
- 健康检查端点
- API文档自动生成（Swagger/ReDoc）
- 依赖注入框架
- 认证基础设施
- 路由模块化

### 1.3 术语定义

| 术语 | 定义 |
|------|------|
| SDD | Specification-Driven Development，规格驱动开发 |
| FR | Functional Requirement，功能需求 |
| NFR | Non-Functional Requirement，非功能需求 |
| TC | Technical Constraint，技术约束 |

---

## 2. 功能需求规格

### FR-001: FastAPI应用初始化

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-001 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：创建FastAPI应用实例，配置基本元数据和文档

**验收标准**：
- [x] AC-001.1: 应用标题 "PDM System API"
- [x] AC-001.2: Swagger文档可通过 `/docs` 访问
- [x] AC-001.3: ReDoc文档可通过 `/redoc` 访问
- [x] AC-001.4: API版本 "0.1.0"

**代码规格**：
```python
app = FastAPI(
    title="PDM System API",
    description="Product Data Management System API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
```

**实现文件**：
- `/code/backend/main.py`

---

### FR-002: 配置管理系统

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-002 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：使用pydantic-settings实现类型安全的配置管理，支持环境变量和.env文件

**验收标准**：
- [x] AC-002.1: 所有配置项有默认值
- [x] AC-002.2: 支持通过环境变量覆盖
- [x] AC-002.3: 支持 `.env` 文件加载
- [x] AC-002.4: 配置分类清晰（数据库/存储/认证/应用/AI）

**配置项规格**：

| 分类 | 配置项 | 类型 | 默认值 |
|------|--------|------|--------|
| **数据库** | `database_url` | str | `postgresql://pdm:pdm123@localhost:5432/pdm` |
| | `database_test_url` | str | `postgresql://pdm:pdm123@localhost:5432/pdm_test` |
| **MinIO** | `minio_endpoint` | str | `localhost:9000` |
| | `minio_access_key` | str | `pdm` |
| | `minio_secret_key` | str | `pdm123` |
| | `minio_bucket` | str | `pdm-documents` |
| | `minio_secure` | bool | `False` |
| **JWT** | `jwt_secret_key` | str | `your-secret-key-change-in-production` |
| | `jwt_algorithm` | str | `HS256` |
| | `jwt_access_token_expire_minutes` | int | `30` |
| **应用** | `environment` | str | `development` |
| | `debug` | bool | `True` |
| | `cors_origins` | list[str] | `["http://localhost:3000", "http://localhost:8000"]` |
| **AI** | `enable_ai_features` | bool | `True` |
| | `ocr_language` | str | `ch` |
| | `embedding_model` | str | `all-MiniLM-L6-v2` |

**实现文件**：
- `/code/backend/config.py`

---

### FR-003: 数据库连接管理

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-003 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：使用SQLAlchemy 2.0配置数据库引擎和会话管理

**验收标准**：
- [x] AC-003.1: 引擎配置 `pool_pre_ping=True`（自动重连）
- [x] AC-003.2: Debug模式下启用SQL日志（`echo=settings.debug`）
- [x] AC-003.3: 会话生成器 `get_db()` 使用依赖注入模式
- [x] AC-003.4: 会话在请求结束后自动关闭（try/finally）

**代码规格**：
```python
engine = create_engine(settings.database_url, pool_pre_ping=True, echo=settings.debug)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**实现文件**：
- `/code/backend/database.py`

---

### FR-004: CORS中间件

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-004 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：配置跨域资源共享（CORS），允许前端访问后端API

**验收标准**：
- [x] AC-004.1: 允许的源来自配置（`cors_origins`）
- [x] AC-004.2: 允许携带凭证（`allow_credentials=True`）
- [x] AC-004.3: 允许所有HTTP方法和头

**代码规格**：
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### FR-005: 健康检查端点

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-005 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：实现健康检查API，监控数据库和MinIO连接状态

**验收标准**：
- [x] AC-005.1: 端点路径 `GET /health`
- [x] AC-005.2: 返回数据库连接状态（`SELECT 1` 查询测试）
- [x] AC-005.3: 返回MinIO连接状态（`list_buckets` 测试）
- [x] AC-005.4: 返回时间戳
- [x] AC-005.5: 任何连接失败时整体状态为 "unhealthy"

**响应规格**：
```json
{
  "status": "healthy" | "unhealthy",
  "database": true | false,
  "minio": true | false,
  "timestamp": "2026-03-29T10:00:00.000000"
}
```

**实现文件**：
- `/code/backend/main.py` (health_check函数)
- `/code/backend/schemas.py` (HealthCheck模型)

---

### FR-006: API根端点

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-006 |
| **优先级** | P1 |
| **状态** | ✅ 已实现 |

**描述**：提供API根路径，返回基本信息

**验收标准**：
- [x] AC-006.1: 端点路径 `GET /`
- [x] AC-006.2: 返回API名称、版本、文档链接

**响应规格**：
```json
{
  "message": "PDM System API",
  "version": "0.1.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

### FR-007: 依赖注入框架

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-007 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：建立认证依赖注入链，为后续API提供用户上下文

**验收标准**：
- [x] AC-007.1: `get_current_user` - 解析JWT token获取当前用户
- [x] AC-007.2: `get_current_active_user` - 验证用户是否激活
- [x] AC-007.3: `get_current_admin_user` - 验证用户是否为管理员
- [x] AC-007.4: 使用 `HTTPBearer` 从请求头提取token

**依赖链**：
```
get_current_user → get_current_active_user → get_current_admin_user
     (认证)            (激活检查)              (权限检查)
```

**实现文件**：
- `/code/backend/deps.py`

---

### FR-008: 路由模块化

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-008 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：采用模块化路由设计，各功能独立成模块

**验收标准**：
- [x] AC-008.1: `routers/products.py` - 产品路由（prefix: `/products`）
- [x] AC-008.2: `routers/documents.py` - 文档路由（prefix: `/documents`）
- [x] AC-008.3: `routers/bom.py` - BOM路由（prefix: `/bom`）
- [x] AC-008.4: `routers/auth.py` - 认证路由（prefix: `/auth`）

**路由注册规格**：
```python
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(bom.router, prefix="/bom", tags=["bom"])
```

---

## 3. 非功能需求规格

### NFR-001: API文档自动生成

| 属性 | 值 |
|------|-----|
| **需求ID** | NFR-001 |
| **优先级** | P0 |
| **状态** | ✅ 已满足 |

**描述**：所有API端点应有自动生成的交互式文档

**验收标准**：
- [x] AC-NFR-001.1: Swagger UI可通过 `/docs` 访问
- [x] AC-NFR-001.2: ReDoc可通过 `/redoc` 访问
- [x] AC-NFR-001.3: 端点有描述和参数说明

---

### NFR-002: 错误处理

| 属性 | 值 |
|------|-----|
| **需求ID** | NFR-002 |
| **优先级** | P1 |
| **状态** | ✅ 已满足 |

**描述**：健康检查应优雅处理外部依赖故障

**验收标准**：
- [x] AC-NFR-002.1: 数据库连接失败不导致500错误
- [x] AC-NFR-002.2: MinIO连接失败不导致500错误
- [x] AC-NFR-002.3: 使用try/except隔离各依赖检查

---

### NFR-003: 可测试性

| 属性 | 值 |
|------|-----|
| **需求ID** | NFR-003 |
| **优先级** | P1 |
| **状态** | ✅ 已满足 |

**描述**：框架设计应便于编写单元测试

**验收标准**：
- [x] AC-NFR-003.1: 依赖注入模式使mock替换简单
- [x] AC-NFR-003.2: 配置通过Settings类集中管理，便于测试覆盖
- [x] AC-NFR-003.3: 测试覆盖率 > 85%（实际达到95%）

---

## 4. 技术约束

| 约束ID | 描述 | 理由 |
|--------|------|------|
| TC-001 | Python版本: 3.11 | FastAPI兼容性好，性能优秀 |
| TC-002 | FastAPI版本: 0.104.1 | 稳定版本 |
| TC-003 | SQLAlchemy版本: 2.0.23 | 使用2.0新API（mapped_column等） |
| TC-004 | 使用pydantic-settings管理配置 | 类型安全，自动验证 |
| TC-005 | 使用HTTPBearer而非OAuth2PasswordBearer | JWT Bearer Token更通用 |
| TC-006 | 启动时自动创建数据库表 | 开发阶段简化流程 |

---

## 5. 依赖版本表

| 包名 | 版本 | 用途 |
|------|------|------|
| fastapi | 0.104.1 | Web框架 |
| uvicorn[standard] | 0.24.0 | ASGI服务器 |
| sqlalchemy | 2.0.23 | ORM |
| psycopg2-binary | 2.9.9 | PostgreSQL驱动 |
| pydantic[email] | 2.5.0 | 数据验证 |
| pydantic-settings | 2.1.0 | 配置管理 |
| python-dotenv | 1.0.0 | .env文件加载 |
| python-multipart | 0.0.6 | 文件上传支持 |
| python-jose[cryptography] | 3.3.0 | JWT处理 |
| passlib[bcrypt] | 1.7.4 | 密码哈希 |
| minio | 7.2.2 | MinIO客户端 |
| httpx | 0.25.2 | HTTP客户端 |
| alembic | 1.12.1 | 数据库迁移 |
| pytest | 7.4.3 | 测试框架 |
| pytest-cov | 4.1.0 | 测试覆盖率 |

---

## 6. 文件结构

```
backend/
├── main.py              # 应用入口，路由注册，中间件
├── config.py            # Settings配置类
├── database.py          # 数据库引擎与会话
├── deps.py              # 依赖注入（认证链）
├── models.py            # SQLAlchemy数据模型
├── schemas.py           # Pydantic数据模式
├── pytest.ini           # 测试配置
├── requirements.txt     # Python依赖
├── Dockerfile.dev       # 开发用Dockerfile
├── routers/             # 路由模块
│   ├── products.py      # 产品CRUD API
│   ├── documents.py     # 文档管理API
│   ├── bom.py           # BOM管理API
│   └── auth.py          # 认证API
└── tests/               # 测试用例
    ├── conftest.py      # 测试fixtures
    ├── test_health.py   # 健康检查测试
    └── test_products.py # 产品API测试
```

---

## 7. 验证矩阵

| 需求ID | 验证方法 | 验证结果 | 日期 |
|--------|----------|----------|------|
| FR-001 | 访问 http://localhost:8000/docs | ✅ 通过 | 2026-03-27 |
| FR-002 | 环境变量覆盖测试 | ✅ 通过 | 2026-03-27 |
| FR-003 | 数据库连接和会话管理 | ✅ 通过 | 2026-03-27 |
| FR-004 | 前端跨域请求测试 | ✅ 通过 | 2026-03-27 |
| FR-005 | GET /health 返回正确状态 | ✅ 通过 | 2026-03-29 |
| FR-006 | GET / 返回API信息 | ✅ 通过 | 2026-03-27 |
| FR-007 | 认证依赖注入mock测试 | ✅ 通过 | 2026-03-29 |
| FR-008 | 路由模块注册检查 | ✅ 通过 | 2026-03-27 |
| NFR-001 | Swagger/ReDoc文档访问 | ✅ 通过 | 2026-03-27 |
| NFR-002 | 健康检查容错测试 | ✅ 通过 | 2026-03-29 |
| NFR-003 | pytest测试覆盖率95% | ✅ 通过 | 2026-03-29 |

---

## 8. 变更记录

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v1.0.0 | 2026-03-29 | 初始版本，基于已完成的T003实现追溯创建SDD规格 |

---

*本文档采用规格驱动开发（SDD）方法编写，作为T003任务的规格基准。*
