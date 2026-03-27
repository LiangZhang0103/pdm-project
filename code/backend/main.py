from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import sqlalchemy

from config import settings
from database import engine, get_db
import models
import schemas

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="PDM System API",
    description="Product Data Management System API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=schemas.HealthCheck)
async def health_check(db: Session = Depends(get_db)):
    """Check system health including database connectivity."""
    db_healthy = False
    minio_healthy = False

    # Check database connectivity
    try:
        db.execute(sqlalchemy.text("SELECT 1"))
        db_healthy = True
    except Exception:
        db_healthy = False

    # TODO: Check MinIO connectivity

    return schemas.HealthCheck(
        status="healthy" if db_healthy else "unhealthy",
        database=db_healthy,
        minio=minio_healthy,
        timestamp=datetime.utcnow(),
    )


@app.get("/")
async def root():
    return {
        "message": "PDM System API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }


# Import routers
from routers import products

# from routers import documents, bom, auth
# app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(products.router, prefix="/products", tags=["products"])
# app.include_router(documents.router, prefix="/documents", tags=["documents"])
# app.include_router(bom.router, prefix="/bom", tags=["bom"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
