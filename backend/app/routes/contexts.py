from fastapi import APIRouter

from ..database import get_supabase


router = APIRouter(
    prefix="/api/contexts",
    tags=["Contexts"]
)


@router.get("/")
def get_contexts():

    supabase = get_supabase()

    response = (
        supabase
        .table("contexts")
        .select("*")
        .order("created_at", desc=False)
        .execute()
    )

    return {
        "count": len(response.data),
        "contexts": response.data
    }