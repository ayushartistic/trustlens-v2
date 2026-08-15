from collections import defaultdict
from datetime import datetime, timezone

import pandas as pd

from ..database import get_supabase


# --------------------------------------------------
# Configuration
# --------------------------------------------------

BATCH_SIZE = 1000


# --------------------------------------------------
# Generic paginated Supabase fetch
# --------------------------------------------------

def fetch_all_rows(table_name: str):

    supabase = get_supabase()

    rows = []
    offset = 0

    while True:

        response = (
            supabase
            .table(table_name)
            .select("*")
            .range(
                offset,
                offset + BATCH_SIZE - 1
            )
            .execute()
        )

        batch = response.data or []

        rows.extend(batch)

        if len(batch) < BATCH_SIZE:
            break

        offset += BATCH_SIZE

    return rows


# --------------------------------------------------
# Timestamp helper
# --------------------------------------------------

def parse_timestamp(value):

    if not value:
        return None

    try:

        timestamp = pd.to_datetime(
            value,
            utc=True
        )

        return timestamp.to_pydatetime()

    except Exception:

        return None


# --------------------------------------------------
# Text normalization
# --------------------------------------------------

def normalize_text(text):

    if not text:
        return ""

    return " ".join(
        str(text)
        .lower()
        .strip()
        .split()
    )


# --------------------------------------------------
# Main feature extraction
# --------------------------------------------------

def extract_bot_features():

    print("Loading social-media data...")

    users = fetch_all_rows("users")
    follows = fetch_all_rows("follows")
    posts = fetch_all_rows("posts")
    comments = fetch_all_rows("comments")

    print(f"Users loaded: {len(users)}")
    print(f"Follows loaded: {len(follows)}")
    print(f"Posts loaded: {len(posts)}")
    print(f"Comments loaded: {len(comments)}")


    # --------------------------------------------------
    # Prepare per-user containers
    # --------------------------------------------------

    follower_counts = defaultdict(int)
    following_counts = defaultdict(int)

    user_posts = defaultdict(list)
    user_comments = defaultdict(list)


    # --------------------------------------------------
    # Follow relationships
    # --------------------------------------------------

    for follow in follows:

        follower_id = follow.get("follower_id")
        followee_id = follow.get("followee_id")

        if follower_id:
            following_counts[follower_id] += 1

        if followee_id:
            follower_counts[followee_id] += 1


    # --------------------------------------------------
    # Posts
    # --------------------------------------------------

    for post in posts:

        user_id = post.get("user_id")

        if user_id:
            user_posts[user_id].append(post)


    # --------------------------------------------------
    # Comments
    # --------------------------------------------------

    for comment in comments:

        user_id = comment.get("user_id")

        if user_id:
            user_comments[user_id].append(comment)


    # --------------------------------------------------
    # Extract features for every user
    # --------------------------------------------------

    feature_rows = []

    now = datetime.now(timezone.utc)


    for user in users:

        user_id = user.get("id")

        # ----------------------------------------------
        # Account age
        # ----------------------------------------------

        account_created_at = parse_timestamp(
            user.get("account_created_at")
        )

        if account_created_at:

            account_age_days = max(
                (now - account_created_at).total_seconds()
                / 86400,
                1
            )

        else:

            account_age_days = 1


        # ----------------------------------------------
        # Network features
        # ----------------------------------------------

        followers = follower_counts[user_id]
        following = following_counts[user_id]

        follow_ratio = (
            following / max(followers, 1)
        )


        # ----------------------------------------------
        # Content activity
        # ----------------------------------------------

        user_post_list = user_posts[user_id]
        user_comment_list = user_comments[user_id]

        posts_count = len(user_post_list)
        comments_count = len(user_comment_list)


        posts_per_day = (
            posts_count / account_age_days
        )

        comments_per_day = (
            comments_count / account_age_days
        )


        comments_per_post = (
            comments_count / max(posts_count, 1)
        )


        # ----------------------------------------------
        # Unique posts commented on
        # ----------------------------------------------

        commented_post_ids = set()

        for comment in user_comment_list:

            post_id = comment.get("post_id")

            if post_id:
                commented_post_ids.add(post_id)

        unique_posts_commented = len(
            commented_post_ids
        )


        # ----------------------------------------------
        # Duplicate comment analysis
        # ----------------------------------------------

        normalized_comments = []

        for comment in user_comment_list:

            text = normalize_text(
                comment.get("text")
            )

            if text:
                normalized_comments.append(text)


        if normalized_comments:

            unique_comment_count = len(
                set(normalized_comments)
            )

            duplicate_comment_rate = (
                1
                - (
                    unique_comment_count
                    / len(normalized_comments)
                )
            )

        else:

            duplicate_comment_rate = 0.0


        # ----------------------------------------------
        # Cross-post repetition
        #
        # Same normalized text appearing on
        # multiple different posts.
        # ----------------------------------------------

        text_to_posts = defaultdict(set)

        for comment in user_comment_list:

            normalized = normalize_text(
                comment.get("text")
            )

            post_id = comment.get("post_id")

            if normalized and post_id:

                text_to_posts[
                    normalized
                ].add(post_id)


        repeated_cross_post_texts = {
            text
            for text, post_ids
            in text_to_posts.items()
            if len(post_ids) > 1
        }


        if normalized_comments:

            cross_post_repeated_comments = sum(
                1
                for comment in user_comment_list
                if normalize_text(
                    comment.get("text")
                ) in repeated_cross_post_texts
            )

            cross_post_comment_rate = (
                cross_post_repeated_comments
                / len(normalized_comments)
            )

        else:

            cross_post_comment_rate = 0.0


        # ----------------------------------------------
        # Maximum comments in one hour
        # ----------------------------------------------

        hourly_comment_counts = defaultdict(int)

        for comment in user_comment_list:

            timestamp = parse_timestamp(
                comment.get("created_at")
            )

            if timestamp:

                hour_bucket = timestamp.replace(
                    minute=0,
                    second=0,
                    microsecond=0
                )

                hourly_comment_counts[
                    hour_bucket
                ] += 1


        if hourly_comment_counts:

            max_comments_in_one_hour = max(
                hourly_comment_counts.values()
            )

        else:

            max_comments_in_one_hour = 0


        # ----------------------------------------------
        # Store feature row
        # ----------------------------------------------

        feature_rows.append({

            "user_id": user_id,

            "username": user.get(
                "username"
            ),

            "display_name": user.get(
                "display_name"
            ),

            "account_age_days":
                round(account_age_days, 2),

            "followers_count":
                followers,

            "following_count":
                following,

            "follow_ratio":
                round(follow_ratio, 4),

            "posts_count":
                posts_count,

            "comments_count":
                comments_count,

            "unique_posts_commented":
                unique_posts_commented,

            "posts_per_day":
                round(posts_per_day, 4),

            "comments_per_day":
                round(comments_per_day, 4),

            "comments_per_post":
                round(comments_per_post, 4),

            "duplicate_comment_rate":
                round(
                    duplicate_comment_rate,
                    4
                ),

            "cross_post_comment_rate":
                round(
                    cross_post_comment_rate,
                    4
                ),

            "max_comments_in_one_hour":
                max_comments_in_one_hour
        })


    # --------------------------------------------------
    # Convert to DataFrame
    # --------------------------------------------------

    dataframe = pd.DataFrame(
        feature_rows
    )


    print(
        f"Bot feature extraction completed "
        f"for {len(dataframe)} users."
    )

    return dataframe