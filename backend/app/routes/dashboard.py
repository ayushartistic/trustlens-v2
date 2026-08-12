from fastapi import APIRouter
from pydantic import BaseModel

from ..database import get_supabase


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


# ---------------------------------------------
# Response model
# ---------------------------------------------

class DashboardSummary(BaseModel):
    users: int
    posts: int
    comments: int
    follows: int
    contexts: int
    attacks: int
    attack_events: int
    comment_detections: int
    account_detections: int


# ---------------------------------------------
# Helper
# ---------------------------------------------

def count_rows(supabase, table_name: str) -> int:

    response = (
        supabase
        .table(table_name)
        .select("id")
        .execute()
    )

    return len(response.data)


# ---------------------------------------------
# Dashboard summary
# ---------------------------------------------

@router.get(
    "/summary",
    response_model=DashboardSummary
)
def dashboard_summary():

    supabase = get_supabase()

    return DashboardSummary(
        users=count_rows(supabase, "users"),
        posts=count_rows(supabase, "posts"),
        comments=count_rows(supabase, "comments"),
        follows=count_rows(supabase, "follows"),
        contexts=count_rows(supabase, "contexts"),
        attacks=count_rows(supabase, "attacks"),
        attack_events=count_rows(
            supabase,
            "attack_events"
        ),
        comment_detections=count_rows(
            supabase,
            "comment_detections"
        ),
        account_detections=count_rows(
            supabase,
            "account_detections"
        )
    )