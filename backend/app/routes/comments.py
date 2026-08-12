from fastapi import APIRouter, HTTPException, Query

from ..database import get_supabase


router = APIRouter(
    prefix="/api/comments",
    tags=["Comments"]
)


@router.get("/")
def get_comments(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):

    supabase = get_supabase()

    response = (
        supabase
        .table("comments")
        .select("*")
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )

    return {
        "count": len(response.data),
        "limit": limit,
        "offset": offset,
        "comments": response.data
    }


@router.get("/{comment_id}")
def get_comment(comment_id: str):

    supabase = get_supabase()

    response = (
        supabase
        .table("comments")
        .select("*")
        .eq("id", comment_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Comment not found."
        )

    return response.data[0]