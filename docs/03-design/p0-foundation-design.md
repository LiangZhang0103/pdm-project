# P0: 项目初始化与基础框架 - 详细设计说明书

## 文档信息

| 项目 | 内容 |
|------|------|
| 版本 | v2.0.0 |
| 状态 | V&V验证通过 |
| 日期 | 2026-03-29 |
| 作者 | AI辅助开发 |
| 关联任务 | T001, T002, T003, T004 |

## 1. 概述

### 1.1 文档目的

本文档详细记录P0阶段（项目初始化与基础框架）的设计方案，为后续开发和维护提供完整的技术参考。该阶段是整个PDM系统的基础，直接影响后续功能开发的速度和质量。

### 1.2 适用范围

本文档适用于以下场景：
- 新开发人员了解项目结构和开发环境配置
- 运维人员部署和配置开发/生产环境
- 架构师评估技术选型和设计方案
- 测试人员理解系统架构和依赖关系

### 1.3 参考文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 技术栈文档 | `/docs/10-references/tech-stack.md` | 技术选型和依赖说明 |
| API设计文档 | `/docs/03-design/api-design.md` | API接口设计规范 |
| 数据库设计 | `/docs/03-design/database-design.md` | 数据模型设计 |
| 系统架构 | `/docs/04-architecture/system-architecture.md` | 整体架构设计 |
| 安全架构 | `/docs/04-architecture/security-architecture.md` | 安全设计方案 |

---

## 2. T001: GitHub仓库初始化

### 2.1 任务概述

创建GitHub仓库并初始化项目结构，设置版本控制规范和开发工作流。这是整个项目的起点，需要建立清晰的目录结构和文件组织方式。

### 2.2 需求描述

根据项目目标和技术栈，需要满足以下需求：
1. 建立清晰的目录结构，区分代码、文档和资源
2. 配置合适的.gitignore规则，避免提交不必要的文件
3. 创建README文档，说明项目概况和使用方法
4. 设置分支策略，支持并行开发和版本管理

### 2.3 设计方案

#### 2.3.1 仓库结构设计

```
pdm-project/
├── .gitignore              # Git忽略规则
├── README.md               # 项目说明文档
├── LICENSE                 # 开源许可证
├── .sisyphus/              # AI辅助开发配置
│   └── plans/              # 工作计划
├── code/                   # 代码目录
│   ├── backend/           # FastAPI后端
│   │   ├── main.py        # 应用入口
│   │   ├── config.py      # 配置管理
│   │   ├── database.py    # 数据库连接
│   │   ├── models.py      # 数据模型
│   │   ├── schemas.py     # Pydantic模式
│   │   ├── deps.py        # 依赖注入
│   │   ├── routers/       # 路由模块
│   │   └── requirements.txt
│   ├── frontend/          # React前端
│   │   ├── src/          # 源代码
│   │   ├── public/       # 静态资源
│   │   ├── package.json  # 依赖配置
│   │   ├── vite.config.ts
│   │   └── tsconfig.json
│   ├── docker-compose.yml # Docker编排
│   └── init-db.sql       # 数据库初始化
├── docs/                  # 文档目录
│   ├── 01-prd/           # 产品需求文档
│   ├── 02-requirements/  # 需求规格
│   ├── 03-design/        # 设计文档
│   ├── 04-architecture/  # 架构文档
│   ├── 05-adr/          # 架构决策记录
│   ├── 06-diagrams/      # 图表
│   ├── 07-specifications/# 规格说明
│   ├── 08-test/          # 测试文档
│   ├── 09-vcs/           # 版本控制
│   ├── 10-references/    # 参考资料
│   ├── 11-project/       # 项目管理
│   └── 12-mbse/          # MBSE分析
└── scripts/              # 脚本目录
```

#### 2.3.2 目录设计原则

采用以下设计原则组织目录结构：

1. **代码与文档分离**：代码在`code/`目录，文档在`docs/`目录，便于管理和部署
2. **模块化结构**：前端和后端分别独立目录，支持独立开发和部署
3. **分层设计**：文档按阶段分层（PRD→需求→设计→架构→实现→测试）
4. **功能模块化**：前端按功能模块组织（features/、components/、stores/）

### 2.4 配置说明

#### 2.4.1 .gitignore配置

项目配置了全面的.gitignore规则，涵盖以下类别：

| 类别 | 说明 | 示例 |
|------|------|------|
| Python | Python字节码、构建产物、虚拟环境 | `__pycache__/`、`*.py[cod]`、`.venv/` |
| Node.js | npm/yarn产物、构建缓存 | `node_modules/`、`.next/`、`dist/` |
| IDE | 编辑器配置和临时文件 | `.vscode/`、`.idea/`、`*.swp` |
| OS | 操作系统临时文件 | `.DS_Store`、`Thumbs.db` |
| Docker | Docker相关文件 | `docker-compose.override.yml` |
| 数据库 | 本地数据库文件 | `*.db`、`*.sqlite3` |
| 环境 | 环境配置文件 | `.env.local`、`.env.*.local` |
| 日志 | 日志文件 | `*.log`、`logs/` |
| 临时 | 临时文件 | `*.tmp`、`*.temp` |

#### 2.4.2 分支策略

采用Git Flow简化版分支策略：

| 分支 | 用途 | 生命周期 |
|------|------|----------|
| `main` | 生产代码 | 长期 |
| `develop` | 开发主分支 | 长期 |
| `feature/*` | 功能开发 | 临时 |
| `bugfix/*` | Bug修复 | 临时 |
| `hotfix/*` | 紧急修复 | 临时 |

### 2.5 交付物

| 交付物 | 路径 | 状态 |
|--------|------|------|
| GitHub仓库 | 用户私有仓库 | 已创建 |
| README.md | `/README.md` | 已完成 |
| .gitignore | `/.gitignore` | 已完成 |
| 项目结构 | `/code/` | 已完成 |

---

## 3. T002: Docker开发环境配置

### 3.1 任务概述

使用Docker Compose配置完整的开发环境，包含PostgreSQL数据库、MinIO对象存储、后端服务和前端应用。通过容器化确保开发环境的一致性和可移植性。

### 3.2 需求描述

开发环境需要满足以下需求：
1. 多服务协同：数据库、存储、应用服务联动
2. 快速启动：一键启动完整开发环境
3. 数据持久化：保证数据在容器重启后不丢失
4. 健康检查：确保服务就绪后再启动依赖服务
5. 开发友好：支持热重载和调试

### 3.3 服务架构

采用微服务架构，通过Docker Compose编排5个核心服务：

```
┌─────────────────────────────────────────────────────────┐
│                   pdm-network (bridge)                  │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │postgres  │  │  minio   │  │ pgadmin  │              │
│  │  :5432   │  │:9000/9001│  │  :5050   │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│       │             │             │                      │
│  ┌────┴─────────────┴─────────────┴────┐               │
│  │           backend (FastAPI)         │               │
│  │               :8000                  │               │
│  └────────────────┬────────────────────┘               │
│                   │                                    │
│  ┌────────────────┴────────────────────┐              │
│  │           frontend (React)           │              │
│  │               :3000                  │              │
│  └──────────────────────────────────────┘              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 3.4 服务配置

#### 3.4.1 PostgreSQL数据库服务

```yaml
postgres:
  image: postgres:16-alpine
  container_name: pdm-postgres
  environment:
    POSTGRES_USER: pdm
    POSTGRES_PASSWORD: pdm123
    POSTGRES_DB: pdm
  ports:
    - "5432:5432"
  volumes:
    - postgres_data:/var/lib/postgresql/data
    - ./init-db.sql:/docker-entrypoint-initdb.d/init.sql
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U pdm"]
    interval: 10s
    timeout: 5s
    retries: 5
```

**配置说明**：
- 使用Alpine轻量镜像减小体积
- 数据卷持久化存储
- 自动执行init-db.sql初始化数据库
- 健康检查确保数据库就绪

#### 3.4.2 MinIO对象存储服务

```yaml
minio:
  image: minio/minio:latest
  container_name: pdm-minio
  environment:
    MINIO_ROOT_USER: pdmadmin
    MINIO_ROOT_PASSWORD: pdmadmin123456
  ports:
    - "9000:9000"      # API端口
    - "9001:9001"      # 控制台端口
  command: server /data --console-address ":9001"
  volumes:
    - minio_data:/data
```

**配置说明**：
- 同时暴露API和控制台端口
- 控制台端口9001便于管理
- S3兼容API便于后续迁移

#### 3.4.3 后端服务

```yaml
backend:
  build:
    context: ./backend
    dockerfile: Dockerfile.dev
  container_name: pdm-backend
  environment:
    DATABASE_URL: postgresql://pdm:pdm123@postgres:5432/pdm
    MINIO_ENDPOINT: minio:9000
    MINIO_ACCESS_KEY: pdmadmin
    MINIO_SECRET_KEY: pdmadmin123456
    JWT_SECRET_KEY: your-secret-key-change-in-production
  ports:
    - "8000:8000"
  volumes:
    - ./backend:/app
  depends_on:
    postgres:
      condition: service_healthy
    minio:
      condition: service_started
```

**配置说明**：
- 使用开发用Dockerfile支持热重载
- 挂载本地目录实现代码热更新
- 依赖健康检查确保启动顺序

#### 3.4.4 前端服务

```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile.dev
  container_name: pdm-frontend
  environment:
    VITE_API_URL: http://localhost:8000
    VITE_MINIO_ENDPOINT: http://localhost:9000
  ports:
    - "3000:3000"
  volumes:
    - ./frontend:/app
    - /app/node_modules
  depends_on:
    - backend
```

**配置说明**：
- 使用 `VITE_*` 前缀环境变量（Vite标准，非 `REACT_APP_*`）
- `VITE_MINIO_ENDPOINT` 用于前端直接访问MinIO控制台
- node_modules使用匿名卷避免覆盖
- 挂载源代码实现热更新

#### 3.4.5 pgAdmin数据库管理

```yaml
pgadmin:
  image: dpage/pgadmin4:latest
  container_name: pdm-pgadmin
  environment:
    PGADMIN_DEFAULT_EMAIL: admin@example.com
    PGADMIN_DEFAULT_PASSWORD: pdm123
  ports:
    - "5050:80"
```

### 3.5 网络设计

```yaml
networks:
  pdm-network:
    driver: bridge
```

所有服务加入同一bridge网络，服务间通过服务名通信（如`postgres:5432`）。

### 3.6 存储设计

```yaml
volumes:
  postgres_data:
    driver: local
  minio_data:
    driver: local
```

使用本地存储卷持久化数据，重启容器后数据不丢失。

### 3.7 环境变量

| 变量 | 服务 | 说明 | 默认值 |
|------|------|------|--------|
| `DATABASE_URL` | backend | 数据库连接串 | postgresql://pdm:pdm123@postgres:5432/pdm |
| `MINIO_ENDPOINT` | backend | MinIO服务地址 | minio:9000 |
| `MINIO_ACCESS_KEY` | backend | MinIO访问密钥 | pdmadmin |
| `MINIO_SECRET_KEY` | backend | MinIO密钥 | pdmadmin123456 |
| `MINIO_BUCKET` | backend | 存储桶名称 | pdm-documents |
| `JWT_SECRET_KEY` | backend | JWT密钥 | your-secret-key-change-in-production |
| `REACT_APP_API_URL` | frontend | API地址（已弃用） | ~~http://localhost:8000~~ → 使用 `VITE_API_URL` |
| `VITE_API_URL` | frontend | API地址 | http://localhost:8000 |
| `VITE_MINIO_ENDPOINT` | frontend | MinIO控制台地址 | http://localhost:9000 |

### 3.8 交付物

| 交付物 | 路径 | 状态 |
|--------|------|------|
| docker-compose.yml | `/code/docker-compose.yml` | 已完成 |
| 基础设施配置 | `/code/docker-compose-infra.yml` | 已完成 |
| 数据库初始化脚本 | `/code/init-db.sql` | 已完成 |

---

## 4. T003: FastAPI基础框架搭建

### 4.1 任务概述

搭建FastAPI后端基础框架，包含应用配置、数据库连接、模型定义、路由组织和中间件配置。这是后端服务的核心骨架。

### 4.2 需求描述

后端框架需要满足以下需求：
1. 快速启动：应用能快速启动并响应请求
2. 健康检查：提供系统健康状态端点
3. 数据库连接：支持PostgreSQL连接和会话管理
4. CORS配置：支持前端跨域请求
5. 模块化路由：按功能模块组织API路由
6. JWT认证：实现用户认证和授权

### 4.3 项目结构

```
backend/
├── main.py              # 应用入口，CORS配置，日志
├── config.py            # 配置管理（Pydantic Settings）
├── database.py          # 数据库连接和会话
├── models.py            # SQLAlchemy数据模型
├── schemas.py           # Pydantic请求/响应模式
├── deps.py              # JWT认证依赖注入
├── routers/             # API路由模块
│   ├── __init__.py     # 包初始化
│   ├── products.py     # 产品管理路由
│   └── auth.py         # 认证路由（登录/用户信息）
├── requirements.txt     # Python依赖
└── Dockerfile.dev       # 开发用Dockerfile
```

### 4.4 核心文件说明

#### 4.4.1 main.py - 应用入口

```python
import logging
from datetime import datetime
from typing import Dict

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

from config import settings
from database import engine, get_db
import models
import schemas
from routers import products
from routers import auth

# 日志配置
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PDM System API",
    description="Product Data Management System API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=schemas.HealthCheck)
async def health_check(db: Session = Depends(get_db)):
    """健康检查端点，检查数据库和MinIO连接状态"""
    db_healthy = False
    minio_healthy = False
    try:
        db.execute(sqlalchemy.text("SELECT 1"))
        db_healthy = True
    except SQLAlchemyError:
        db_healthy = False
    try:
        from minio import Minio
        minio_client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )
        minio_client.list_buckets()
        minio_healthy = True
    except Exception:
        minio_healthy = False
    return schemas.HealthCheck(
        status="healthy" if db_healthy and minio_healthy else "unhealthy",
        database=db_healthy,
        minio=minio_healthy,
        timestamp=datetime.utcnow(),
    )

# 注册路由
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
```

**关键特性**：
- 自动生成OpenAPI文档（/docs、/redoc）
- CORS中间件支持跨域请求
- 健康检查端点验证数据库和MinIO连接状态
- logging模块配置，支持DEBUG/INFO级别切换
- 产品路由和认证路由分离注册

#### 4.4.2 config.py - 配置管理

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 数据库
    database_url: str = "postgresql://pdm:pdm123@localhost:5432/pdm"
    
    # MinIO对象存储
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "pdm"
    minio_secret_key: str = "pdm123"
    minio_bucket: str = "pdm-documents"
    minio_secure: bool = False
    
    # JWT认证
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    
    # 应用配置
    environment: str = "development"
    debug: bool = True
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # AI功能
    enable_ai_features: bool = True
    ocr_language: str = "ch"
    embedding_model: str = "all-MiniLM-L6-v2"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**设计特点**：
- 使用Pydantic Settings管理配置
- 支持从环境变量读取
- 默认值适合本地开发

#### 4.4.3 database.py - 数据库连接

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    settings.database_url, 
    pool_pre_ping=True, 
    echo=settings.debug
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**关键特性**：
- `pool_pre_ping=True` 自动检测连接有效性
- `echo=settings.debug` 开发环境打印SQL
- 使用依赖注入获取数据库会话

#### 4.4.4 models.py - 数据模型

定义了4个核心数据模型：

| 模型 | 说明 | 主要字段 |
|------|------|----------|
| Product | 产品 | id, product_code, name, description, category, status, version |
| Document | 文档 | id, filename, filepath, file_size, product_id, version, ocr_text |
| BOMItem | BOM条目 | id, parent_product_id, child_product_id, quantity, unit |
| User | 用户 | id, username, email, hashed_password, role, is_active |

所有模型使用UUID作为主键，支持版本控制和软删除。

#### 4.4.5 schemas.py - Pydantic模式

为每个数据模型定义完整的Pydantic模式：

```python
class ProductBase(BaseSchema):
    product_code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    status: str = "draft"

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: uuid.UUID
    version: int
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime
```

**特点**：
- 数据验证和类型提示
- 自动文档生成
- ORM模式兼容

#### 4.4.6 deps.py - 依赖注入

实现JWT认证依赖，使用HTTPBearer scheme：

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from config import settings
from database import get_db
import models

oauth2_scheme = HTTPBearer(auto_error=False)

def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
) -> models.User:
    """验证JWT token并返回当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise credentials_exception
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """检查用户是否活跃"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user

def get_current_admin_user(
    current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    """检查用户是否是管理员"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user
```

**认证流程**：
1. `HTTPBearer` 从请求头 `Authorization: Bearer <token>` 提取凭据
2. `get_current_user` 解码JWT → 查询数据库 → 返回User对象
3. `get_current_active_user` 检查用户激活状态
4. `get_current_admin_user` 检查管理员角色

### 4.5 中间件配置

#### 4.5.1 CORS配置

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

允许前端跨域访问，开发环境使用`localhost:3000`。

### 4.6 API端点

#### 4.6.1 产品管理路由（products.py）

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | /products/ | 获取产品列表 | 公开 |
| GET | /products/{id} | 获取单个产品 | 公开 |
| POST | /products/ | 创建产品 | 需要 |
| PUT | /products/{id} | 更新产品 | 需要 |
| DELETE | /products/{id} | 删除产品 | 管理员 |

#### 4.6.2 认证路由（auth.py）

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /auth/login | 用户登录，获取JWT token | 公开（OAuth2表单） |
| GET | /auth/me | 获取当前用户信息 | 需要 |

**密码方案**：使用 `bcrypt` 库直接调用（非passlib），兼容 bcrypt>=5.0。

```python
import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )

def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
```

#### 4.6.3 系统端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 根路径返回应用信息 |
| GET | /health | 健康检查 |
| GET | /docs | OpenAPI文档 |
| GET | /redoc | ReDoc文档 |

### 4.7 依赖清单

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic[email]==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
bcrypt>=4.0.0
minio==7.2.2
httpx==0.25.2
alembic==1.12.1
pytest==7.4.3
pytest-cov==4.1.0
```

> **变更说明**：`passlib[bcrypt]==1.7.4` 已替换为 `bcrypt>=4.0.0`。原因是 passlib 与 bcrypt>=5.0 不兼容（passlib 的 bcrypt 后端在检测 wrap bug 时会触发 `ValueError: password cannot be longer than 72 bytes`）。直接使用 bcrypt 库更稳定、维护更活跃。

### 4.8 交付物

| 交付物 | 路径 | 状态 |
|--------|------|------|
| 应用入口 | `/code/backend/main.py` | 已完成 |
| 配置管理 | `/code/backend/config.py` | 已完成 |
| 数据库连接 | `/code/backend/database.py` | 已完成 |
| 数据模型 | `/code/backend/models.py` | 已完成 |
| Pydantic模式 | `/code/backend/schemas.py` | 已完成 |
| 认证依赖 | `/code/backend/deps.py` | 已完成（V&V验证通过） |
| 产品路由 | `/code/backend/routers/products.py` | 已完成 |
| 认证路由 | `/code/backend/routers/auth.py` | 已完成（V&V验证通过） |
| 路由包初始化 | `/code/backend/routers/__init__.py` | 已完成 |
| 依赖清单 | `/code/backend/requirements.txt` | 已完成 |

### 4.9 Bug修复记录

#### 4.9.1 初次修复（2026-03-29, commit `1f9551f`）

| 问题 | 描述 | 修复方案 |
|------|------|----------|
| models.py语法错误 | 第86行/98行枚举未定义错误，第155行缩进错误 | 修复语法和缩进 |
| PostgreSQL枚举冲突 | `LookupError: 'released' is not among the defined enum values` | 所有枚举列改为 `String(50)` |

#### 4.9.2 V&V审计修复（2026-03-29, commit `31e5550`）

基于V&V报告（`docs/07-specifications/VV-report.md`）发现的28个缺陷，修复了以下关键项：

| 缺陷ID | 文件 | 修复内容 |
|--------|------|----------|
| BUG-VV-001 | `deps.py` | 实现认证函数体（get_current_user/get_current_active_user/get_current_admin_user） |
| BUG-VV-002 | `models.py` | Document模型添加 `ocr_text` 和 `embedding` 字段 |
| BUG-VV-003 | `init-db.sql` | `file_size BIGINT` → `INTEGER` 统一类型 |
| BUG-VV-004 | `schemas.py` | Document schema添加 `Field(alias="metadata")` 映射 |
| BUG-VV-005 | `docker-compose.yml` | `REACT_APP_*` → `VITE_*` 环境变量名修正 |
| BUG-VV-008 | `routers/` | 创建 `__init__.py` 包初始化文件 |
| BUG-VV-010 | `frontend/src/api/products.ts` | 添加分页参数（skip/limit）支持 |
| BUG-VV-011 | `init-db.sql` | 补充 `idx_documents_status` 和 `idx_bom_items_child_product_id` 索引 |
| BUG-VV-012 | `main.py` | 添加logging配置，清理未使用导入，注册auth router |
| main.py语法错误 | `main.py:16` | `from routers import products,from routers import auth` → 分两行导入 |

#### 4.9.3 集成验证修复（2026-03-29, commit `33b93c1`）

集成测试阶段发现的额外问题：

| 问题 | 根因 | 修复 |
|------|------|------|
| `/auth/login` 返回500 | `passlib` 与 `bcrypt>=5.0` 不兼容 | `auth.py` 改用 `bcrypt` 库直接调用 |
| `/auth/me` 返回500 | `admin@pdm.local` 是保留域名，Pydantic email验证失败 | 改为 `admin@pdm-system.example.com` |
| `deps.py` token解析错误 | `HTTPBearer` 返回 `HTTPAuthorizationCredentials` 对象，非字符串 | 使用 `credentials.credentials` 访问token值 |
| `init-db.sql` 密码hash错误 | 原hash是 "secret" 而非 "admin123" 的bcrypt hash | 更新为正确的hash |
| `products.ts` 重复定义 | `productsApi` 对象被定义了两次 | 删除重复定义 |

#### 4.9.4 验证结果

| 指标 | 结果 |
|------|------|
| 后端单元测试 | ✅ 14/14 通过，覆盖率 89% |
| 后端集成测试 | ✅ 10/10 通过 |
| 前端 TypeScript 编译 | ✅ 0 错误 |
| Docker容器 | ✅ 5/5 healthy |
| 系统状态 | ✅ 完全可用 |

---

## 5. T004: React前端基础框架

### 5.1 任务概述

搭建React前端基础框架，采用模块化架构组织代码，使用TypeScript、Tailwind CSS和Zustand构建现代化前端应用。

### 5.2 需求描述

前端框架需要满足以下需求：
1. 类型安全：使用TypeScript保证类型安全
2. 样式方案：使用Tailwind CSS快速构建UI
3. 状态管理：使用Zustand管理应用状态
4. 路由管理：支持多页面路由
5. API交互：统一处理API请求和错误
6. 模块化：按功能模块组织代码

### 5.3 技术选型

| 技术 | 版本 | 选择理由 |
|------|------|----------|
| React | 18.2.0 | 主流UI库，生态丰富 |
| TypeScript | 5.3.2 | 类型安全，减少运行时错误 |
| Vite | 5.4.19 | 快速构建，热更新 |
| Tailwind CSS | 3.3.6 | 实用优先，响应式支持 |
| Zustand | 4.4.7 | 轻量级状态管理 |
| React Router | 6.20.0 | 声明式路由 |
| Axios | 1.6.2 | HTTP客户端 |
| Lucide React | 0.309.0 | 图标库 |
| date-fns | 3.0.6 | 日期处理 |

### 5.4 项目结构

```
frontend/
├── src/
│   ├── api/                    # API层
│   │   ├── client.ts          # Axios实例配置
│   │   └── products.ts        # 产品API封装
│   ├── components/            # 通用组件
│   │   ├── Layout.tsx         # 布局组件
│   │   ├── ErrorBoundary.tsx  # 错误边界
│   │   └── ui/                # UI组件
│   │       └── StatusBadge.tsx
│   ├── features/              # 功能模块
│   │   └── products/          # 产品模块
│   │       ├── pages/
│   │       │   └── ProductListPage.tsx
│   │       ├── components/
│   │       │   └── ProductTable.tsx
│   │       └── hooks/
│   │           └── useProducts.ts
│   ├── stores/                # 状态管理
│   │   └── products.ts        # 产品状态
│   ├── types/                 # 类型定义
│   │   ├── index.ts           # 导出入口
│   │   ├── product.ts         # 产品类型
│   │   └── api.ts             # API类型
│   ├── lib/                   # 工具函数
│   │   └── utils.ts           # 工具函数
│   ├── App.tsx                # 应用入口
│   ├── main.tsx               # 渲染入口
│   └── index.css              # 全局样式
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
└── postcss.config.js
```

### 5.5 核心配置

#### 5.5.1 vite.config.ts

```typescript
import path from 'path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    host: true,
  },
})
```

**配置特点**：
- 路径别名`@`指向src目录
- 端口3000与Docker配置一致
- host模式支持外部访问

#### 5.5.2 tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2023",
    "module": "ESNext",
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "moduleResolution": "bundler",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"]
}
```

**配置特点**：
- 严格模式开启
- 路径别名支持
- bundler模块解析

#### 5.5.3 tailwind.config.js

```javascript
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### 5.6 状态管理

#### 5.6.1 Zustand store设计

```typescript
interface ProductsState {
  items: Product[]
  loading: boolean
  error: string | null
  filters: ProductFilters
  setFilters: (filters: ProductFilters) => void
  fetchProducts: () => Promise<void>
}

export const useProductsStore = create<ProductsState>()(
  devtools(
    (set, get) => ({
      items: [],
      loading: false,
      error: null,
      filters: {},
      
      setFilters: (filters) => {
        set({ filters })
        get().fetchProducts()
      },
      
      fetchProducts: async () => {
        set({ loading: true, error: null })
        try {
          const response = await productsApi.getAll(get().filters)
          set({ items: response.data, loading: false })
        } catch (err) {
          set({ error: err instanceof Error ? err.message : 'Failed', loading: false })
        }
      },
    }),
    { name: 'products-store' }
  )
)
```

**设计特点**：
- 集成devtools支持调试
- 自动获取和更新产品列表
- 错误处理和加载状态

### 5.7 API层设计

#### 5.7.1 Axios客户端配置

```typescript
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 10000,
})

// 请求拦截：添加认证token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截：统一错误处理
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken')
    }
    return Promise.reject(error)
  }
)
```

### 5.8 组件架构

#### 5.8.1 App.tsx - 应用入口

```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Layout } from '@/components/Layout'
import ProductListPage from '@/features/products/pages/ProductListPage'

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<ProductListPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
```

#### 5.8.2 组件层次结构

```
App
├── BrowserRouter
├── Layout
│   └── Routes
│       └── ProductListPage
│           ├── ProductTable
│           │   └── StatusBadge
│           └── Error/Loading states
└── ErrorBoundary
```

### 5.9 类型定义

#### 5.9.1 产品类型（product.ts）

```typescript
export type ProductStatus = 'draft' | 'released' | 'obsolete'

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
```

### 5.10 交付物

| 交付物 | 路径 | 状态 |
|--------|------|------|
| 应用入口 | `/code/frontend/src/App.tsx` | 已完成 |
| 渲染入口 | `/code/frontend/src/main.tsx` | 已完成 |
| API客户端 | `/code/frontend/src/api/client.ts` | 已完成 |
| 产品API | `/code/frontend/src/api/products.ts` | 已完成 |
| Zustand store | `/code/frontend/src/stores/products.ts` | 已完成 |
| 类型定义 | `/code/frontend/src/types/` | 已完成 |
| 通用组件 | `/code/frontend/src/components/` | 已完成 |
| 功能模块 | `/code/frontend/src/features/products/` | 已完成 |
| 配置文件 | `/code/frontend/package.json` 等 | 已完成 |

---

## 6. 验收标准汇总

### 6.1 T001验收标准

| 验收项 | 状态 | 说明 |
|--------|------|------|
| 仓库创建 | ✓ | GitHub仓库已创建 |
| 目录结构 | ✓ | 按设计结构组织 |
| .gitignore | ✓ | 覆盖所有常见类型 |
| README | ✓ | 项目说明完整 |

### 6.2 T002验收标准

| 验收项 | 状态 | 说明 |
|--------|------|------|
| 服务数量 | ✓ | 5个服务正常运行 |
| 数据库 | ✓ | PostgreSQL可连接 |
| 对象存储 | ✓ | MinIO可访问 |
| 健康检查 | ✓ | 服务依赖正确 |
| 数据持久化 | ✓ | 卷配置正确 |

### 6.3 T003验收标准

| 验收项 | 状态 | 说明 |
|--------|------|------|
| 应用启动 | ✓ | FastAPI可启动 |
| 文档访问 | ✓ | /docs 可访问 |
| 健康检查 | ✓ | /health 返回状态 |
| 产品CRUD | ✓ | 基础API可用 |
| 认证依赖 | ✓ | JWT认证已实现 |

### 6.4 T004验收标准

| 验收项 | 状态 | 说明 |
|--------|------|------|
| 应用启动 | ✓ | React应用可启动 |
| 类型检查 | ✓ | TypeScript无错误 |
| 样式配置 | ✓ | Tailwind CSS可用 |
| 状态管理 | ✓ | Zustand工作正常 |
| API调用 | ✓ | 可调用后端API |

---

## 7. 附录

### 7.1 术语表

| 术语 | 说明 |
|------|------|
| PDM | Product Data Management，产品数据管理 |
| FastAPI | Python异步Web框架 |
| SQLAlchemy | Python ORM框架 |
| Pydantic | Python数据验证库 |
| Zustand | React状态管理库 |
| MinIO | S3兼容对象存储 |
| CORS | Cross-Origin Resource Sharing，跨域资源共享 |
| JWT | JSON Web Token，JSON网络令牌 |
| UUID | 通用唯一标识符 |
| ORM | Object-Relational Mapping，对象关系映射 |

### 7.2 参考链接

| 资源 | 链接 |
|------|------|
| FastAPI文档 | https://fastapi.tiangolo.com/ |
| SQLAlchemy文档 | https://docs.sqlalchemy.org/ |
| React文档 | https://react.dev/ |
| TypeScript手册 | https://www.typescriptlang.org/docs/ |
| Tailwind CSS | https://tailwindcss.com/docs |
| Zustand | https://github.com/pmndrs/zustand |
| Docker文档 | https://docs.docker.com/ |

### 7.3 变更记录

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v1.0.0 | 2026-03-27 | 初始版本，完成T001-T004设计文档 |
| v1.1.0 | 2026-03-29 | T003 bug修复：models.py枚举类型修复 |
| v2.0.0 | 2026-03-29 | V&V验证修复：passlib→bcrypt迁移、认证路由auth.py、deps.py完整实现、Docker环境变量VITE_*、集成测试全部通过 |

---

*本文档为P0阶段详细设计说明书，记录项目初始化和基础框架的完整设计方案。*