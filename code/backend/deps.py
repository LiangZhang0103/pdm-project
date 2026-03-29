from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from config import settings
from database import get_db
import models
import schemas


# OAuth2 scheme for token extraction
oauth2_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    """
    获取当前认证用户

    Args:
        db: 数据库会话
        token: JWT token字符串

    Returns:
        User: 当前认证用户对象

    Raises:
        HTTPException: 401 - 当token无效或用户不存在时
    """


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    获取当前活跃用户

    Args:
        current_user: 当前用户对象

    Returns:
        User: 当前活跃用户对象

    Raises:
        HTTPException: 400 - 当用户未激活时
    """


def get_current_admin_user(
    current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    """
    获取当前管理员用户

    Args:
        current_user: 当前用户对象

    Returns:
        User: 管理员用户对象

    Raises:
        HTTPException: 403 - 当用户不是管理员时
    """
