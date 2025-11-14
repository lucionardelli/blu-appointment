from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.schemas import Token
from app.core.config import settings
from app.core.rate_limit import RateLimiter, get_client_id
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    create_access_token,
    create_refresh_token,
)
from app.db.base import get_db
from app.users.logged import authenticate_user, get_current_user, validate_token
from app.users.schemas import User
from app.users.services import get_user_by_username

router = APIRouter()

# Rate limiters: 5 attempts per minute for login, 10 per minute for refresh
login_limiter = RateLimiter(requests=5, window=60)
refresh_limiter = RateLimiter(requests=10, window=60)


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    is_production = settings.ENV == "production"  # In production, use stricter cookie settings, i.e. https only
    samesite_policy = "strict" if is_production else "lax"
    cookie_kwargs = {
        "httponly": True,
        "samesite": samesite_policy,
        "secure": is_production,
        "path": "/",
        "domain": settings.COOKIE_DOMAIN,
    }

    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        **cookie_kwargs,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        **cookie_kwargs,
    )


@router.post("/token")
async def login_for_access_token(
    request: Request,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    login_limiter.check_rate_limit(get_client_id(request))
    user = get_user_by_username(db, form_data.username)
    if not user or not authenticate_user(user, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    _set_auth_cookies(response, access_token, refresh_token)
    return Token(access_token=access_token, token_type="bearer", user=user)  # noqa: S106


@router.post("/refresh")
async def refresh_access_token(
    request: Request,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> Token:
    refresh_limiter.check_rate_limit(get_client_id(request))

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = validate_token(db, refresh_token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    access_token = create_access_token(data={"sub": user.username})
    new_refresh_token = create_refresh_token(data={"sub": user.username})
    _set_auth_cookies(response, access_token, new_refresh_token)
    return Token(access_token=access_token, token_type="bearer", user=user)  # noqa: S106


@router.post("/logout")
async def logout(
    response: Response,
    _user: Annotated[User, Depends(get_current_user)],
) -> dict[str, str]:
    cookie_kwargs = {
        "path": "/",
        "domain": settings.COOKIE_DOMAIN,
    }
    response.delete_cookie("access_token", **cookie_kwargs)
    response.delete_cookie("refresh_token", **cookie_kwargs)
    return {"message": "Logout successful"}
