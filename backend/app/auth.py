from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .database import get_supabase


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    access_token = credentials.credentials

    supabase = get_supabase()

    try:
        response = supabase.auth.get_user(access_token)

    except Exception as error:
        print("AUTH ERROR:", repr(error))

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