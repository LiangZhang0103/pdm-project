from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

from config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True, echo=settings.debug)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[sessionmaker, None, None]:
    """
    数据库会话生成器（依赖注入）

    Yields:
        Session: SQLAlchemy数据库会话

    使用示例:
        @app.get("/products")
        def get_products(db: Session = Depends(get_db)):
            return db.query(models.Product).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
