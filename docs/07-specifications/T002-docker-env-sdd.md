# T002: Docker开发环境配置 - SDD规格说明文档

## 文档信息

| 项目 | 内容 |
|------|------|
| 文档ID | SPEC-T002 |
| 版本 | v1.0.0 |
| 状态 | 已完成 |
| 创建日期 | 2026-03-29 |
| 关联任务 | T002 |
| 完成日期 | 2026-03-27 |

---

## 1. 概述

### 1.1 目的
本文档采用规格驱动开发（SDD）方法，定义Docker开发环境的功能需求、非功能需求、技术约束和验收标准。

### 1.2 范围
- Docker Compose多服务编排
- PostgreSQL数据库容器
- MinIO对象存储容器
- FastAPI后端容器
- React前端容器
- pgAdmin数据库管理工具
- 网络与数据卷管理

### 1.3 术语定义

> 完整术语和共享数据类型定义参见 [SDD共享数据字典](./SDD-data-dictionary.md)。

| 术语 | 定义 |
|------|------|
| SDD | Specification-Driven Development，规格驱动开发 |
| FR | Functional Requirement，功能需求 |
| NFR | Non-Functional Requirement，非功能需求 |
| TC | Technical Constraint，技术约束 |

---

## 2. 功能需求规格

### FR-001: Docker Compose编排

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-001 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：使用Docker Compose编排多服务开发环境，一条命令启动全部服务

**验收标准**：
- [x] AC-001.1: `docker compose up` 可启动全部服务
- [x] AC-001.2: 服务间依赖关系正确（backend依赖postgres和minio）
- [x] AC-001.3: 使用 `pdm-network` 桥接网络实现服务间通信
- [x] AC-001.4: 定义持久化数据卷（`postgres_data`, `minio_data`）

**实现文件**：
- `/code/docker-compose.yml`

**服务依赖关系**：
```
frontend → backend → postgres (healthcheck)
                  → minio
                  → pgadmin → postgres
```

---

### FR-002: PostgreSQL数据库服务

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-002 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：配置PostgreSQL 16数据库作为主数据存储

**验收标准**：
- [x] AC-002.1: 使用 `postgres:16-alpine` 镜像
- [x] AC-002.2: 容器名 `pdm-postgres`
- [x] AC-002.3: 数据库凭据配置（user: pdm, db: pdm）
- [x] AC-002.4: 端口映射 `5432:5432`
- [x] AC-002.5: 健康检查 `pg_isready -U pdm`（间隔10s, 超时5s, 重试5次）
- [x] AC-002.6: 持久化数据卷 `postgres_data`
- [x] AC-002.7: 初始化SQL脚本挂载 `init-db.sql`

**配置规格**：
```yaml
postgres:
  image: postgres:16-alpine
  container_name: pdm-postgres
  environment:
    POSTGRES_USER: pdm
    POSTGRES_PASSWORD: pdm123
    POSTGRES_DB: pdm
  ports: ["5432:5432"]
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U pdm"]
    interval: 10s
    timeout: 5s
    retries: 5
```

---

### FR-003: MinIO对象存储服务

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-003 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：配置MinIO作为S3兼容对象存储，用于文档管理

**验收标准**：
- [x] AC-003.1: 使用 `minio/minio:latest` 镜像
- [x] AC-003.2: 容器名 `pdm-minio`
- [x] AC-003.3: API端口 `9000`，控制台端口 `9001`
- [x] AC-003.4: 健康检查（`/minio/health/live`）
- [x] AC-003.5: 持久化数据卷 `minio_data`
- [x] AC-003.6: MinIO控制台可通过 `http://localhost:9001` 访问

**配置规格**：
```yaml
minio:
  image: minio/minio:latest
  container_name: pdm-minio
  environment:
    MINIO_ROOT_USER: pdmadmin
    MINIO_ROOT_PASSWORD: pdmadmin123456
  ports: ["9000:9000", "9001:9001"]
  command: server /data --console-address ":9001"
```

---

### FR-004: FastAPI后端服务

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-004 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：配置FastAPI后端容器，支持热重载开发

**验收标准**：
- [x] AC-004.1: 使用 `Dockerfile.dev` 构建
- [x] AC-004.2: 基础镜像 `python:3.11-slim`
- [x] AC-004.3: 源码挂载到 `/app`（热重载）
- [x] AC-004.4: 端口映射 `8000:8000`
- [x] AC-004.5: 环境变量注入（DATABASE_URL, MINIO_*, JWT_SECRET_KEY）
- [x] AC-004.6: 启动命令 `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
- [x] AC-004.7: 依赖postgres健康检查通过后才启动

**Dockerfile规格**：
```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**环境变量规格**：
```yaml
environment:
  DATABASE_URL: postgresql://pdm:pdm123@postgres:5432/pdm
  MINIO_ENDPOINT: minio:9000
  MINIO_ACCESS_KEY: pdmadmin
  MINIO_SECRET_KEY: pdmadmin123456
  MINIO_BUCKET: pdm-documents
  JWT_SECRET_KEY: your-secret-key-change-in-production
  ENVIRONMENT: development
```

---

### FR-005: React前端服务

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-005 |
| **优先级** | P0 |
| **状态** | ✅ 已实现 |

**描述**：配置React前端容器，支持热重载开发

**验收标准**：
- [x] AC-005.1: 使用 `Dockerfile.dev` 构建
- [x] AC-005.2: 基础镜像 `node:20-alpine`
- [x] AC-005.3: 源码挂载到 `/app`（热重载）
- [x] AC-005.4: `node_modules` 使用容器内独立卷
- [x] AC-005.5: 端口映射 `3000:3000`
- [x] AC-005.6: 启动命令 `npm run dev -- --host`

**Dockerfile规格**：
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host"]
```

---

### FR-006: pgAdmin管理工具

| 属性 | 值 |
|------|-----|
| **需求ID** | FR-006 |
| **优先级** | P1 |
| **状态** | ✅ 已实现 |

**描述**：配置pgAdmin作为PostgreSQL可视化管理工具

**验收标准**：
- [x] AC-006.1: 使用 `dpage/pgadmin4:latest` 镜像
- [x] AC-006.2: 端口映射 `5050:80`
- [x] AC-006.3: 通过 `http://localhost:5050` 可访问管理界面
- [x] AC-006.4: 登录凭据配置（admin@example.com / pdm123）

---

## 3. 非功能需求规格

### NFR-001: 服务可靠性

| 属性 | 值 |
|------|-----|
| **需求ID** | NFR-001 |
| **优先级** | P0 |
| **状态** | ✅ 已满足 |

**描述**：关键服务应具备健康检查和自动重启能力

**验收标准**：
- [x] AC-NFR-001.1: PostgreSQL具备健康检查（pg_isready）
- [x] AC-NFR-001.2: MinIO具备健康检查（/minio/health/live）
- [x] AC-NFR-001.3: backend和frontend配置 `restart: unless-stopped`

---

### NFR-002: 开发体验

| 属性 | 值 |
|------|-----|
| **需求ID** | NFR-002 |
| **优先级** | P0 |
| **状态** | ✅ 已满足 |

**描述**：开发环境应支持代码热重载，无需重建容器

**验收标准**：
- [x] AC-NFR-002.1: 后端代码变更自动生效（uvicorn --reload）
- [x] AC-NFR-002.2: 前端代码变更自动生效（Vite HMR）
- [x] AC-NFR-002.3: 源码通过volume挂载，不依赖镜像重建

---

### NFR-003: 数据持久化

| 属性 | 值 |
|------|-----|
| **需求ID** | NFR-003 |
| **优先级** | P0 |
| **状态** | ✅ 已满足 |

**描述**：数据库和对象存储数据应在容器重启后保留

**验收标准**：
- [x] AC-NFR-003.1: PostgreSQL数据持久化到 `postgres_data` 卷
- [x] AC-NFR-003.2: MinIO数据持久化到 `minio_data` 卷

---

## 4. 技术约束

| 约束ID | 描述 | 理由 |
|--------|------|------|
| TC-001 | PostgreSQL版本: 16-alpine | Alpine镜像更小，版本足够新 |
| TC-002 | Node.js版本: 20-alpine | LTS版本，稳定可靠 |
| TC-003 | Python版本: 3.11-slim | 兼容性好，镜像适中 |
| TC-004 | 使用bridge网络 | 容器间DNS解析，与宿主机隔离 |
| TC-005 | 开发环境不使用HTTPS | 简化本地开发 |
| TC-006 | 默认密码仅用于开发 | 生产环境必须更换 |

---

## 5. 端口映射表

| 服务 | 容器内端口 | 宿主机端口 | 用途 |
|------|-----------|-----------|------|
| PostgreSQL | 5432 | 5432 | 数据库 |
| MinIO API | 9000 | 9000 | 对象存储API |
| MinIO Console | 9001 | 9001 | MinIO管理界面 |
| FastAPI | 8000 | 8000 | 后端API + Swagger文档 |
| React | 3000 | 3000 | 前端开发服务器 |
| pgAdmin | 80 | 5050 | 数据库管理工具 |

---

## 6. 验证矩阵

| 需求ID | 验证方法 | 验证结果 | 日期 |
|--------|----------|----------|------|
| FR-001 | `docker compose up` 全部服务启动 | ✅ 通过 | 2026-03-27 |
| FR-002 | PostgreSQL连接测试 | ✅ 通过 | 2026-03-27 |
| FR-003 | MinIO控制台访问 http://localhost:9001 | ✅ 通过 | 2026-03-27 |
| FR-004 | 后端API访问 http://localhost:8000/docs | ✅ 通过 | 2026-03-27 |
| FR-005 | 前端访问 http://localhost:3000 | ✅ 通过 | 2026-03-27 |
| FR-006 | pgAdmin访问 http://localhost:5050 | ✅ 通过 | 2026-03-27 |
| NFR-001 | 健康检查验证 | ✅ 通过 | 2026-03-27 |
| NFR-002 | 代码热重载测试 | ✅ 通过 | 2026-03-27 |
| NFR-003 | 容器重启后数据保留 | ✅ 通过 | 2026-03-27 |

---

## 7. 变更记录

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v1.0.0 | 2026-03-29 | 初始版本，基于已完成的T002实现追溯创建SDD规格 |

---

*本文档采用规格驱动开发（SDD）方法编写，作为T002任务的规格基准。*
