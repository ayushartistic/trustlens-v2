from fastapi import APIRouter, HTTPException, Depends

from ..database import get_supabase
from ..auth import get_current_user


router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


# --------------------------------------------------
# Get all users
# --------------------------------------------------

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


# --------------------------------------------------
# Get current authenticated user's profile
# --------------------------------------------------

@router.get("/me")
def get_current_user_profile(
    current_user=Depends(get_current_user)
):

    supabase = get_supabase()

    response = (
        supabase
        .table("users")
        .select("*")
        .eq("auth_user_id", current_user.id)
        .execute()
    )

    if not response.data:

        raise HTTPException(
            status_code=404,
            detail="Social user profile not found."
        )

    return response.data[0]


# --------------------------------------------------
# Get user by social user ID
# --------------------------------------------------

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

# --------------------------------------------------
# Follow a user
# --------------------------------------------------

@router.post("/{user_id}/follow")
def follow_user(
    user_id: str,
    current_user=Depends(get_current_user)
):

    supabase = get_supabase()


    # ----------------------------------------------
    # Find authenticated user's social profile
    # ----------------------------------------------

    current_user_response = (
        supabase
        .table("users")
        .select("id")
        .eq("auth_user_id", current_user.id)
        .execute()
    )

    if not current_user_response.data:

        raise HTTPException(
            status_code=404,
            detail="Social user profile not found."
        )

    follower_id = current_user_response.data[0]["id"]


    # ----------------------------------------------
    # Prevent following yourself
    # ----------------------------------------------

    if follower_id == user_id:

        raise HTTPException(
            status_code=400,
            detail="You cannot follow yourself."
        )


    # ----------------------------------------------
    # Check target user exists
    # ----------------------------------------------

    target_user_response = (
        supabase
        .table("users")
        .select("id")
        .eq("id", user_id)
        .execute()
    )

    if not target_user_response.data:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )


    # ----------------------------------------------
    # Check whether already following
    # ----------------------------------------------

    existing_follow = (
        supabase
        .table("follows")
        .select("id")
        .eq("follower_id", follower_id)
        .eq("followee_id", user_id)
        .execute()
    )

    if existing_follow.data:

        raise HTTPException(
            status_code=409,
            detail="You are already following this user."
        )


    # ----------------------------------------------
    # Create follow relationship
    # ----------------------------------------------

    response = (
        supabase
        .table("follows")
        .insert({
            "follower_id": follower_id,
            "followee_id": user_id
        })
        .execute()
    )

    if not response.data:

        raise HTTPException(
            status_code=500,
            detail="Failed to follow user."
        )


    return {
        "message": "User followed successfully.",
        "follower_id": follower_id,
        "followee_id": user_id
    }


# --------------------------------------------------
# Unfollow a user
# --------------------------------------------------

@router.delete("/{user_id}/follow")
def unfollow_user(
    user_id: str,
    current_user=Depends(get_current_user)
):

    supabase = get_supabase()


    # ----------------------------------------------
    # Find authenticated user's social profile
    # ----------------------------------------------

    current_user_response = (
        supabase
        .table("users")
        .select("id")
        .eq("auth_user_id", current_user.id)
        .execute()
    )

    if not current_user_response.data:

        raise HTTPException(
            status_code=404,
            detail="Social user profile not found."
        )

    follower_id = current_user_response.data[0]["id"]


    # ----------------------------------------------
    # Prevent unfollowing yourself
    # ----------------------------------------------

    if follower_id == user_id:

        raise HTTPException(
            status_code=400,
            detail="You cannot unfollow yourself."
        )


    # ----------------------------------------------
    # Find existing follow relationship
    # ----------------------------------------------

    existing_follow = (
        supabase
        .table("follows")
        .select("id")
        .eq("follower_id", follower_id)
        .eq("followee_id", user_id)
        .execute()
    )

    if not existing_follow.data:

        raise HTTPException(
            status_code=404,
            detail="You are not following this user."
        )


    # ----------------------------------------------
    # Delete follow relationship
    # ----------------------------------------------

    follow_id = existing_follow.data[0]["id"]

    response = (
        supabase
        .table("follows")
        .delete()
        .eq("id", follow_id)
        .execute()
    )


    return {
        "message": "User unfollowed successfully.",
        "follower_id": follower_id,
        "followee_id": user_id
    }


# --------------------------------------------------
# Get followers
# --------------------------------------------------

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


# --------------------------------------------------
# Get following
# --------------------------------------------------

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