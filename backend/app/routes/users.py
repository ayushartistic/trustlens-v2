from fastapi import APIRouter, HTTPException

from ..database import get_supabase


router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.get("/")
def get_users():

    supabase = get_supabase()

    response = (
        supabase
        .table("users")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return {
        "count": len(response.data),
        "users": response.data
    }


@router.get("/{user_id}")
def get_user(user_id: str):

    supabase = get_supabase()

    response = (
        supabase
        .table("users")
        .select("*")
        .eq("id", user_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return response.data[0]


@router.get("/{user_id}/followers")
def get_followers(user_id: str):

    supabase = get_supabase()

    response = (
        supabase
        .table("follows")
        .select("follower_id")
        .eq("followee_id", user_id)
        .execute()
    )

    follower_ids = [
        row["follower_id"]
        for row in response.data
    ]

    if not follower_ids:
        return {
            "user_id": user_id,
            "count": 0,
            "followers": []
        }

    users_response = (
        supabase
        .table("users")
        .select("*")
        .in_("id", follower_ids)
        .execute()
    )

    return {
        "user_id": user_id,
        "count": len(users_response.data),
        "followers": users_response.data
    }


@router.get("/{user_id}/following")
def get_following(user_id: str):

    supabase = get_supabase()

    response = (
        supabase
        .table("follows")
        .select("followee_id")
        .eq("follower_id", user_id)
        .execute()
    )

    followee_ids = [
        row["followee_id"]
        for row in response.data
    ]

    if not followee_ids:
        return {
            "user_id": user_id,
            "count": 0,
            "following": []
        }

    users_response = (
        supabase
        .table("users")
        .select("*")
        .in_("id", followee_ids)
        .execute()
    )

    return {
        "user_id": user_id,
        "count": len(users_response.data),
        "following": users_response.data
    }