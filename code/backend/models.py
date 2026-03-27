from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    Boolean,
    DateTime,
    JSON,
    ForeignKey,
    DECIMAL,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_code = Column(String(50), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    version = Column(Integer, default=1)
    status = Column(String(50), default="draft")
    created_by = Column(String(100))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(500))
    file_size = Column(Integer)
    mime_type = Column(String(100))
    product_id = Column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE")
    )
    version = Column(Integer, default=1)
    status = Column(String(50), default="active")
    doc_metadata = Column(JSON)
    uploaded_by = Column(String(100))
    uploaded_at = Column(DateTime, default=func.now())
    ocr_text = Column(Text)


class BOMItem(Base):
    __tablename__ = "bom_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_product_id = Column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE")
    )
    child_product_id = Column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE")
    )
    quantity = Column(DECIMAL(10, 3), default=1)
    unit = Column(String(50))
    reference = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200))
    role = Column(String(50), default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    last_login = Column(DateTime)
