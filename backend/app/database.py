from supabase import create_client, Client

from .config import SUPABASE_URL, SUPABASE_SECRET_KEY


# --------------------------------------------------
# Supabase backend client
# --------------------------------------------------

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SECRET_KEY
)


def get_supabase() -> Client:
    """
    Return the server-side Supabase client.

    This client uses the secret key and therefore must
    only be used by backend code.
    """

    return supabase