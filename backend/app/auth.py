from fastapi import Header, HTTPException

from .database import get_supabase


def get_current_user(
    authorization: str | None = Header(default=None)
):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header is required."
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header."
        )

    access_token = authorization.split(" ", 1)[1]

    supabase = get_supabase()

    try:
        response = supabase.auth.get_user(access_token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token."
        )

    if not response.user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token."
        )

    return response.user