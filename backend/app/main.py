# import os

# from dotenv import load_dotenv
# from supabase import create_client, Client


# # --------------------------------------------------
# # Load environment variables
# # --------------------------------------------------

# load_dotenv()


# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")


# if not SUPABASE_URL:
#     raise RuntimeError("SUPABASE_URL is not set.")

# if not SUPABASE_KEY:
#     raise RuntimeError("SUPABASE_PUBLISHABLE_KEY is not set.")


# # --------------------------------------------------
# # Initialize Supabase
# # --------------------------------------------------

# supabase: Client = create_client(
#     SUPABASE_URL,
#     SUPABASE_KEY
# )


# # --------------------------------------------------
# # Test database connection
# # --------------------------------------------------

# def test_database_connection():
#     response = (
#         supabase
#         .table("contexts")
#         .select("*")
#         .limit(5)
#         .execute()
#     )

#     print("Database query executed successfully.")
#     print(f"Rows returned: {len(response.data)}")


# # --------------------------------------------------
# # Main
# # --------------------------------------------------

# if __name__ == "__main__":

#     print("==============================================")
#     print("TrustLens Backend")
#     print("==============================================")

#     print()
#     print("Supabase client initialized successfully.")
#     print()

#     test_database_connection()

#     print()
#     print("Database connection test completed.")


from fastapi import FastAPI

from .database import get_supabase
from .routes.attacks import router as attacks_router

from .routes import (
    users,
    posts,
    comments,
    contexts,
    dashboard
)


app = FastAPI(
    title="TrustLens API",
    description="AI-powered social-media authenticity and security analysis system.",
    version="1.0.0"
)


app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(contexts.router)
app.include_router(dashboard.router)
app.include_router(attacks_router)

@app.get("/")
def root():

    return {
        "name": "TrustLens",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/health")
def health():

    try:

        supabase = get_supabase()

        response = (
            supabase
            .table("users")
            .select("id")
            .limit(1)
            .execute()
        )

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as error:

        return {
            "status": "unhealthy",
            "database": "error",
            "detail": str(error)
        }