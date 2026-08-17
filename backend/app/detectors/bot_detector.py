import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "bot_detection"
    / "bot_training_dataset.csv"
)


# --------------------------------------------------
# Load training data
# --------------------------------------------------

def load_training_data():

    print("Loading bot training dataset...")

    df = pd.read_csv(DATASET_PATH)

    print(
        f"Dataset loaded: "
        f"{len(df)} users"
    )

    return df


# --------------------------------------------------
# Prepare dataset
# --------------------------------------------------

def prepare_dataset(df):

    # Only labeled users can be used
    # for supervised training.
    labeled_df = df[
        df["is_bot"].notna()
    ].copy()

    print(
        f"Labeled users available: "
        f"{len(labeled_df)}"
    )

    # These are identifiers / descriptive
    # fields and should not be model features.
    excluded_columns = [
        "user_id",
        "username",
        "display_name",
        "is_bot",
        "account_type"
    ]

    feature_columns = [
        column
        for column in labeled_df.columns
        if column not in excluded_columns
    ]

    X = labeled_df[feature_columns]

    y = labeled_df["is_bot"].astype(int)

    return X, y, feature_columns


# --------------------------------------------------
# Train model
# --------------------------------------------------

def train_model(X, y):

    print("\nSplitting dataset...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print(
        f"Training samples: {len(X_train)}"
    )

    print(
        f"Testing samples: {len(X_test)}"
    )


    print("\nTraining Random Forest model...")

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )

    model.fit(
        X_train,
        y_train
    )

    return model, X_test, y_test


# --------------------------------------------------
# Evaluate model
# --------------------------------------------------

def evaluate_model(
    model,
    X_test,
    y_test
):

    predictions = model.predict(X_test)


    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    matrix = confusion_matrix(
        y_test,
        predictions
    )


    print("\n")
    print("=" * 60)
    print("BOT DETECTOR EVALUATION")
    print("=" * 60)

    print(
        f"\nAccuracy  : {accuracy:.4f}"
    )

    print(
        f"Precision : {precision:.4f}"
    )

    print(
        f"Recall    : {recall:.4f}"
    )

    print(
        f"F1 Score  : {f1:.4f}"
    )


    print("\nConfusion Matrix:")

    print(matrix)


    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions,
            target_names=[
                "Human",
                "Bot"
            ],
            zero_division=0
        )
    )


# --------------------------------------------------
# Feature importance
# --------------------------------------------------

def show_feature_importance(
    model,
    feature_columns
):

    importance_df = pd.DataFrame({

        "feature": feature_columns,

        "importance":
            model.feature_importances_

    })

    importance_df = (
        importance_df
        .sort_values(
            "importance",
            ascending=False
        )
    )


    print("\n")
    print("=" * 60)
    print("BOT DETECTION FEATURE IMPORTANCE")
    print("=" * 60)

    print(
        importance_df.to_string(
            index=False
        )
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    df = load_training_data()

    X, y, feature_columns = (
        prepare_dataset(df)
    )

    model, X_test, y_test = (
        train_model(
            X,
            y
        )
    )

    evaluate_model(
        model,
        X_test,
        y_test
    )

    show_feature_importance(
        model,
        feature_columns
    )
    MODEL_PATH = "data/bot_detection/bot_random_forest.joblib"

    joblib.dump(model, MODEL_PATH)

    print(f"\nModel saved to:")
    print(MODEL_PATH)


if __name__ == "__main__":
    main()