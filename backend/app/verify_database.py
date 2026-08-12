from .database import get_supabase


def verify_table(table_name):
    supabase = get_supabase()

    response = (
        supabase
        .table(table_name)
        .select("*")
        .execute()
    )

    return response.data


def main():

    print()
    print("=" * 60)
    print("TrustLens - Database Verification")
    print("=" * 60)
    print()

    supabase = get_supabase()

    # --------------------------------------------------
    # Basic row counts
    # --------------------------------------------------

    tables = [
        "contexts",
        "users",
        "posts",
        "follows",
        "comments",
        "attacks",
        "attack_events",
        "comment_detections",
        "account_detections",
    ]

    print("Table counts:")
    print()

    counts = {}

    for table in tables:

        response = (
            supabase
            .table(table)
            .select("id")
            .execute()
        )

        count = len(response.data)

        counts[table] = count

        print(f"{table:<25} : {count}")

    # --------------------------------------------------
    # Verify posts
    # --------------------------------------------------

    print()
    print("Checking post relationships...")

    posts = (
        supabase
        .table("posts")
        .select("id, user_id, context_id")
        .execute()
        .data
    )

    users = (
        supabase
        .table("users")
        .select("id")
        .execute()
        .data
    )

    contexts = (
        supabase
        .table("contexts")
        .select("id")
        .execute()
        .data
    )

    user_ids = {
        user["id"]
        for user in users
    }

    context_ids = {
        context["id"]
        for context in contexts
    }

    invalid_post_users = [
        post
        for post in posts
        if post["user_id"] not in user_ids
    ]

    invalid_post_contexts = [
        post
        for post in posts
        if (
            post["context_id"] is not None
            and post["context_id"] not in context_ids
        )
    ]

    if not invalid_post_users:
        print("[PASS] All posts reference valid users.")
    else:
        print(
            f"[FAIL] {len(invalid_post_users)} posts "
            "reference invalid users."
        )

    if not invalid_post_contexts:
        print("[PASS] All posts reference valid contexts.")
    else:
        print(
            f"[FAIL] {len(invalid_post_contexts)} posts "
            "reference invalid contexts."
        )

    # --------------------------------------------------
    # Verify comments
    # --------------------------------------------------

    print()
    print("Checking comment relationships...")

    comments = (
        supabase
        .table("comments")
        .select("id, user_id, post_id")
        .execute()
        .data
    )

    post_ids = {
        post["id"]
        for post in posts
    }

    invalid_comment_users = [
        comment
        for comment in comments
        if comment["user_id"] not in user_ids
    ]

    invalid_comment_posts = [
        comment
        for comment in comments
        if comment["post_id"] not in post_ids
    ]

    if not invalid_comment_users:
        print("[PASS] All comments reference valid users.")
    else:
        print(
            f"[FAIL] {len(invalid_comment_users)} comments "
            "reference invalid users."
        )

    if not invalid_comment_posts:
        print("[PASS] All comments reference valid posts.")
    else:
        print(
            f"[FAIL] {len(invalid_comment_posts)} comments "
            "reference invalid posts."
        )

    # --------------------------------------------------
    # Verify follows
    # --------------------------------------------------

    print()
    print("Checking follow relationships...")

    follows = (
        supabase
        .table("follows")
        .select("id, follower_id, followee_id")
        .execute()
        .data
    )

    invalid_follow_users = [
        follow
        for follow in follows
        if (
            follow["follower_id"] not in user_ids
            or follow["followee_id"] not in user_ids
        )
    ]

    self_follows = [
        follow
        for follow in follows
        if follow["follower_id"] == follow["followee_id"]
    ]

    relationship_pairs = [
        (
            follow["follower_id"],
            follow["followee_id"]
        )
        for follow in follows
    ]

    duplicate_relationships = (
        len(relationship_pairs)
        != len(set(relationship_pairs))
    )

    if not invalid_follow_users:
        print("[PASS] All follows reference valid users.")
    else:
        print(
            f"[FAIL] {len(invalid_follow_users)} follows "
            "reference invalid users."
        )

    if not self_follows:
        print("[PASS] No self-follow relationships found.")
    else:
        print(
            f"[FAIL] {len(self_follows)} self-follow "
            "relationships found."
        )

    if not duplicate_relationships:
        print("[PASS] No duplicate follow relationships found.")
    else:
        print("[FAIL] Duplicate follow relationships found.")

    # --------------------------------------------------
    # Verify timestamps
    # --------------------------------------------------

    print()
    print("Checking timestamps...")

    timestamp_checks = [
        ("posts", "created_at"),
        ("comments", "created_at"),
        ("follows", "created_at"),
        ("users", "account_created_at"),
    ]

    timestamp_errors = 0

    for table, column in timestamp_checks:

        response = (
            supabase
            .table(table)
            .select(column)
            .execute()
        )

        for row in response.data:

            if not row.get(column):

                timestamp_errors += 1

    if timestamp_errors == 0:
        print("[PASS] All required timestamps are present.")
    else:
        print(
            f"[FAIL] {timestamp_errors} timestamp values are missing."
        )

    # --------------------------------------------------
    # Final result
    # --------------------------------------------------

    failures = (
        len(invalid_post_users)
        + len(invalid_post_contexts)
        + len(invalid_comment_users)
        + len(invalid_comment_posts)
        + len(invalid_follow_users)
        + len(self_follows)
        + int(duplicate_relationships)
        + timestamp_errors
    )

    print()
    print("=" * 60)
    print("Verification Summary")
    print("=" * 60)

    if failures == 0:

        print()
        print("RESULT: PASS")
        print()
        print(
            "The TrustLens social-media database "
            "passed all integrity checks."
        )

    else:

        print()
        print(f"RESULT: FAIL")
        print(f"Integrity problems found: {failures}")
        print()


if __name__ == "__main__":
    main()