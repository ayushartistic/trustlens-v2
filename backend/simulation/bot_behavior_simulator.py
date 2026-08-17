
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

from backend.app.database import get_supabase


# ============================================================
# Configuration
# ============================================================

NUM_SYNTHETIC_USERS = 500
NUM_BOT_USERS = 50

HUMAN_USERS = NUM_SYNTHETIC_USERS - NUM_BOT_USERS

HUMAN_POSTS_MIN = 0
HUMAN_POSTS_MAX = 8

BOT_POSTS_MIN = 0
BOT_POSTS_MAX = 2

HUMAN_COMMENTS_MIN = 0
HUMAN_COMMENTS_MAX = 15

BOT_COMMENTS_MIN = 40
BOT_COMMENTS_MAX = 80

HUMAN_FOLLOWS_MIN = 3
HUMAN_FOLLOWS_MAX = 15

BOT_FOLLOWS_MIN = 60
BOT_FOLLOWS_MAX = 120

BATCH_SIZE = 100

SIMULATION_DAYS = 30


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

GROUND_TRUTH_DIR = PROJECT_ROOT / "data" / "bot_detection"

GROUND_TRUTH_FILE = (
    GROUND_TRUTH_DIR / "bot_ground_truth.csv"
)


# ============================================================
# Human-like content
# ============================================================

HUMAN_POST_TEMPLATES = [
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
    "I think this is worth looking into.",
    "There are several perspectives on this.",
    "Curious to hear what others think.",
    "This topic has some interesting implications.",
    "I came across this today and wanted to share it.",
    "There is a lot to discuss here.",
    "This caught my attention today.",
    "Interested in hearing different viewpoints.",
]


HUMAN_COMMENT_TEMPLATES = [
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
    "I hadn't considered it from this perspective.",
    "That is an interesting observation.",
    "Thanks for explaining this.",
    "I think there is another side to this.",
    "This makes sense.",
    "Good point.",
    "I can understand this perspective.",
    "This is something worth thinking about.",
    "I have seen similar discussions before.",
    "Interesting information.",
    "Thanks for bringing this up.",
    "I would like to know more about this.",
    "This is a reasonable argument.",
    "There are some useful points here.",
    "I agree with part of this.",
    "This gives some useful context.",
    "Interesting way of looking at it.",
    "I think this deserves more discussion.",
    "This is helpful information.",
    "That is a good observation.",
    "I see where you are coming from.",
]


# ============================================================
# Bot-like content
# ============================================================

BOT_COMMENT_TEMPLATES = [
    "Check this out!",
    "Amazing opportunity! Check this now!",
    "Don't miss this!",
    "Visit this now!",
    "This is the best deal!",
]


# ============================================================
# Utilities
# ============================================================

def get_supabase_client():
    return get_supabase()


def insert_in_batches(table_name, rows):
    """
    Insert rows into Supabase in manageable batches.
    """

    if not rows:
        return []

    supabase = get_supabase_client()

    inserted = []

    for start in range(
        0,
        len(rows),
        BATCH_SIZE
    ):

        batch = rows[
            start:start + BATCH_SIZE
        ]

        response = (
            supabase
            .table(table_name)
            .insert(batch)
            .execute()
        )

        inserted.extend(response.data)

    return inserted


def random_recent_timestamp():
    """
    Generate a timestamp within the last 30 days.
    """

    now = datetime.now(timezone.utc)

    seconds_back = random.randint(
        0,
        SIMULATION_DAYS * 24 * 60 * 60
    )

    return (
        now -
        timedelta(seconds=seconds_back)
    ).isoformat()


def random_account_created_at(is_bot):
    """
    Bots receive younger account ages.
    Human-like accounts receive older ages.
    """

    if is_bot:

        age_days = random.randint(
            7,
            60
        )

    else:

        age_days = random.randint(
            180,
            1500
        )

    timestamp = (
        datetime.now(timezone.utc)
        - timedelta(days=age_days)
    )

    return timestamp.isoformat()


def get_existing_contexts():
    """
    Load contexts already present in Supabase.
    """

    supabase = get_supabase_client()

    response = (
        supabase
        .table("contexts")
        .select("id")
        .execute()
    )

    if not response.data:

        raise RuntimeError(
            "No contexts found in the database. "
            "Run the normal seed first."
        )

    return [
        row["id"]
        for row in response.data
    ]


# ============================================================
# Synthetic users
# ============================================================

def create_synthetic_users():
    """
    Add 500 synthetic accounts.

    450 are human-like.
    50 are bot-like.

    Existing users are NOT modified.
    """

    print()
    print("=" * 60)
    print("CREATING SYNTHETIC USERS")
    print("=" * 60)

    rows = []

    ground_truth = []

    for index in range(
        1,
        NUM_SYNTHETIC_USERS + 1
    ):

        is_bot = (
            index >
            HUMAN_USERS
        )

        if is_bot:

            username = (
                f"sim_bot_{index - HUMAN_USERS:04d}"
            )

            display_name = (
                f"Simulated Bot "
                f"{index - HUMAN_USERS:04d}"
            )

            bio = (
                "TrustLens synthetic bot account"
            )

        else:

            username = (
                f"sim_user_{index:04d}"
            )

            display_name = (
                f"Simulated User {index:04d}"
            )

            bio = (
                "TrustLens synthetic human-like account"
            )

        rows.append({

            "username": username,

            "display_name": display_name,

            "bio": bio,

            "account_created_at":
                random_account_created_at(
                    is_bot
                ),

        })

        ground_truth.append({

            "username": username,

            "is_bot": int(is_bot),

            "account_type":
                "bot" if is_bot
                else "human"

        })


    inserted_users = insert_in_batches(
        "users",
        rows
    )

    print(
        f"Synthetic users created: "
        f"{len(inserted_users)}"
    )

    return inserted_users, ground_truth


# ============================================================
# Human-like posts
# ============================================================

def create_human_posts(
    users,
    context_ids
):

    rows = []

    for user in users:

        number_of_posts = random.randint(
            HUMAN_POSTS_MIN,
            HUMAN_POSTS_MAX
        )

        for _ in range(
            number_of_posts
        ):

            rows.append({

                "user_id":
                    user["id"],

                "context_id":
                    random.choice(
                        context_ids
                    ),

                "text":
                    random.choice(
                        HUMAN_POST_TEMPLATES
                    ),

                "created_at":
                    random_recent_timestamp()

            })

    return rows


# ============================================================
# Bot-like posts
# ============================================================

def create_bot_posts(
    bot_users,
    context_ids
):

    rows = []

    for bot in bot_users:

        number_of_posts = random.randint(
            BOT_POSTS_MIN,
            BOT_POSTS_MAX
        )

        for _ in range(
            number_of_posts
        ):

            rows.append({

                "user_id":
                    bot["id"],

                "context_id":
                    random.choice(
                        context_ids
                    ),

                "text":
                    random.choice(
                        HUMAN_POST_TEMPLATES
                    ),

                "created_at":
                    random_recent_timestamp()

            })

    return rows


# ============================================================
# Posts
# ============================================================

def create_posts(
    users,
    ground_truth,
    context_ids
):

    print()
    print("=" * 60)
    print("CREATING SYNTHETIC POSTS")
    print("=" * 60)

    bot_usernames = {
        row["username"]
        for row in ground_truth
        if row["is_bot"] == 1
    }

    human_users = [
        user
        for user in users
        if user["username"]
        not in bot_usernames
    ]

    bot_users = [
        user
        for user in users
        if user["username"]
        in bot_usernames
    ]

    rows = []

    rows.extend(
        create_human_posts(
            human_users,
            context_ids
        )
    )

    rows.extend(
        create_bot_posts(
            bot_users,
            context_ids
        )
    )

    inserted_posts = insert_in_batches(
        "posts",
        rows
    )

    print(
        f"Synthetic posts created: "
        f"{len(inserted_posts)}"
    )

    return inserted_posts


# ============================================================
# Human follow behavior
# ============================================================

def create_human_follows(
    human_users,
    all_users
):

    rows = []

    existing_relationships = set()

    all_user_ids = [
        user["id"]
        for user in all_users
    ]

    for user in human_users:

        number_of_follows = random.randint(
            HUMAN_FOLLOWS_MIN,
            HUMAN_FOLLOWS_MAX
        )

        possible_targets = [
            user_id
            for user_id in all_user_ids
            if user_id != user["id"]
        ]

        targets = random.sample(
            possible_targets,
            min(
                number_of_follows,
                len(possible_targets)
            )
        )

        for target_id in targets:

            relationship = (
                user["id"],
                target_id
            )

            if relationship in existing_relationships:
                continue

            existing_relationships.add(
                relationship
            )

            rows.append({

                "follower_id":
                    user["id"],

                "followee_id":
                    target_id,

                "created_at":
                    random_recent_timestamp()

            })

    return rows, existing_relationships


# ============================================================
# Bot follow behavior
# ============================================================

def create_bot_follows(
    bot_users,
    all_users,
    existing_relationships
):

    rows = []

    all_user_ids = [
        user["id"]
        for user in all_users
    ]

    for bot in bot_users:

        number_of_follows = random.randint(
            BOT_FOLLOWS_MIN,
            BOT_FOLLOWS_MAX
        )

        possible_targets = [
            user_id
            for user_id in all_user_ids
            if user_id != bot["id"]
        ]

        targets = random.sample(
            possible_targets,
            min(
                number_of_follows,
                len(possible_targets)
            )
        )

        for target_id in targets:

            relationship = (
                bot["id"],
                target_id
            )

            if relationship in existing_relationships:
                continue

            existing_relationships.add(
                relationship
            )

            rows.append({

                "follower_id":
                    bot["id"],

                "followee_id":
                    target_id,

                "created_at":
                    random_recent_timestamp()

            })

    return rows


# ============================================================
# Follows
# ============================================================

def create_follows(
    users,
    ground_truth
):

    print()
    print("=" * 60)
    print("CREATING SYNTHETIC FOLLOW ACTIVITY")
    print("=" * 60)

    bot_usernames = {
        row["username"]
        for row in ground_truth
        if row["is_bot"] == 1
    }

    human_users = [
        user
        for user in users
        if user["username"]
        not in bot_usernames
    ]

    bot_users = [
        user
        for user in users
        if user["username"]
        in bot_usernames
    ]

    human_rows, relationships = (
        create_human_follows(
            human_users,
            users
        )
    )

    bot_rows = create_bot_follows(
        bot_users,
        users,
        relationships
    )

    rows = (
        human_rows +
        bot_rows
    )

    inserted = insert_in_batches(
        "follows",
        rows
    )

    print(
        f"Synthetic follows created: "
        f"{len(inserted)}"
    )

    return inserted


# ============================================================
# Human comments
# ============================================================

def create_human_comments(
    human_users,
    posts
):

    rows = []

    post_ids = [
        post["id"]
        for post in posts
    ]

    for user in human_users:

        number_of_comments = random.randint(
            HUMAN_COMMENTS_MIN,
            HUMAN_COMMENTS_MAX
        )

        for _ in range(
            number_of_comments
        ):

            rows.append({

                "user_id":
                    user["id"],

                "post_id":
                    random.choice(
                        post_ids
                    ),

                "text":
                    random.choice(
                        HUMAN_COMMENT_TEMPLATES
                    ),

                "created_at":
                    random_recent_timestamp()

            })

    return rows


# ============================================================
# Bot comments
# ============================================================

def create_bot_comments(
    bot_users,
    posts
):

    rows = []

    post_ids = [
        post["id"]
        for post in posts
    ]

    now = datetime.now(
        timezone.utc
    )

    for bot in bot_users:

        number_of_comments = random.randint(
            BOT_COMMENTS_MIN,
            BOT_COMMENTS_MAX
        )

        # Bots concentrate their activity
        # into a short period.
        activity_start = (
            now -
            timedelta(
                days=random.randint(
                    0,
                    SIMULATION_DAYS - 1
                )
            )
        )

        for _ in range(
            number_of_comments
        ):

            # Most bot comments are spread across
            # different posts but within a short
            # time window.
            post_id = random.choice(
                post_ids
            )

            seconds_after_start = random.randint(
                0,
                45 * 60
            )

            timestamp = (
                activity_start +
                timedelta(
                    seconds=seconds_after_start
                )
            )

            rows.append({

                "user_id":
                    bot["id"],

                "post_id":
                    post_id,

                "text":
                    random.choice(
                        BOT_COMMENT_TEMPLATES
                    ),

                "created_at":
                    timestamp.isoformat()

            })

    return rows


# ============================================================
# Comments
# ============================================================

def create_comments(
    users,
    posts,
    ground_truth
):

    print()
    print("=" * 60)
    print("CREATING SYNTHETIC COMMENT ACTIVITY")
    print("=" * 60)

    bot_usernames = {
        row["username"]
        for row in ground_truth
        if row["is_bot"] == 1
    }

    human_users = [
        user
        for user in users
        if user["username"]
        not in bot_usernames
    ]

    bot_users = [
        user
        for user in users
        if user["username"]
        in bot_usernames
    ]

    rows = []

    rows.extend(
        create_human_comments(
            human_users,
            posts
        )
    )

    rows.extend(
        create_bot_comments(
            bot_users,
            posts
        )
    )

    inserted = insert_in_batches(
        "comments",
        rows
    )

    print(
        f"Synthetic comments created: "
        f"{len(inserted)}"
    )

    return inserted


# ============================================================
# Ground truth
# ============================================================

def save_ground_truth(
    ground_truth
):

    GROUND_TRUTH_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    dataframe = pd.DataFrame(
        ground_truth
    )

    dataframe.to_csv(
        GROUND_TRUTH_FILE,
        index=False
    )

    print()
    print(
        f"Ground truth saved to:"
    )

    print(
        GROUND_TRUTH_FILE
    )


# ============================================================
# Main simulation
# ============================================================

def run_simulation():

    print()
    print("=" * 60)
    print("TRUSTLENS BOT BEHAVIOR SIMULATOR")
    print("=" * 60)
    print()

    print(
        "Existing social data will NOT be deleted."
    )

    print()

    # --------------------------------------------------------
    # Contexts
    # --------------------------------------------------------

    context_ids = get_existing_contexts()

    print(
        f"Contexts available: "
        f"{len(context_ids)}"
    )

    # --------------------------------------------------------
    # Users
    # --------------------------------------------------------

    users, ground_truth = (
        create_synthetic_users()
    )

    bot_usernames = {
        row["username"]
        for row in ground_truth
        if row["is_bot"] == 1
    }

    # --------------------------------------------------------
    # Posts
    # --------------------------------------------------------

    posts = create_posts(
        users,
        ground_truth,
        context_ids
    )

    # --------------------------------------------------------
    # Follows
    # --------------------------------------------------------

    follows = create_follows(
        users,
        ground_truth
    )

    # --------------------------------------------------------
    # Comments
    # --------------------------------------------------------

    comments = create_comments(
        users,
        posts,
        ground_truth
    )

    # --------------------------------------------------------
    # Ground truth
    # --------------------------------------------------------

    save_ground_truth(
        ground_truth
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("BOT SIMULATION COMPLETE")
    print("=" * 60)

    print()

    print(
        f"Synthetic users : "
        f"{len(users)}"
    )

    print(
        f"Human-like users: "
        f"{HUMAN_USERS}"
    )

    print(
        f"Bot-like users  : "
        f"{NUM_BOT_USERS}"
    )

    print(
        f"Synthetic posts : "
        f"{len(posts)}"
    )

    print(
        f"Synthetic follows: "
        f"{len(follows)}"
    )

    print(
        f"Synthetic comments: "
        f"{len(comments)}"
    )

    print()

    print(
        "Existing users and existing social "
        "activity were preserved."
    )


if __name__ == "__main__":
    run_simulation()