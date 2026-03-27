from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

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
    product_id: str,
    db: Session = Depends(get_db),
):
    """Get a specific product by ID."""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
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
    product_id: str,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Update an existing product."""
    db_product = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
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
    product_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_admin_user),
):
    """Delete a product (admin only)."""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    db.delete(product)
    db.commit()
    return None
