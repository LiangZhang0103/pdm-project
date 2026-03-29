"""
Pytest配置和共享fixtures

提供测试数据库、客户端和常用测试数据的fixtures。
"""

import pytest
import sqlite3
from sqlalchemy import create_engine, String, event, TypeDecorator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
import deps


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


class SQLiteUUID(TypeDecorator):
    """UUID类型适配器，将Python UUID对象转换为字符串存储在SQLite中"""

    impl = String(36)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return str(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return str(value)
        return value


@pytest.fixture(scope="function")
def db_engine():
    """创建测试数据库引擎（SQLite替代PostgreSQL）"""
    from sqlalchemy.dialects.postgresql import UUID as PG_UUID

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # SQLite不支持PostgreSQL的UUID类型，替换为兼容适配器
    for table in Base.metadata.tables.values():
        for column in table.columns:
            if isinstance(column.type, PG_UUID):
                column.type = SQLiteUUID()

    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """创建测试数据库会话"""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=db_engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_engine, db_session):
    """创建测试客户端，覆盖数据库和认证依赖"""
    from fastapi.testclient import TestClient
    import models

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    test_user = models.User(
        id="00000000-0000-0000-0000-000000000001",
        username="testuser",
        email="test@example.com",
        hashed_password="fake_hashed_password",
        role="admin",
        is_active=True,
    )

    def override_get_current_active_user():
        return test_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[deps.get_current_active_user] = (
        override_get_current_active_user
    )
    app.dependency_overrides[deps.get_current_user] = override_get_current_active_user
    app.dependency_overrides[deps.get_current_admin_user] = (
        override_get_current_active_user
    )

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_product_data():
    """示例产品数据"""
    return {
        "product_code": "TEST-001",
        "name": "Test Product",
        "description": "A test product for unit testing",
        "category": "Electronics",
        "status": "draft",
    }


@pytest.fixture
def sample_product_data_2():
    """第二个示例产品数据"""
    return {
        "product_code": "TEST-002",
        "name": "Test Product 2",
        "description": "Another test product",
        "category": "Mechanical",
        "status": "active",
    }
