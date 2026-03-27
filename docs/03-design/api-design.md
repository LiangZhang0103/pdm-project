# API Design Document

## Overview

This document defines the RESTful API design for the Product Data Management (PDM) System. The API provides endpoints for product management, document management, BOM (Bill of Materials) management, user authentication, and AI-enhanced features.

---

## Design Summary (Meta)

```yaml
design_type: "new_feature"
risk_level: "low"
complexity_level: "medium"
complexity_rationale: "Standard CRUD APIs with authentication; complexity from multi-table relationships and file handling"
main_constraints:
  - JWT authentication required for write operations
  - File storage via MinIO S3-compatible API
  - Database with UUID primary keys
biggest_risks:
  - File upload size limits and timeout handling
  - Complex nested queries for BOM tree
unknowns:
  - AI feature API design may evolve during Phase 2
  - Search performance with large datasets
```

---

## Background and Context

### Prerequisite ADRs

- No existing ADRs - this is the initial system design

### Agreement Checklist

#### Scope
- [x] Product CRUD endpoints
- [x] User authentication endpoints
- [x] Document management endpoints
- [x] BOM management endpoints
- [x] Health check endpoint
- [x] Future AI feature endpoints (placeholder)

#### Non-Scope
- [x] Real-time WebSocket endpoints
- [x] Batch processing APIs
- [x] Admin dashboard APIs

#### Constraints
- [x] Parallel operation: Yes (stateless API)
- [x] Backward compatibility: Required for minor version updates
- [x] Performance measurement: Required via response headers

---

## Base URL and Versioning

```
Base URL: http://localhost:8000
API Version: v1 (prefix: /api/v1)
Documentation: /docs (Swagger UI), /redoc (ReDoc)
```

---

## Authentication

### JWT Authentication

All endpoints except health check and authentication require a valid JWT token.

**Header**: `Authorization: Bearer <token>`

**Token Claims**:
```json
{
  "sub": "username",
  "exp": 1234567890,
  "role": "user|admin"
}
```

### Endpoints Not Requiring Authentication
- `GET /health` - System health check
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

---

## API Endpoints

### 1. Health Check

#### GET /health

Check system health including database and MinIO connectivity.

**Response**:
```json
{
  "status": "healthy",
  "database": true,
  "minio": false,
  "timestamp": "2026-03-27T10:00:00Z"
}
```

---

### 2. Authentication

#### POST /auth/register

Register a new user.

**Request Body**:
```json
{
  "username": "string (3-100 chars)",
  "email": "user@example.com",
  "password": "string (min 6 chars)",
  "full_name": "string (optional)"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "full_name": "string",
  "role": "user",
  "is_active": true,
  "created_at": "datetime"
}
```

#### POST /auth/login

Login and receive JWT token.

**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

### 3. Products

#### GET /products

Retrieve products with pagination and filtering.

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| skip | int | 0 | Number of records to skip |
| limit | int | 100 | Max records to return (1-1000) |
| category | string | - | Filter by category |
| status | string | - | Filter by status |

**Response** (200):
```json
[
  {
    "id": "uuid",
    "product_code": "PRD-001",
    "name": "Product Name",
    "description": "Description",
    "category": "Electronics",
    "status": "draft",
    "version": 1,
    "created_by": "username",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

#### GET /products/{product_id}

Get a specific product by ID.

**Response** (200): Product object

#### POST /products

Create a new product (requires authentication).

**Request Body**:
```json
{
  "product_code": "string (unique)",
  "name": "string",
  "description": "string (optional)",
  "category": "string (optional)",
  "status": "draft"
}
```

**Response** (201): Created product object

#### PUT /products/{product_id}

Update an existing product (requires authentication).

**Request Body** (all fields optional):
```json
{
  "product_code": "string",
  "name": "string",
  "description": "string",
  "category": "string",
  "status": "released"
}
```

**Response** (200): Updated product object

#### DELETE /products/{product_id}

Delete a product (admin only).

**Response** (204): No content

---

### 4. Documents

#### GET /products/{product_id}/documents

List documents for a specific product.

**Response** (200):
```json
[
  {
    "id": "uuid",
    "filename": "spec.pdf",
    "filepath": "path/in/minio",
    "file_size": 1024000,
    "mime_type": "application/pdf",
    "product_id": "uuid",
    "version": 1,
    "status": "active",
    "uploaded_by": "username",
    "uploaded_at": "datetime",
    "ocr_text": "extracted text (if available)"
  }
]
```

#### POST /documents

Upload a document (requires authentication).

**Request**: multipart/form-data
- file: binary
- product_id: uuid (optional)
- metadata: JSON (optional)

**Response** (201):
```json
{
  "id": "uuid",
  "filename": "spec.pdf",
  "filepath": "minio-path",
  "file_size": 1024000,
  "mime_type": "application/pdf",
  "product_id": "uuid",
  "version": 1,
  "status": "active"
}
```

#### GET /documents/{document_id}/download

Download a document.

**Response** (200): File stream

#### POST /documents/{document_id}/ocr

Trigger OCR extraction (Phase 2).

**Response** (202):
```json
{
  "task_id": "uuid",
  "status": "processing"
}
```

---

### 5. BOM (Bill of Materials)

#### GET /products/{product_id}/bom

Get BOM tree for a product.

**Response** (200):
```json
{
  "product_id": "uuid",
  "items": [
    {
      "id": "uuid",
      "child_product": { "id": "uuid", "product_code": "...", "name": "..." },
      "quantity": 2,
      "unit": "pcs",
      "reference": "REF-001",
      "notes": "optional notes",
      "children": []
    }
  ]
}
```

#### POST /bom

Create BOM item (requires authentication).

**Request Body**:
```json
{
  "parent_product_id": "uuid",
  "child_product_id": "uuid",
  "quantity": 1.0,
  "unit": "pcs",
  "reference": "string (optional)",
  "notes": "string (optional)"
}
```

**Response** (201): Created BOM item

#### PUT /bom/{bom_id}

Update BOM item.

**Response** (200): Updated BOM item

#### DELETE /bom/{bom_id}

Delete BOM item.

**Response** (204): No content

---

### 6. Search (Phase 2)

#### POST /search

Semantic search endpoint.

**Request Body**:
```json
{
  "query": "natural language search query",
  "type": "products|documents|all",
  "limit": 10
}
```

**Response** (200):
```json
{
  "results": [
    {
      "type": "product",
      "id": "uuid",
      "score": 0.95,
      "data": { ... }
    }
  ]
}
```

---

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Invalid/missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error |

---

## Data Contracts

### Product Object

```yaml
Input:
  Type: ProductCreate (Pydantic model)
  Preconditions:
    - product_code: unique, 1-50 chars
    - name: required, 1-200 chars
  Validation: Pydantic field validation

Output:
  Type: Product (Pydantic model)
  Guarantees:
    - id: always returned as UUID
    - version: auto-incremented on update
    - created_at/updated_at: auto-generated
  On Error: HTTPException with detail message

Invariants:
  - product_code cannot be duplicated
  - delete requires admin role
```

### Authentication Token

```yaml
Input:
  Type: LoginRequest
  Preconditions: username and password required

Output:
  Type: Token
  Guarantees:
    - access_token: JWT string
    - token_type: "bearer"
  On Error: 401 for invalid credentials

Invariants:
  - Token expires in 1 hour
  - Password hashed with bcrypt
```

---

## State Transitions

### Product Status

```
draft → released → obsolete
  ↑______________↓
  
Allowed transitions:
- draft → released (when ready)
- released → obsolete (when deprecated)
- Any → (deletion by admin only)
```

---

## Performance Considerations

### Pagination
- Default limit: 100
- Maximum limit: 1000
- Use cursor-based pagination for large datasets

### Caching
- Implement Redis caching for frequently accessed products
- Cache invalidation on updates

### Rate Limiting
- 100 requests/minute for authenticated users
- 20 requests/minute for unauthenticated endpoints

---

## Versioning Strategy

- URL-based versioning: `/api/v1/`
- Minor version bumps for backward-compatible changes
- Major version bumps for breaking changes
- Deprecation warnings in response headers

---

## Reference

- Backend implementation: `/code/backend/`
- API schemas: `/code/backend/schemas.py`
- Database models: `/code/backend/models.py`

---

*Document created: 2026-03-27*
*Status: Draft*
*Version: 1.0*