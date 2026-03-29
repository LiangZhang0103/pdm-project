from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict

from config import settings
from database import engine, get_db
import models
import schemas
from routers import products

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
    """
    健康检查端点，检查数据库和MinIO连接状态

    Args:
        db: 数据库会话

    Returns:
        HealthCheck: 系统健康状态
    """
    db_healthy = False
    minio_healthy = False

    # 检查数据库连接
    try:
        db.execute(sqlalchemy.text("SELECT 1"))
        db_healthy = True
    except SQLAlchemyError as e:
        db_healthy = False

    # 检查MinIO连接
    try:
        from minio import Minio

        minio_client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )
        minio_client.list_buckets()  # 简单检查连接
        minio_healthy = True
    except Exception:
        minio_healthy = False

    return schemas.HealthCheck(
        status="healthy" if db_healthy and minio_healthy else "unhealthy",
        database=db_healthy,
        minio=minio_healthy,
        timestamp=datetime.utcnow(),
    )


@app.get("/")
async def root() -> Dict[str, str]:
    """
    API根路径，返回基本信息

    Returns:
        Dict[str, str]: 包含API版本、文档链接、健康检查端点等信息
    """
    return {
        "message": "PDM System API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }


# from routers import documents, bom, auth
# app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(products.router, prefix="/products", tags=["products"])
# app.include_router(documents.router, prefix="/documents", tags=["documents"])
# app.include_router(bom.router, prefix="/bom", tags=["bom"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
