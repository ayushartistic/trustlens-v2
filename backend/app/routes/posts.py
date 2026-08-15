from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel

from ..auth import get_current_user
from ..database import get_supabase


router = APIRouter(
    prefix="/api/posts",
    tags=["Posts"]
)
class CreatePostRequest(BaseModel):
    text: str

@router.post("/")
def create_post(
    post: CreatePostRequest,
    current_user=Depends(get_current_user)
):

    supabase = get_supabase()

    if not post.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Post text cannot be empty."
        )

    response = (
        supabase
        .table("posts")
        .insert({
            "user_id": current_user.id,
            "text": post.text.strip()
        })
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=500,
            detail="Failed to create post."
        )

    return response.data[0]

@router.get("/")
def get_posts(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):

    supabase = get_supabase()

    response = (
        supabase
        .table("posts")
        .select(
            """
            *,
            users (
                id,
                username,
                display_name
            ),
            contexts (
                id,
                context_type,
                context_name
            )
            """
        )
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )

    return {
        "count": len(response.data),
        "limit": limit,
        "offset": offset,
        "posts": response.data
    }



@router.get("/{post_id}")
def get_post(post_id: str):

    supabase = get_supabase()

    response = (
        supabase
        .table("posts")
        .select("*")
        .eq("id", post_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Post not found."
        )

    return response.data[0]


@router.get("/{post_id}/comments")
def get_post_comments(post_id: str):

    supabase = get_supabase()

    response = (
    supabase
    .table("comments")
    .select(
        """
        *,
        users (
            id,
            username,
            display_name
        )
        """
    )
    .eq("post_id", post_id)
    .order("created_at", desc=False)
    .execute()
    )

    return {
        "post_id": post_id,
        "count": len(response.data),
        "comments": response.data
    }