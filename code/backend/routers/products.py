from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database import get_db
import models
import schemas
import deps

router = APIRouter(tags=["products"])


@router.get("/", response_model=List[schemas.Product])
def read_products(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    status: Optional[str] = None,
):
    """Retrieve products with optional filtering."""
    query = db.query(models.Product)

    if category:
        query = query.filter(models.Product.category == category)
    if status:
        query = query.filter(models.Product.status == status)

    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=schemas.Product)
def read_product(
    product_id: UUID,
    db: Session = Depends(get_db),
):
    """
    获取单个产品

    Args:
        product_id: 产品UUID

    Returns:
        Product: 产品对象
    """
    # 将UUID转换为字符串用于数据库查询
    product_id_str = str(product_id)
    product = (
        db.query(models.Product).filter(models.Product.id == product_id_str).first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Create a new product."""
    # Check if product code already exists
    existing = (
        db.query(models.Product)
        .filter(models.Product.product_code == product.product_code)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product code already exists",
        )

    db_product = models.Product(**product.dict(), created_by=current_user.username)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: UUID,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    更新产品

    Args:
        product_id: 产品UUID
        product_update: 产品更新数据
        current_user: 当前认证用户

    Returns:
        Product: 更新后的产品对象
    """
    product_id_str = str(product_id)
    db_product = (
        db.query(models.Product).filter(models.Product.id == product_id_str).first()
    )
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    # Check if new product code conflicts with existing
    if (
        product_update.product_code
        and product_update.product_code != db_product.product_code
    ):
        existing = (
            db.query(models.Product)
            .filter(models.Product.product_code == product_update.product_code)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product code already exists",
            )

    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_admin_user),
):
    """
    删除产品（管理员权限）

    Args:
        product_id: 产品UUID
        db: 数据库会话
        current_user: 当前认证用户（需是管理员）
    """
    product_id_str = str(product_id)
    product = (
        db.query(models.Product).filter(models.Product.id == product_id_str).first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    db.delete(product)
    db.commit()
    return None
