from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel

from ..auth import get_current_user
from ..database import get_supabase


router = APIRouter(
    prefix="/api/comments",
    tags=["Comments"]
)


class CreateCommentRequest(BaseModel):
    post_id: str
    text: str


@router.post("/")
def create_comment(
    comment: CreateCommentRequest,
    current_user=Depends(get_current_user)
):

    supabase = get_supabase()

    # ---------------------------------------------
    # Validate comment text
    # ---------------------------------------------

    if not comment.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Comment text cannot be empty."
        )

    # ---------------------------------------------
    # Verify that the post exists
    # ---------------------------------------------

    post_response = (
        supabase
        .table("posts")
        .select("id")
        .eq("id", comment.post_id)
        .execute()
    )

    if not post_response.data:
        raise HTTPException(
            status_code=404,
            detail="Post not found."
        )

    # ---------------------------------------------
    # Create comment
    # ---------------------------------------------

    response = (
        supabase
        .table("comments")
        .insert({
            "post_id": comment.post_id,
            "user_id": current_user.id,
            "text": comment.text.strip()
        })
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=500,
            detail="Failed to create comment."
        )

    return response.data[0]


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