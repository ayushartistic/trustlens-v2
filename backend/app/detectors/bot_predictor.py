import joblib
import pandas as pd
from pathlib import Path

from .bot_feature_extractor import extract_bot_features


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    PROJECT_ROOT
    / "data"
    / "bot_detection"
    / "bot_random_forest.joblib"
)


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

def load_model():

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"Bot detection model not found: {MODEL_PATH}"
        )

    print("Loading trained bot detection model...")

    model = joblib.load(MODEL_PATH)

    print("Bot detection model loaded successfully.")

    return model


# --------------------------------------------------
# Predict bots
# --------------------------------------------------

def predict_bots():

    print("\n" + "=" * 60)
    print("BOT DETECTION INFERENCE")
    print("=" * 60)

    # ----------------------------------------------
    # Load trained model
    # ----------------------------------------------

    model = load_model()


    # ----------------------------------------------
    # Extract current behavioral features
    # ----------------------------------------------

    print("\nExtracting current user behavior...")

    feature_df = extract_bot_features()

    print(
        f"Feature records available: "
        f"{len(feature_df)}"
    )


    # ----------------------------------------------
    # Model feature columns
    # ----------------------------------------------

    excluded_columns = [
        "user_id",
        "username",
        "display_name",
        "is_bot",
        "account_type"
    ]

    feature_columns = [
        column
        for column in feature_df.columns
        if column not in excluded_columns
    ]


    X = feature_df[feature_columns]


    # ----------------------------------------------
    # Predictions
    # ----------------------------------------------

    predictions = model.predict(X)

    probabilities = model.predict_proba(X)


    # ----------------------------------------------
    # Build result dataframe
    # ----------------------------------------------

    results = feature_df[
        [
            "user_id",
            "username",
            "display_name"
        ]
    ].copy()


    results["is_bot"] = predictions


    results["human_probability"] = (
        probabilities[:, 0]
    )


    results["bot_probability"] = (
        probabilities[:, 1]
    )


    # ----------------------------------------------
    # Account classification
    # ----------------------------------------------

    results["prediction"] = results["is_bot"].map({

        0: "Human",
        1: "Bot"

    })


    # ----------------------------------------------
    # Sort suspicious users first
    # ----------------------------------------------

    results = (
        results
        .sort_values(
            "bot_probability",
            ascending=False
        )
        .reset_index(drop=True)
    )


    # ----------------------------------------------
    # Display summary
    # ----------------------------------------------

    bot_count = (
        results["is_bot"] == 1
    ).sum()

    human_count = (
        results["is_bot"] == 0
    ).sum()


    print("\n" + "=" * 60)
    print("BOT DETECTION RESULTS")
    print("=" * 60)

    print(
        f"\nTotal users analyzed : {len(results)}"
    )

    print(
        f"Predicted humans     : {human_count}"
    )

    print(
        f"Predicted bots       : {bot_count}"
    )


    print("\nTop suspicious accounts:")

    print(
        results[
            [
                "username",
                "prediction",
                "bot_probability"
            ]
        ]
        .head(20)
        .to_string(index=False)
    )


    return results


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    results = predict_bots()

    print("\nInference completed successfully.")


if __name__ == "__main__":
    main()