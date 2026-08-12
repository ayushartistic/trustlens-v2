from fastapi import APIRouter, HTTPException, Query

from ..database import get_supabase


router = APIRouter(
    prefix="/api/posts",
    tags=["Posts"]
)


@router.get("/")
def get_posts(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):

    supabase = get_supabase()

    response = (
        supabase
        .table("posts")
        .select("*")
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
        .select("*")
        .eq("post_id", post_id)
        .order("created_at", desc=False)
        .execute()
    )

    return {
        "post_id": post_id,
        "count": len(response.data),
        "comments": response.data
    }