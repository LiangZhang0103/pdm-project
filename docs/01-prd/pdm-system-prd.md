# PRD: Product Data Management (PDM) System

## Overview

### One-line Summary
An AI-enhanced Product Data Management system built with FastAPI + React + PostgreSQL, enabling product lifecycle management with integrated OCR, NLP, and semantic search capabilities.

### Background
The project is a 3-month learning initiative to build a comprehensive PDM system as a portfolio project. The primary goal is to learn full-stack development (FastAPI, React, TypeScript, PostgreSQL) and AI integration (OCR, NLP, vector search). The system addresses the need for centralized product data management with intelligent document processing and semantic search capabilities.

---

## Project Context

### Current Status
- **Start Date**: March 27, 2026
- **Expected Completion**: June 27, 2026
- **Current Phase**: Week 1 complete - Basic system infrastructure and product CRUD
- **Team Size**: 1 person
- **Time Investment**: 10-15 hours/week (1-2 hours weekday, 4-6 hours weekend)

### Technology Stack
- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS + Zustand
- **Backend**: FastAPI + SQLAlchemy + Pydantic
- **Database**: PostgreSQL 15 + pgvector (for vector storage)
- **File Storage**: MinIO (S3-compatible)
- **AI Components**: PaddleOCR, spaCy, sentence-transformers

---

## User Stories

### Primary Users
1. **Product Managers**: Create and manage product data, track product lifecycle
2. **Engineers**: Access product specifications, manage BOM (Bill of Materials)
3. **Administrators**: System configuration, user management

### User Stories
```
As a Product Manager,
I want to create, read, update, and delete product records
So that I can manage product information throughout its lifecycle

As an Engineer,
I want to upload and manage product documents
So that I can store and retrieve technical specifications

As a Product Manager,
I want to create and manage Bill of Materials (BOM)
So that I can track component relationships and dependencies

As an Engineer,
I want to search products using natural language
So that I can quickly find relevant products without exact keywords

As a System Administrator,
I want to manage user authentication and authorization
So that I can control access to sensitive product data
```

### Use Cases
1. **Product CRUD**: Create, read, update, delete products with version control
2. **Document Management**: Upload, version, preview technical documents
3. **BOM Management**: Create hierarchical product structures with quantities
4. **AI Document Processing**: Automatic OCR extraction from images/PDFs
5. **Semantic Search**: Natural language product and document search
6. **User Authentication**: Secure login with role-based access control

---

## Functional Requirements

### Must Have (MVP)

#### 1. Product Data Management
- [ ] Requirement 1: Create new product with unique product code
  - AC: POST /products creates product, returns 201 with product data
- [ ] Requirement 2: List products with pagination and filtering
  - AC: GET /products returns paginated list, supports category/status filters
- [ ] Requirement 3: Get single product by ID
  - AC: GET /products/{id} returns product or 404
- [ ] Requirement 4: Update product information
  - AC: PUT /products/{id} updates product, prevents duplicate codes
- [ ] Requirement 5: Delete product (admin only)
  - AC: DELETE /products/{id} removes product, returns 204

#### 2. User Authentication
- [ ] Requirement 1: User registration
  - AC: POST /auth/register creates user with hashed password
- [ ] Requirement 2: User login with JWT
  - AC: POST /auth/login returns access token
- [ ] Requirement 3: Role-based access control
  - AC: Admin can delete products, regular users cannot

#### 3. Document Management
- [ ] Requirement 1: Upload document to product
  - AC: POST /documents uploads file to MinIO, creates DB record
- [ ] Requirement 2: List documents for product
  - AC: GET /products/{id}/documents returns document list
- [ ] Requirement 3: Download document
  - AC: GET /documents/{id}/download returns file stream
- [ ] Requirement 4: Document version control
  - AC: Uploading same filename creates new version

#### 4. BOM Management
- [ ] Requirement 1: Create BOM item (parent-child relationship)
  - AC: POST /bom creates relationship with quantity
- [ ] Requirement 2: Get BOM tree for product
  - AC: GET /products/{id}/bom returns hierarchical tree
- [ ] Requirement 3: Update BOM item quantity
  - AC: PUT /bom/{id} updates quantity/unit

### AI Features (Phase 2)

#### 5. Document Intelligent Processing
- [ ] Requirement 1: OCR text extraction
  - AC: POST /documents/{id}/ocr extracts text from images/PDFs
- [ ] Requirement 2: Entity recognition
  - AC: NLP extracts part numbers, materials, dimensions from text

#### 6. Semantic Search
- [ ] Requirement 1: Vector-based search
  - AC: POST /search converts query to vector, returns similar products
- [ ] Requirement 2: Hybrid search (keyword + semantic)
  - AC: Search combines keyword match with vector similarity

#### 7. BOM Analysis
- [ ] Requirement 1: Cost estimation
  - AC: Calculate estimated cost from historical data
- [ ] Requirement 2: Supply chain risk assessment
  - AC: Identify single-source components

---

## Non-Functional Requirements

### Performance
- **Response Time**: API responses < 500ms (95th percentile)
- **Throughput**: Support 100 concurrent users
- **File Upload**: Support files up to 100MB

### Reliability
- **Availability**: 99.5% uptime (excluding planned maintenance)
- **Error Rate**: < 0.1% API error rate

### Security
- JWT authentication with 1-hour token expiry
- Password hashing with bcrypt
- CORS configured for frontend origin only

### Scalability
- Horizontal scaling ready (stateless backend)
- Database connection pooling
- CDN-ready static asset serving

---

## Success Criteria

### Quantitative Metrics
1. **System Uptime**: > 99.5% during development phase
2. **Code Quality**: ESLint/Black formatting, type checking passes
3. **Test Coverage**: Core business logic > 70% coverage
4. **Response Time**: API endpoints < 500ms

### Qualitative Metrics
1. **User Experience**: Clean, intuitive UI with responsive design
2. **Developer Experience**: Clear API documentation (/docs)
3. **Maintainability**: Modular code structure, comprehensive comments

---

## Technical Considerations

### Dependencies
- PostgreSQL 15+ with pgvector extension
- MinIO for file storage
- Docker for containerization

### Constraints
- Single developer (time constraint)
- Learning-focused (quality over quantity)
- Budget-conscious (free tier services)

### Assumptions
- Development environment can run all services locally
- Frontend and backend can be developed simultaneously
- AI features can be added in Phase 2 without breaking Phase 1

### Risks and Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| AI model accuracy | High | Medium | Use proven APIs first, then local models |
| Time management | High | High | Weekly review, flexible roadmap |
| Technical complexity | Medium | Medium | Start simple, refactor after |
| Deployment complexity | Medium | Low | Use managed services (Vercel, Railway) |

---

## Out of Scope
- Mobile applications (web-only for MVP)
- Real-time collaboration features
- Advanced analytics dashboard
- Multi-tenant architecture

---

## Undetermined Items

- [ ] **Authentication Provider**: Consider OAuth2 (Google, GitHub login) vs. simple JWT
- [ ] **AI Deployment Strategy**: Cloud AI APIs vs. local model inference tradeoff
- [ ] **Search UI**: Full-text search vs. filtered list interface decision

---

## Appendix

### References
- 3-month roadmap: `/plan/3-month-roadmap.md`
- Tech stack details: `/resources/tech-stack.md`
- Backend code: `/code/backend/`
- Frontend code: `/code/frontend/`

### Glossary
- **BOM**: Bill of Materials - hierarchical structure of product components
- **OCR**: Optical Character Recognition - text extraction from images
- **NLP**: Natural Language Processing - text understanding and entity extraction
- **pgvector**: PostgreSQL extension for vector storage and similarity search

---

*Document created: 2026-03-27*
*Status: Draft - Pending Review*