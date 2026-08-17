from fastapi import APIRouter, HTTPException

from ..detectors.bot_predictor import predict_bots


router = APIRouter(
    prefix="/api/detections",
    tags=["Detections"]
)


# --------------------------------------------------
# Bot detection
# --------------------------------------------------

@router.get("/bots")
def detect_bots():

    try:

        results = predict_bots()

        # Convert DataFrame into JSON-compatible records
        records = results.to_dict(
            orient="records"
        )

        bot_count = int(
            (results["is_bot"] == 1).sum()
        )

        human_count = int(
            (results["is_bot"] == 0).sum()
        )

        total_users = len(results)

        return {
            "total_users": total_users,
            "bot_count": bot_count,
            "human_count": human_count,
            "bot_percentage": (
                round(
                    (bot_count / total_users) * 100,
                    2
                )
                if total_users > 0
                else 0
            ),
            "users": records
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Bot detection failed: {str(exc)}"
        )