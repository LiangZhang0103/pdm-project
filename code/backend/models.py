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
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
import uuid
import enum

from database import Base


class ProductStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RELEASED = "released"
    ARCHIVED = "archived"
    OBSOLETE = "obsolete"


class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class Product(Base):
    """
    产品数据模型

    Attributes:
        id: 产品唯一标识符（UUID）
        product_code: 产品编号（唯一）
        name: 产品名称
        description: 产品描述
        category: 产品分类
        version: 产品版本号
        status: 产品状态（draft/released/obsolete）
        created_by: 创建人用户名
        created_at: 创建时间
        updated_at: 更新时间
    """

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
    """
    文档数据模型

    Attributes:
        id: 文档唯一标识符（UUID）
        filename: 文件名
        filepath: 文件存储路径
        file_size: 文件大小（字节）
        mime_type: MIME类型
        product_id: 关联的产品ID（UUID）
        version: 文档版本号
        status: 文档状态（active/archived）
        doc_metadata: 文档元数据（JSON格式）
        uploaded_by: 上传人用户名
        uploaded_at: 上传时间
        ocr_text: OCR识别的文本内容
    """

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


class BOMItem(Base):
    """
    BOM（物料清单）条目数据模型

    Attributes:
        id: BOM条目唯一标识符（UUID）
        parent_product_id: 父产品ID（UUID）
        child_product_id: 子产品ID（UUID）
        quantity: 数量
        unit: 单位
        reference: 参考号
        notes: 备注
        created_at: 创建时间
    """

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
    """
    用户数据模型

    Attributes:
        id: 用户唯一标识符（UUID）
        username: 用户名（唯一）
        email: 邮箱地址（唯一）
        hashed_password: 加密后的密码
        full_name: 全名
        role: 用户角色（user/admin）
        is_active: 是否激活
        created_at: 创建时间
        last_login: 最后登录时间
    """

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
