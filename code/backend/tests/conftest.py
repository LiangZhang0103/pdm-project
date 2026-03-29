"""
Pytest配置和共享fixtures

提供测试数据库、客户端和常用测试数据的fixtures。
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app


# 使用内存SQLite数据库进行测试
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_engine():
    """创建测试数据库引擎"""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
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
def client(db_session):
    """创建测试客户端，覆盖数据库依赖"""
    from fastapi.testclient import TestClient

    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # session由fixture管理

    app.dependency_overrides[get_db] = override_get_db

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
