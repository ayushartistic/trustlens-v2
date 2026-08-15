from backend.app.detectors.bot_feature_extractor import (
    extract_bot_features
)


def main():

    dataframe = extract_bot_features()

    print()
    print("==========================================")
    print("BOT DETECTION FEATURE DATASET")
    print("==========================================")

    print()

    print("Dataset shape:")
    print(dataframe.shape)

    print()
    print("Feature columns:")
    print()

    for column in dataframe.columns:
        print(f"- {column}")

    print()
    print("==========================================")
    print("MOST ACTIVE USERS")
    print("==========================================")

    print(
        dataframe[
            [
                "username",
                "posts_count",
                "comments_count",
                "posts_per_day",
                "comments_per_day"
            ]
        ]
        .sort_values(
            "comments_count",
            ascending=False
        )
        .head(10)
        .to_string(index=False)
    )

    print()
    print("==========================================")
    print("HIGHEST FOLLOWING RATIO")
    print("==========================================")

    print(
        dataframe[
            [
                "username",
                "followers_count",
                "following_count",
                "follow_ratio"
            ]
        ]
        .sort_values(
            "follow_ratio",
            ascending=False
        )
        .head(10)
        .to_string(index=False)
    )

    print()
    print("==========================================")
    print("DUPLICATE / CROSS-POST ACTIVITY")
    print("==========================================")

    print(
        dataframe[
            [
                "username",
                "comments_count",
                "duplicate_comment_rate",
                "cross_post_comment_rate",
                "max_comments_in_one_hour"
            ]
        ]
        .sort_values(
            "duplicate_comment_rate",
            ascending=False
        )
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()