# System Architecture Document

## Document Information

| Property | Value |
|-----------|-------|
| Version | 1.0 |
| Status | Draft |
| Created | 2026-03-27 |
| Author | PDM Project |

---

## 1. Architecture Overview

### 1.1 System Purpose

The Product Data Management (PDM) System is a web-based application designed to manage product lifecycle data with integrated AI capabilities for document processing and semantic search.

### 1.2 Architecture Style

```
┌─────────────────────────────────────────────────────────────────┐
│                        Architecture Style                        │
├─────────────────────────────────────────────────────────────────┤
│  • Pattern: Client-Server with RESTful API                     │
│  • Frontend: Single Page Application (SPA)                      │
│  • Backend: Microservices-ready Monolith                        │
│  • Data: Relational Database with Vector Extension              │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        A[React SPA<br/>TypeScript<br/>Tailwind CSS]
    end
    
    subgraph "API Gateway Layer"
        B[FastAPI<br/>Port 8000]
    end
    
    subgraph "Application Layer"
        C[Auth Service]
        D[Product Service]
        E[Document Service]
        F[BOM Service]
        G[AI Service]
    end
    
    subgraph "Data Layer"
        H[PostgreSQL<br/>Port 5432]
        I[MinIO<br/>Port 9000]
        J[pgvector<br/>Extension]
    end
    
    A -->|HTTPS| B
    B --> C
    B --> D
    B --> E
    B --> F
    B --> G
    
    C --> H
    D --> H
    E --> H
    E --> I
    F --> H
    G --> H
    G --> J
```

---

## 2. Design Principles

### 2.1 Core Principles

| Principle | Description | Application |
|------------|-------------|-------------|
| **Separation of Concerns** | Each layer has distinct responsibilities | API, Service, Repository layers |
| **Stateless Design** | APIs don't maintain client state | JWT authentication |
| **RESTful Conventions** | Resource-based URLs, HTTP verbs | /products, /documents |
| **Configuration over Code** | Environment-driven configuration | .env files, config.py |
| **Fail Fast** | Early validation and error reporting | Pydantic validation |

### 2.2 Technology Principles

| Principle | Implementation |
|------------|----------------|
| Type Safety | TypeScript (frontend), Pydantic (backend) |
| Immutability | React immutability, Python frozen configs |
| Minimal Dependencies | Core dependencies only, feature flags |
| Observability | Structured logging, health endpoints |

---

## 3. Component Architecture

### 3.1 Frontend Components

```mermaid
graph LR
    subgraph "React Application"
        A[App.tsx<br/>Router] --> B[Layout]
        B --> C[Pages]
        B --> D[Components]
        D --> E[UI Components]
        D --> F[Feature Components]
        C --> G[ProductListPage]
        C --> H[AuthPages]
    end
    
    subgraph "State Management"
        I[Zustand Store] --> F
        J[React Query] --> K[API Client]
    end
    
    F --> K
    K -->|HTTP| L[Backend API]
```

### 3.2 Backend Components

```mermaid
graph TB
    subgraph "FastAPI Application"
        A[main.py<br/>App Entry] --> B[Middleware]
        B --> C[Router Layer]
        C --> D[products.py]
        C --> E[documents.py]
        C --> F[bom.py]
        C --> G[auth.py]
        
        D --> H[Service Layer]
        E --> H
        F --> H
        G --> H
        
        H --> I[Repository Layer]
        I --> J[SQLAlchemy ORM]
    end
    
    J --> K[(PostgreSQL)]
    I --> L[(MinIO)]
```

### 3.3 Component Responsibilities

| Component | Responsibility | Public API |
|-----------|----------------|------------|
| **Router** | Request routing, CORS | FastAPI router |
| **Service** | Business logic | Python functions |
| **Repository** | Data access | SQLAlchemy queries |
| **Schema** | Data validation | Pydantic models |
| **Middleware** | Cross-cutting concerns | Auth, logging |

---

## 4. Layer Architecture

### 4.1 Backend Layers

```
┌─────────────────────────────────────────┐
│           Presentation Layer             │
│  (Routers: products.py, auth.py, etc.)  │
├─────────────────────────────────────────┤
│            Service Layer                │
│  (Business logic, validation)            │
├─────────────────────────────────────────┤
│          Repository Layer               │
│  (Data access, queries)                  │
├─────────────────────────────────────────┤
│            Database Layer                │
│  (SQLAlchemy, models.py)                 │
└─────────────────────────────────────────┘
```

### 4.2 Frontend Layers

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│       (Pages, Components)               │
├─────────────────────────────────────────┤
│          State Layer                     │
│    (Zustand stores, React Query)        │
├─────────────────────────────────────────┤
│          API Layer                       │
│     (Axios client, endpoints)           │
└─────────────────────────────────────────┘
```

---

## 5. Data Flow

### 5.1 Request Flow

```
User Action
    ↓
React Component
    ↓
API Client (Axios)
    ↓
HTTP Request
    ↓
FastAPI Router
    ↓ (auth middleware)
Service Layer
    ↓
Repository Layer
    ↓
SQLAlchemy → PostgreSQL
    ↓
Response (JSON)
    ↓
React Query Cache
    ↓
UI Update
```

### 5.2 File Upload Flow

```
User selects file
    ↓
React FormData
    ↓
POST /documents (multipart)
    ↓
FastAPI router validates
    ↓
Service: upload_to_minio()
    ↓
MinIO S3 API
    ↓
Store metadata in PostgreSQL
    ↓
Return document record
```

---

## 6. Infrastructure Architecture

### 6.1 Development Environment

```yaml
Services:
  frontend:
    image: pdm-frontend:latest
    ports: [3000:3000]
    depends_on: [backend]
    
  backend:
    image: pdm-backend:latest
    ports: [8000:8000]
    environment:
      - DATABASE_URL=postgresql://pdm:pdm123@postgres:5432/pdm_db
      - MINIO_ENDPOINT=minio:9000
    
  postgres:
    image: postgres:15
    ports: [5432:5432]
    volumes: [postgres_data:/var/lib/postgresql/data]
    
  minio:
    image: minio/minio
    ports: [9000:9000, 9001:9001]
    command: server /data --console-address ":9001"
    
  pgadmin:
    image: dpage/pgadmin4
    ports: [5050:80]
```

### 6.2 Production Architecture (Future)

```yaml
# Planned production deployment
Frontend:
  - Platform: Vercel
  - CDN: Global
  - SSL: Automatic
  
Backend:
  - Platform: Railway
  - Instances: Auto-scaling
  - Region: us-east
  
Database:
  - Platform: Railway PostgreSQL
  - Backup: Daily
  
Storage:
  - Platform: Cloudflare R2
  - CDN: Global
  
Monitoring:
  - Logs: Papertrail
  - Errors: Sentry
  - Uptime: Health checks
```

---

## 7. Module Design

### 7.1 Backend Modules

| Module | Path | Responsibility |
|--------|------|----------------|
| **config** | /config.py | Settings, environment |
| **database** | /database.py | DB connection, session |
| **models** | /models.py | SQLAlchemy models |
| **schemas** | /schemas.py | Pydantic schemas |
| **deps** | /deps.py | Dependencies (auth) |
| **routers** | /routers/ | API endpoints |

### 7.2 Frontend Modules

| Module | Path | Responsibility |
|--------|------|----------------|
| **api** | /src/api/ | API client, endpoints |
| **components** | /src/components/ | Shared UI components |
| **features** | /src/features/ | Feature-based modules |
| **stores** | /src/stores/ | Zustand stores |
| **types** | /src/types/ | TypeScript types |
| **lib** | /src/lib/ | Utilities |

### 7.3 Feature Module Structure

```
features/products/
├── components/       # Product-specific UI components
│   ├── ProductTable.tsx
│   └── ProductForm.tsx
├── hooks/            # Custom React hooks
│   └── useProducts.ts
├── pages/            # Page components
│   └── ProductListPage.tsx
└── index.ts          # Module exports
```

---

## 8. API Design

### 8.1 API Structure

```
/api/v1
├── /health           # System health
├── /auth             # Authentication
│   ├── POST /login
│   ├── POST /register
│   └── POST /refresh
├── /products         # Product management
│   ├── GET /         # List products
│   ├── POST /        # Create product
│   ├── GET /{id}     # Get product
│   ├── PUT /{id}     # Update product
│   └── DELETE /{id}  # Delete product
├── /documents        # Document management
│   ├── POST /        # Upload document
│   ├── GET /{id}     # Get document
│   └── GET /{id}/download
└── /bom              # BOM management
    ├── GET /         # List BOM items
    ├── POST /        # Create BOM item
    └── PUT /{id}     # Update BOM item
```

### 8.2 Response Standards

```json
// Success Response
{
  "data": { ... },
  "message": "Success"
}

// Error Response
{
  "detail": "Error message"
}

// List Response
{
  "items": [...],
  "total": 100,
  "page": 1,
  "limit": 10
}
```

---

## 9. Security Architecture

### 9.1 Authentication Flow

```
User Login
    ↓
POST /auth/login
    ↓
Validate credentials
    ↓
Generate JWT token (HS256)
    ↓
Return access_token
    ↓
Client stores in memory/localStorage
    ↓
Subsequent requests include:
Authorization: Bearer <token>
    ↓
Middleware validates token
    ↓
Extract user_id and role
    ↓
Check endpoint permissions
```

### 9.2 Security Measures

| Layer | Measure |
|-------|---------|
| Transport | HTTPS (production) |
| Authentication | JWT with expiration |
| Password | bcrypt hashing |
| Authorization | Role-based (user/admin) |
| CORS | Restricted origins |
| Input Validation | Pydantic schemas |
| SQL Injection | SQLAlchemy parameterized |
| XSS | React escaping |
| File Upload | Type validation, size limit |

---

## 10. Performance Architecture

### 10.1 Caching Strategy

| Data Type | Cache | TTL |
|-----------|-------|-----|
| Product list | React Query | 5 min |
| Product detail | React Query | 1 min |
| User session | Memory | 1 hour |
| Static assets | Browser | 1 day |

### 10.2 Database Optimization

| Technique | Application |
|-----------|-------------|
| Indexes | FK, unique fields, frequently filtered |
| Pagination | Offset/limit on lists |
| Connection Pool | 20 max connections |
| Lazy Loading | Relationships loaded on demand |

### 10.3 API Performance

| Metric | Target |
|--------|--------|
| API Response | < 500ms (p95) |
| File Upload | < 10s (100MB) |
| Page Load | < 2s (initial) |
| Database Query | < 100ms |

---

## 11. Observability

### 11.1 Health Checks

| Endpoint | Purpose |
|----------|---------|
| GET /health | Overall system health |
| GET /health/database | Database connectivity |
| GET /health/minio | MinIO connectivity |

### 11.2 Logging

| Level | Usage |
|-------|-------|
| DEBUG | Development details |
| INFO | Normal operations |
| WARNING | Recoverable issues |
| ERROR | Failures |

### 11.3 Monitoring (Future)

- Error tracking: Sentry
- Performance: Custom metrics
- Uptime: Health check alerts

---

## 12. Technology Stack Summary

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2 | UI Framework |
| TypeScript | 5.3 | Type Safety |
| Vite | 5.4 | Build Tool |
| Tailwind | 3.3 | Styling |
| Zustand | 4.4 | State Management |
| React Router | 6.20 | Routing |
| Axios | 1.6 | HTTP Client |

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | Latest | Web Framework |
| SQLAlchemy | Latest | ORM |
| Pydantic | Latest | Validation |
| PostgreSQL | 15 | Database |
| MinIO | Latest | File Storage |
| Python | 3.11 | Runtime |

### DevOps

| Technology | Purpose |
|------------|---------|
| Docker | Containerization |
| Docker Compose | Local orchestration |
| Git | Version control |

---

## 13. Decision Records Reference

| ADR | Topic | Status |
|-----|-------|--------|
| ADR-0001 | Database: PostgreSQL | Accepted |
| ADR-0002 | Auth: JWT | Accepted |
| ADR-0003 | State: Zustand | Accepted |
| ADR-0004 | File Storage: MinIO | Accepted |

---

## 14. Future Architecture Considerations

### Scalability
- Extract AI services to separate microservices
- Implement message queue for async processing
- CDN for static assets

### AI Integration
- Vector search service (pgvector)
- OCR processing service
- NLP entity extraction service

### Multi-tenancy (Future)
- Row-level security
- Tenant isolation
- Resource quotas

---

*Document Version: 1.0*
*Last Updated: 2026-03-27*
*Next Review: After Phase 1 completion*