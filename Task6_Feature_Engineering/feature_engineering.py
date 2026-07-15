"""
Task 6 : Feature Engineering (MovieLens Edition)

Author : Hemesh Joshi
"""

import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import PROCESSED_PATH, FEATURE_PATH
from utils.logger import get_logger

logger = get_logger("task6_feature_engineering.log")


class FeatureEngineering:

    def __init__(self):
        FEATURE_PATH.mkdir(parents=True, exist_ok=True)

    def create_customer_features(self):
        logger.info("Creating Customer Features")
        df = pd.read_csv(PROCESSED_PATH / "customers.csv")

        # Age group cohort bins
        df["age_group"] = pd.cut(df["age"], bins=[0, 25, 45, 100], labels=["Young", "Adult", "Senior"])
        df["is_student"] = (df["occupation"] == "student").astype(int)

        # Track total ratings provided by the user
        trans_df = pd.read_csv(PROCESSED_PATH / "transactions.csv")
        user_counts = trans_df["customer_id"].value_counts().reset_index()
        user_counts.columns = ["customer_id", "user_total_transactions"]
        df = df.merge(user_counts, on="customer_id", how="left").fillna(0)

        features = df[["customer_id", "age_group", "is_student", "user_total_transactions"]]
        features.to_csv(FEATURE_PATH / "customer_features.csv", index=False)

    def create_article_features(self):
        logger.info("Creating Movie Catalog Features")
        df = pd.read_csv(PROCESSED_PATH / "articles.csv")

        # Preserve the movie identity labels and movie genre flags
        genre_cols = [f"genre_{i}" for i in range(19)]
        features = df[["article_id", "movie_title"] + genre_cols]
        features.to_csv(FEATURE_PATH / "article_features.csv", index=False)

    def create_transaction_features(self):
        logger.info("Creating Transaction Features")
        df = pd.read_csv(PROCESSED_PATH / "transactions.csv")

        # Pull datetime features from timestamp
        df["t_dat"] = pd.to_datetime(df["timestamp"], unit="s")
        df["purchase_year"] = df["t_dat"].dt.year
        df["purchase_month"] = df["t_dat"].dt.month

        features = df[["customer_id", "article_id", "rating", "purchase_year", "purchase_month"]]
        features.to_csv(FEATURE_PATH / "transaction_features.csv", index=False)

    def run(self):
        logger.info("=" * 70)
        logger.info("Starting Task 6 : Feature Engineering")
        logger.info("=" * 70)

        self.create_customer_features()
        self.create_article_features()
        self.create_transaction_features()

        logger.info("=" * 70)
        logger.info("Task 6 Completed Successfully")
        logger.info("=" * 70)


if __name__ == "__main__":
    FeatureEngineering().run()