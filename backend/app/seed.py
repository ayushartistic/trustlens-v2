import argparse
import random
from datetime import datetime, timedelta, timezone

from .database import get_supabase


# ============================================================
# Configuration
# ============================================================

NUM_USERS = 20
NUM_POSTS = 30
NUM_FOLLOWS = 50
NUM_COMMENTS = 50


# ============================================================
# Context data
# ============================================================

CONTEXTS = [
    {
        "context_type": "political",
        "context_name": "Election Discussion",
        "description": (
            "Social media discussion surrounding an "
            "election-related situation."
        ),
    },
    {
        "context_type": "disaster",
        "context_name": "Flood Emergency",
        "description": (
            "Social media activity related to "
            "a simulated flood emergency."
        ),
    },
    {
        "context_type": "social",
        "context_name": "Public Demonstration",
        "description": (
            "Social media discussion surrounding "
            "a simulated public demonstration."
        ),
    },
    {
        "context_type": "religious",
        "context_name": "Religious Festival",
        "description": (
            "Social media activity surrounding "
            "a simulated religious festival."
        ),
    },
    {
        "context_type": "public_safety",
        "context_name": "Emergency Situation",
        "description": (
            "Social media activity concerning "
            "a simulated public safety situation."
        ),
    },
    {
        "context_type": "general",
        "context_name": "Technology Discussion",
        "description": (
            "General social media discussion about technology."
        ),
    },
]


# ============================================================
# Post data
# ============================================================

POST_TEMPLATES = [
    "What do you think about this?",
    "Interesting discussion happening today.",
    "Sharing my thoughts on this topic.",
    "This deserves more attention.",
    "What is everyone's opinion on this?",
    "I found this information interesting.",
    "Here is something worth discussing.",
    "This topic has generated a lot of discussion.",
    "Would like to hear different opinions.",
    "What do you think will happen next?",
    "This is an interesting development.",
    "Sharing some information I came across today.",
]


# ============================================================
# Comment data
# ============================================================

COMMENT_TEMPLATES = [
    "Great post!",
    "Very interesting.",
    "I completely agree.",
    "This is really useful.",
    "Thanks for sharing.",
    "Interesting perspective.",
    "I learned something new from this.",
    "This was helpful.",
    "Nice post.",
    "Good information.",
    "This is worth discussing.",
    "Interesting point.",
    "Well explained.",
    "I agree with this.",
]


# ============================================================
# Utility functions
# ============================================================

def random_timestamp(days_back=30):
    """
    Generate a random UTC timestamp within the previous
    `days_back` days.

    Returns an ISO 8601 string so that it can be safely
    serialized to JSON by the Supabase client.
    """

    now = datetime.now(timezone.utc)

    random_seconds = random.randint(
        0,
        days_back * 24 * 60 * 60
    )

    timestamp = now - timedelta(seconds=random_seconds)

    return timestamp.isoformat()


def insert_in_batches(table_name, rows, batch_size=100):
    """
    Insert records in batches.

    This avoids sending one huge request to Supabase.
    """

    supabase = get_supabase()

    inserted = []

    for start in range(0, len(rows), batch_size):

        batch = rows[start:start + batch_size]

        response = (
            supabase
            .table(table_name)
            .insert(batch)
            .execute()
        )

        inserted.extend(response.data)

    return inserted


# ============================================================
# Check database state
# ============================================================

def database_has_data():
    """
    Check whether the database already contains users.

    We use this to prevent accidentally inserting duplicate
    seed data.
    """

    supabase = get_supabase()

    response = (
        supabase
        .table("users")
        .select("id")
        .limit(1)
        .execute()
    )

    return len(response.data) > 0


# ============================================================
# Clear development database
# ============================================================

def reset_database():
    """
    Delete development data.

    This is intentionally explicit and must only be called
    when --reset is provided.
    """

    supabase = get_supabase()

    print()
    print("WARNING: Resetting TrustLens development database.")
    print()

    # Delete in dependency order.
    tables = [
        "comment_detections",
        "account_detections",
        "attack_events",
        "attacks",
        "comments",
        "follows",
        "posts",
        "users",
        "contexts",
    ]

    for table in tables:

        print(f"Clearing {table}...")

        (
            supabase
            .table(table)
            .delete()
            .neq("id", "00000000-0000-0000-0000-000000000000")
            .execute()
        )

    print()
    print("Database reset completed.")


# ============================================================
# Generate contexts
# ============================================================

def seed_contexts():

    print("Creating contexts...")

    rows = []

    for context in CONTEXTS:

        rows.append({
            "context_type": context["context_type"],
            "context_name": context["context_name"],
            "description": context["description"],
        })

    inserted = insert_in_batches(
        "contexts",
        rows
    )

    print(f"Contexts created: {len(inserted)}")

    return inserted


# ============================================================
# Generate users
# ============================================================

def seed_users():

    print("Creating users...")

    rows = []

    for i in range(NUM_USERS):

        username = f"user_{i + 1:04d}"

        rows.append({
            "username": username,
            "display_name": f"User {i + 1:04d}",
            "bio": f"TrustLens demo user {i + 1:04d}",
            "account_created_at": random_timestamp(1000),
        })

    inserted = insert_in_batches(
        "users",
        rows
    )

    print(f"Users created: {len(inserted)}")

    return inserted


# ============================================================
# Generate posts
# ============================================================

def seed_posts(users, contexts):

    print("Creating posts...")

    rows = []

    for _ in range(NUM_POSTS):

        user = random.choice(users)
        context = random.choice(contexts)

        text = random.choice(POST_TEMPLATES)

        rows.append({
            "user_id": user["id"],
            "context_id": context["id"],
            "text": text,
            "created_at": random_timestamp(30),
        })

    inserted = insert_in_batches(
        "posts",
        rows
    )

    print(f"Posts created: {len(inserted)}")

    return inserted


# ============================================================
# Generate follows
# ============================================================

def seed_follows(users):

    print("Creating follow relationships...")

    rows = []
    relationships = set()

    user_ids = [
        user["id"]
        for user in users
    ]

    while len(rows) < NUM_FOLLOWS:

        follower_id = random.choice(user_ids)
        followee_id = random.choice(user_ids)

        if follower_id == followee_id:
            continue

        relationship = (
            follower_id,
            followee_id
        )

        if relationship in relationships:
            continue

        relationships.add(relationship)

        rows.append({
            "follower_id": follower_id,
            "followee_id": followee_id,
            "created_at": random_timestamp(30),
        })

    inserted = insert_in_batches(
        "follows",
        rows
    )

    print(f"Follow relationships created: {len(inserted)}")

    return inserted


# ============================================================
# Generate comments
# ============================================================

def seed_comments(users, posts):

    print("Creating comments...")

    rows = []

    for _ in range(NUM_COMMENTS):

        user = random.choice(users)
        post = random.choice(posts)

        text = random.choice(COMMENT_TEMPLATES)

        rows.append({
            "user_id": user["id"],
            "post_id": post["id"],
            "text": text,
            "created_at": random_timestamp(30),
        })

    inserted = insert_in_batches(
        "comments",
        rows
    )

    print(f"Comments created: {len(inserted)}")

    return inserted


# ============================================================
# Seed entire database
# ============================================================

def seed_database():

    print()
    print("=" * 60)
    print("TrustLens - Database Seeder")
    print("=" * 60)
    print()

    print("Starting database seed...")
    print()

    # --------------------------------------------------------
    # Contexts
    # --------------------------------------------------------

    contexts = seed_contexts()

    # --------------------------------------------------------
    # Users
    # --------------------------------------------------------

    users = seed_users()

    # --------------------------------------------------------
    # Posts
    # --------------------------------------------------------

    posts = seed_posts(
        users,
        contexts
    )

    # --------------------------------------------------------
    # Follows
    # --------------------------------------------------------

    follows = seed_follows(
        users
    )

    # --------------------------------------------------------
    # Comments
    # --------------------------------------------------------

    comments = seed_comments(
        users,
        posts
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("Database Seed Complete")
    print("=" * 60)

    print()
    print(f"Contexts    : {len(contexts)}")
    print(f"Users       : {len(users)}")
    print(f"Posts       : {len(posts)}")
    print(f"Follows     : {len(follows)}")
    print(f"Comments    : {len(comments)}")
    print()


# ============================================================
# Main
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="Seed the TrustLens development database."
    )

    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear existing development data before seeding."
    )

    args = parser.parse_args()

    # --------------------------------------------------------
    # Reset if explicitly requested
    # --------------------------------------------------------

    if args.reset:
        reset_database()

    # --------------------------------------------------------
    # Prevent accidental duplicate seeding
    # --------------------------------------------------------

    elif database_has_data():

        print()
        print("Database already contains data.")
        print()
        print("Seeding has been cancelled to prevent duplicates.")
        print()
        print("If this is a development database and you want")
        print("to start again, run:")
        print()
        print("python -m backend.app.seed --reset")
        print()

        return

    # --------------------------------------------------------
    # Seed
    # --------------------------------------------------------

    seed_database()


if __name__ == "__main__":
    main()