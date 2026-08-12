import os

from dotenv import load_dotenv
from supabase import create_client, Client


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")


if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is not set.")

if not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_PUBLISHABLE_KEY is not set.")


# --------------------------------------------------
# Initialize Supabase
# --------------------------------------------------

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# --------------------------------------------------
# Test database connection
# --------------------------------------------------

def test_database_connection():
    response = (
        supabase
        .table("contexts")
        .select("*")
        .limit(5)
        .execute()
    )

    print("Database query executed successfully.")
    print(f"Rows returned: {len(response.data)}")


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("==============================================")
    print("TrustLens Backend")
    print("==============================================")

    print()
    print("Supabase client initialized successfully.")
    print()

    test_database_connection()

    print()
    print("Database connection test completed.")