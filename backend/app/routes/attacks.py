from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..database import get_supabase


router = APIRouter(
    prefix="/api/attacks",
    tags=["Attacks"]
)


# ============================================================
# Request Models
# ============================================================

class CommentAttackRequest(BaseModel):
    attacker_user_id: str = Field(
        ...,
        description="UUID of the user performing the attack"
    )

    target_post_id: str = Field(
        ...,
        description="UUID of the post receiving the spam comment"
    )

    comment_text: str = Field(
        ...,
        min_length=1,
        description="Comment text to inject"
    )


# ============================================================
# Response Models
# ============================================================

class CommentAttackResponse(BaseModel):
    success: bool
    message: str

    attack_id: str
    attack_event_id: str
    comment_id: str

    attacker_user_id: str
    target_post_id: str


# ============================================================
# Helper Functions
# ============================================================

def get_user(supabase, user_id: str):
    response = (
        supabase
        .table("users")
        .select("id, username, display_name")
        .eq("id", user_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail=f"User not found: {user_id}"
        )

    return response.data[0]


def get_post(supabase, post_id: str):
    response = (
        supabase
        .table("posts")
        .select("id, user_id, text")
        .eq("id", post_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail=f"Post not found: {post_id}"
        )

    return response.data[0]


# ============================================================
# Comment Spam Attack
# ============================================================

@router.post(
    "/comment",
    response_model=CommentAttackResponse
)
def execute_comment_attack(
    request: CommentAttackRequest
):

    supabase = get_supabase()

    # --------------------------------------------------------
    # 1. Validate attacker
    # --------------------------------------------------------

    attacker = get_user(
        supabase,
        request.attacker_user_id
    )

    # --------------------------------------------------------
    # 2. Validate target post
    # --------------------------------------------------------

    post = get_post(
        supabase,
        request.target_post_id
    )

    # --------------------------------------------------------
    # 3. Create attack record
    # --------------------------------------------------------

    attack_data = {
        "attack_type": "comment_spam",
        "target_user_id": post["user_id"],
        "target_post_id": request.target_post_id,
        "parameters": {
            "attacker_user_id": request.attacker_user_id,
            "comment_text": request.comment_text
        },
        "status": "completed"
    }

    attack_response = (
        supabase
        .table("attacks")
        .insert(attack_data)
        .execute()
    )

    if not attack_response.data:
        raise HTTPException(
            status_code=500,
            detail="Failed to create attack record."
        )

    attack = attack_response.data[0]

    # --------------------------------------------------------
    # 4. Create actual comment
    # --------------------------------------------------------

    comment_data = {
        "user_id": request.attacker_user_id,
        "post_id": request.target_post_id,
        "text": request.comment_text
    }

    comment_response = (
        supabase
        .table("comments")
        .insert(comment_data)
        .execute()
    )

    if not comment_response.data:

        # The attack record exists but the actual activity
        # failed. Mark the attack accordingly.

        (
            supabase
            .table("attacks")
            .update({
                "status": "failed"
            })
            .eq("id", attack["id"])
            .execute()
        )

        raise HTTPException(
            status_code=500,
            detail="Attack record created, but comment injection failed."
        )

    comment = comment_response.data[0]

    # --------------------------------------------------------
    # 5. Create attack event
    # --------------------------------------------------------

    event_data = {
        "attack_id": attack["id"],
        "target_user_id": post["user_id"],
        "target_post_id": request.target_post_id,
        "event_type": "comment_injected",
        "metadata": {
            "attacker_user_id": request.attacker_user_id,
            "comment_id": comment["id"],
            "comment_text": request.comment_text
        }
    }

    event_response = (
        supabase
        .table("attack_events")
        .insert(event_data)
        .execute()
    )

    if not event_response.data:

        # The comment has already been created.
        # We therefore mark the attack as partially failed
        # rather than pretending everything succeeded.

        (
            supabase
            .table("attacks")
            .update({
                "status": "partial_failure"
            })
            .eq("id", attack["id"])
            .execute()
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Comment was injected, but the attack event "
                "could not be recorded."
            )
        )

    event = event_response.data[0]

    # --------------------------------------------------------
    # 6. Return result
    # --------------------------------------------------------

    return CommentAttackResponse(
        success=True,
        message="Comment spam attack executed successfully.",

        attack_id=attack["id"],
        attack_event_id=event["id"],
        comment_id=comment["id"],

        attacker_user_id=attacker["id"],
        target_post_id=post["id"]
    )