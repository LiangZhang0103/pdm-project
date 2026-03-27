# 技术栈文档

## 技术选型原则
1. **学习友好**：文档丰富，社区活跃，易于上手
2. **就业相关**：市场需求大，技能通用性强
3. **AI生态好**：便于集成AI/ML功能
4. **现代化**：采用当前主流和趋势技术
5. **成本可控**：有免费或低成本方案

## 整体技术架构

```
┌─────────────────────────────────┐
│          前端层                 │
│  • React 18 + TypeScript       │
│  • Tailwind CSS               │
│  • React Query / Zustand       │
│  • Vite 构建工具              │
├─────────────────────────────────┤
│          后端层                 │
│  • FastAPI (Python)           │
│  • SQLAlchemy (ORM)           │
│  • Pydantic (数据验证)         │
│  • Alembic (数据库迁移)        │
├─────────────────────────────────┤
│          数据层                 │
│  • PostgreSQL 15+             │
│  • pgvector (向量扩展)         │
│  • MinIO / S3 (文件存储)       │
│  • Redis (缓存)               │
├─────────────────────────────────┤
│          AI/ML层               │
│  • PaddleOCR (文档OCR)         │
│  • spaCy / transformers (NLP)  │
│  • sentence-transformers       │
│  • scikit-learn (机器学习)     │
├─────────────────────────────────┤
│          运维层                 │
│  • Docker + Docker Compose    │
│  • Vercel (前端部署)          │
│  • Railway (后端部署)         │
│  • GitHub Actions (CI/CD)     │
└─────────────────────────────────┘
```

## 前端技术栈

### React 18 + TypeScript
**选择理由**：
- 市场需求最大，就业机会最多
- 生态丰富，学习资源充足
- TypeScript提供类型安全，减少错误
- React Hooks和函数组件现代化

**核心依赖**：
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "typescript": "^5.0.0",
  "@types/react": "^18.2.0",
  "@types/react-dom": "^18.2.0"
}
```

**学习资源**：
- [React官方文档](https://react.dev/learn)
- [TypeScript手册](https://www.typescriptlang.org/docs/)
- [React TypeScript教程](https://react-typescript-cheatsheet.netlify.app/)

### Tailwind CSS
**选择理由**：
- 实用优先，开发效率高
- 响应式设计内置支持
- 自定义灵活，设计系统友好
- 社区活跃，组件丰富

**配置示例**：
```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#10b981',
      }
    }
  }
}
```

### 状态管理
**方案选择**：
- **React Query**：服务器状态管理（API数据）
- **Zustand**：客户端状态管理（UI状态）
- **Context API**：简单状态共享

**使用场景**：
```typescript
// React Query示例
import { useQuery } from '@tanstack/react-query';

function ProductList() {
  const { data, isLoading } = useQuery({
    queryKey: ['products'],
    queryFn: fetchProducts
  });
  
  // Zustand示例
  const useStore = create((set) => ({
    user: null,
    setUser: (user) => set({ user })
  }));
}
```

### 组件库
**选择策略**：
- **初期**：使用Headless UI + 自定义样式
- **中期**：引入Shadcn/ui或Radix UI
- **后期**：根据需求选择专业组件库

**推荐组件**：
- **表单**：React Hook Form + Zod验证
- **表格**：TanStack Table
- **图标**：Lucide React
- **日期**：React Date Picker

## 后端技术栈

### FastAPI
**选择理由**：
- 性能优秀，媲美Node.js和Go
- 自动API文档生成（OpenAPI/Swagger）
- 类型提示和验证（Pydantic）
- 异步支持好，适合IO密集型应用
- Python生态，AI集成方便

**项目结构**：
```
backend/
├── app/
│   ├── api/          # 路由端点
│   ├── models/       # 数据模型
│   ├── schemas/      # Pydantic模式
│   ├── services/     # 业务逻辑
│   ├── core/         # 核心配置
│   └── utils/        # 工具函数
├── alembic/          # 数据库迁移
├── tests/            # 测试文件
└── requirements.txt  # 依赖管理
```

**核心配置**：
```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="PDM API",
    description="产品数据管理API",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### SQLAlchemy + Alembic
**选择理由**：
- Python最成熟的ORM
- 支持多种数据库后端
- 迁移工具Alembic成熟稳定
- 表达能力强大，支持复杂查询

**模型定义示例**：
```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_number = Column(String(50), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### Pydantic
**作用**：
- 请求/响应数据验证
- 类型提示和自动文档生成
- 数据序列化/反序列化

**示例**：
```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    product_number: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    
class ProductResponse(ProductCreate):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True
```

## 数据库技术栈

### PostgreSQL 15+
**选择理由**：
- 功能最丰富的开源关系数据库
- JSONB支持好，灵活性和性能平衡
- 扩展丰富（pgvector、PostGIS等）
- 成熟稳定，生产验证

**关键配置**：
```sql
-- 启用扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgvector";

-- 性能优化配置
-- 在postgresql.conf中调整
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
```

### pgvector扩展
**作用**：向量存储和相似度搜索
**应用场景**：语义搜索、推荐系统

**使用示例**：
```sql
-- 创建向量列
ALTER TABLE documents ADD COLUMN embedding vector(768);

-- 创建向量索引
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops);

-- 相似度搜索
SELECT id, content, 
       1 - (embedding <=> '[0.1,0.2,...]') as similarity
FROM documents
ORDER BY embedding <=> '[0.1,0.2,...]'
LIMIT 10;
```

### Redis
**用途**：
- 会话存储
- API速率限制
- 缓存热点数据
- 任务队列

**配置示例**：
```python
# Redis连接
import redis
from redis import ConnectionPool

pool = ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)
redis_client = redis.Redis(connection_pool=pool)
```

## 文件存储

### MinIO（S3兼容）
**选择理由**：
- 开源，可自建
- S3 API兼容，迁移成本低
- 性能优秀，支持大文件
- 有免费版本

**配置示例**：
```python
import boto3
from botocore.client import Config

s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin',
    config=Config(signature_version='s3v4')
)

# 上传文件
s3_client.upload_file(
    'local_file.pdf',
    'pdm-documents',
    'uploads/document.pdf'
)
```

## AI/ML技术栈

### 文档处理
**PaddleOCR**：
- 优点：中文OCR效果好，开源免费
- 缺点：模型较大，部署稍复杂
- 适用：图片/PDF文字提取

```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='ch')
result = ocr.ocr('document.jpg', cls=True)
```

**spaCy**：
- 优点：工业级NLP，速度快
- 缺点：需要训练自定义模型
- 适用：实体识别、关系提取

```python
import spacy

nlp = spacy.load("zh_core_web_sm")
doc = nlp("主轴组件材料为45#钢，直径50mm")
for ent in doc.ents:
    print(ent.text, ent.label_)
```

### 向量嵌入
**sentence-transformers**：
- 优点：多语言支持，预训练模型丰富
- 缺点：模型加载较慢
- 适用：文本向量化，语义搜索

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings = model.encode(["文本1", "文本2"])
```

### 机器学习
**scikit-learn**：
- 优点：算法全面，文档优秀
- 缺点：深度学习支持有限
- 适用：传统机器学习任务

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

## 开发运维

### Docker
**容器化方案**：
```dockerfile
# 后端Dockerfile示例
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml**：
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: pdm
      POSTGRES_PASSWORD: pdm123
      POSTGRES_DB: pdm_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
  
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
  
  backend:
    build: ./backend
    depends_on:
      - postgres
      - redis
      - minio
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"

volumes:
  postgres_data:
```

### 部署服务
**前端部署**：Vercel
- 免费额度充足
- 自动HTTPS和CDN
- 与GitHub集成好

**后端部署**：Railway
- 免费额度适合小型项目
- 支持数据库和缓存
- 部署简单

**监控告警**：
- **应用监控**：Sentry（错误追踪）
- **性能监控**：Datadog或New Relic（可选）
- **日志收集**：Papertrail或Loggly（可选）

## 开发工具链

### 代码质量
```json
// package.json 前端
{
  "scripts": {
    "lint": "eslint src --ext ts,tsx",
    "format": "prettier --write src",
    "type-check": "tsc --noEmit"
  }
}
```

```ini
# .pre-commit-config.yaml 后端
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
```

### 测试工具
**前端测试**：
- Vitest：测试框架
- React Testing Library：组件测试
- MSW：API模拟

**后端测试**：
- pytest：测试框架
- pytest-asyncio：异步测试
- pytest-cov：覆盖率

### CI/CD
**GitHub Actions配置**：
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest --cov=app
```

## 学习路径建议

### 第1-2周：基础掌握
1. React基础（组件、状态、Hooks）
2. FastAPI基础（路由、依赖、中间件）
3. PostgreSQL基础（SQL、索引、事务）

### 第3-4周：进阶技能
1. TypeScript高级特性
2. SQLAlchemy关系映射
3. Docker容器化

### 第5-6周：AI入门
1. PaddleOCR基础使用
2. spaCy实体识别
3. 向量搜索概念

### 第7-8周：系统集成
1. 前后端完整数据流
2. 文件上传处理
3. 认证授权系统

### 第9-12周：优化完善
1. 性能优化
2. 测试覆盖
3. 部署运维

## 备选技术栈

### 前端备选
- **Vue 3**：更易上手，生态完善
- **Svelte**：编译时框架，性能优秀
- **Next.js**：全栈框架，SSR支持

### 后端备选
- **Django**：更重但更完整，内置功能多
- **Flask**：更轻量，更灵活
- **Go + Gin**：性能更好，学习曲线陡

### 数据库备选
- **MySQL**：更简单，生态丰富
- **MongoDB**：文档型，适合非结构化数据
- **Supabase**：BaaS，开发速度快

## 技术债务管理

### 已知技术债务
1. **初期**：代码结构可能不够优化
   - 计划：第2个月进行重构
   
2. **测试覆盖**：初期测试可能不完善
   - 计划：核心功能测试先行

3. **安全性**：初期安全措施可能不足
   - 计划：逐步添加安全特性

### 技术升级计划
1. **3个月后**：评估新技术采用
2. **6个月后**：考虑架构演进
3. **1年后**：技术栈全面评估

---
*技术栈选择是平衡的艺术，没有完美方案，只有适合当前需求的方案。*