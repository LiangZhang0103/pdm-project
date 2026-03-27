from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
import uuid


# Shared properties
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


# Product schemas
class ProductBase(BaseSchema):
    product_code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    status: str = "draft"


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseSchema):
    product_code: Optional[str] = Field(None, min_length=1, max_length=50)
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None


class Product(ProductBase):
    id: uuid.UUID
    version: int
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime


# Document schemas
class DocumentBase(BaseSchema):
    filename: str = Field(..., min_length=1, max_length=255)
    filepath: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    product_id: Optional[uuid.UUID] = None
    status: str = "active"


class DocumentCreate(DocumentBase):
    pass


class Document(DocumentBase):
    id: uuid.UUID
    version: int
    metadata: Optional[dict]
    uploaded_by: Optional[str]
    uploaded_at: datetime
    ocr_text: Optional[str]


# BOM schemas
class BOMItemBase(BaseSchema):
    parent_product_id: uuid.UUID
    child_product_id: uuid.UUID
    quantity: float = 1.0
    unit: Optional[str] = None
    reference: Optional[str] = None
    notes: Optional[str] = None


class BOMItemCreate(BOMItemBase):
    pass


class BOMItem(BOMItemBase):
    id: uuid.UUID
    created_at: datetime


# User schemas
class UserBase(BaseSchema):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "user"


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseSchema):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]


# Authentication schemas
class Token(BaseSchema):
    access_token: str
    token_type: str


class TokenData(BaseSchema):
    username: Optional[str] = None


# Health check
class HealthCheck(BaseSchema):
    status: str
    database: bool
    minio: bool
    timestamp: datetime
