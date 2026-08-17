from pathlib import Path

import pandas as pd

from .bot_feature_extractor import BotFeatureExtractor


GROUND_TRUTH_PATH = Path(
    "data/bot_detection/bot_ground_truth.csv"
)

OUTPUT_PATH = Path(
    "data/bot_detection/bot_training_dataset.csv"
)


def create_training_dataset():

    print("Loading bot detection features...")

    # --------------------------------------------------
    # Extract behavioral features for ALL users
    # --------------------------------------------------

    extractor = BotFeatureExtractor()

    features_df = extractor.extract_features()

    print(
        f"Feature dataset loaded: "
        f"{len(features_df)} users"
    )


    # --------------------------------------------------
    # Load ground truth
    # --------------------------------------------------

    print("Loading bot ground truth...")

    ground_truth_df = pd.read_csv(
        GROUND_TRUTH_PATH
    )

    print(
        f"Ground truth records: "
        f"{len(ground_truth_df)}"
    )


    # --------------------------------------------------
    # Validate required columns
    # --------------------------------------------------

    required_ground_truth_columns = {
        "username",
        "is_bot",
        "account_type"
    }

    missing_columns = (
        required_ground_truth_columns
        - set(ground_truth_df.columns)
    )

    if missing_columns:

        raise ValueError(
            "Ground truth is missing columns: "
            f"{missing_columns}"
        )


    if "username" not in features_df.columns:

        raise ValueError(
            "Feature dataset does not contain "
            "'username'."
        )


    # --------------------------------------------------
    # Make sure usernames are unique
    # --------------------------------------------------

    if ground_truth_df["username"].duplicated().any():

        raise ValueError(
            "Duplicate usernames found in "
            "ground truth."
        )


    # --------------------------------------------------
    # Keep only the columns we need from ground truth
    # --------------------------------------------------

    ground_truth_df = ground_truth_df[
        [
            "username",
            "is_bot",
            "account_type"
        ]
    ]


    # --------------------------------------------------
    # Join features with ground truth
    #
    # LEFT JOIN means:
    # - all 526 feature users remain
    # - 500 synthetic users receive labels
    # - existing users remain unlabeled
    # --------------------------------------------------

    training_df = features_df.merge(
        ground_truth_df,
        on="username",
        how="left"
    )


    # --------------------------------------------------
    # Convert label to nullable integer
    #
    # 0 = human
    # 1 = bot
    # NaN = unknown
    # --------------------------------------------------

    training_df["is_bot"] = (
        training_df["is_bot"]
        .astype("Int64")
    )


    # --------------------------------------------------
    # Save dataset
    # --------------------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    training_df.to_csv(
        OUTPUT_PATH,
        index=False
    )


    # --------------------------------------------------
    # Print validation information
    # --------------------------------------------------

    print()
    print("=" * 50)
    print("BOT TRAINING DATASET")
    print("=" * 50)

    print()
    print("Dataset shape:")
    print(training_df.shape)

    print()
    print("Label distribution:")
    print(
        training_df["is_bot"]
        .value_counts(dropna=False)
    )

    print()
    print("Account type distribution:")
    print(
        training_df["account_type"]
        .value_counts(dropna=False)
    )

    print()
    print("Users with ground truth:")
    print(
        training_df["is_bot"]
        .notna()
        .sum()
    )

    print()
    print("Users without ground truth:")
    print(
        training_df["is_bot"]
        .isna()
        .sum()
    )

    print()
    print("Training dataset saved to:")
    print(OUTPUT_PATH)

    return training_df


if __name__ == "__main__":

    create_training_dataset()