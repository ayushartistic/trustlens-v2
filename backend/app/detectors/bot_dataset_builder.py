from pathlib import Path

import pandas as pd

from .bot_feature_extractor import extract_bot_features


# --------------------------------------------------
# Configuration
# --------------------------------------------------

GROUND_TRUTH_PATH = Path(
    "data/bot_detection/bot_ground_truth.csv"
)

OUTPUT_PATH = Path(
    "data/bot_detection/bot_training_dataset.csv"
)


# --------------------------------------------------
# Build labeled dataset
# --------------------------------------------------

def build_bot_training_dataset():

    print("Loading bot behavior features...")

    # Extract features for ALL users currently
    # present in the social-media database.
    features_df = extract_bot_features()

    print(
        f"Feature records loaded: {len(features_df)}"
    )


    # --------------------------------------------------
    # Load ground truth
    # --------------------------------------------------

    print("Loading bot ground truth...")

    ground_truth_df = pd.read_csv(
        GROUND_TRUTH_PATH
    )

    print(
        f"Ground truth records loaded: "
        f"{len(ground_truth_df)}"
    )


    # --------------------------------------------------
    # Validate ground-truth columns
    # --------------------------------------------------

    required_columns = {
        "username",
        "is_bot",
        "account_type"
    }

    missing_columns = (
        required_columns
        - set(ground_truth_df.columns)
    )

    if missing_columns:

        raise ValueError(
            "Ground truth is missing columns: "
            f"{missing_columns}"
        )


    # --------------------------------------------------
    # Check username uniqueness
    # --------------------------------------------------

    if features_df["username"].duplicated().any():

        raise ValueError(
            "Duplicate usernames found in "
            "feature dataset."
        )


    if ground_truth_df["username"].duplicated().any():

        raise ValueError(
            "Duplicate usernames found in "
            "ground truth dataset."
        )


    # --------------------------------------------------
    # Keep ground-truth columns
    # --------------------------------------------------

    ground_truth_df = ground_truth_df[
        [
            "username",
            "is_bot",
            "account_type"
        ]
    ]


    # --------------------------------------------------
    # Join
    # --------------------------------------------------

    training_df = features_df.merge(
        ground_truth_df,
        on="username",
        how="left"
    )


    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    labeled_users = (
        training_df["is_bot"]
        .notna()
        .sum()
    )

    unlabeled_users = (
        training_df["is_bot"]
        .isna()
        .sum()
    )


    print()
    print("=" * 60)
    print("BOT TRAINING DATASET")
    print("=" * 60)

    print()
    print("Dataset shape:")
    print(training_df.shape)

    print()
    print("Labeled users:")
    print(labeled_users)

    print()
    print("Unlabeled users:")
    print(unlabeled_users)

    print()
    print("Ground-truth distribution:")

    print(
        training_df["is_bot"]
        .value_counts(dropna=False)
    )

    print()
    print("Account-type distribution:")

    print(
        training_df["account_type"]
        .value_counts(dropna=False)
    )


    # --------------------------------------------------
    # Show unmatched synthetic users
    # --------------------------------------------------

    synthetic_ground_truth_usernames = set(
        ground_truth_df["username"]
    )

    feature_usernames = set(
        features_df["username"]
    )

    missing_from_features = (
        synthetic_ground_truth_usernames
        - feature_usernames
    )

    if missing_from_features:

        print()
        print(
            "WARNING:"
        )

        print(
            "Ground-truth users not found "
            "in feature dataset:"
        )

        for username in sorted(
            missing_from_features
        ):

            print(
                f"  - {username}"
            )


    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    training_df.to_csv(
        OUTPUT_PATH,
        index=False
    )


    print()
    print("Training dataset saved to:")

    print(
        OUTPUT_PATH
    )

    return training_df


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    build_bot_training_dataset()