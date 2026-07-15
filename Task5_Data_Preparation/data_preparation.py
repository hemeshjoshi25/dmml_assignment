"""
Task 5 : Data Preparation & Visual EDA (MovieLens Edition)

Author : Hemesh Joshi
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import VALIDATION_PATH, PROCESSED_PATH, REPORT_PATH
from utils.logger import get_logger

logger = get_logger("task5_preparation.log")


class DataPreparation:

    def __init__(self):
        PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
        self.eda_report_path = REPORT_PATH / "eda"
        self.eda_report_path.mkdir(parents=True, exist_ok=True)

    def preprocess_customers(self):
        logger.info("Processing Customers Dataset")
        df = pd.read_csv(VALIDATION_PATH / "customers.csv")

        df.drop_duplicates(inplace=True)
        df["age"] = df["age"].fillna(df["age"].median())
        df["occupation"] = df["occupation"].fillna("other")

        df.to_csv(PROCESSED_PATH / "customers.csv", index=False)
        return df

    def preprocess_articles(self):
        logger.info("Processing Movie Catalog Articles")
        df = pd.read_csv(VALIDATION_PATH / "articles.csv")

        df.drop_duplicates(inplace=True)
        df["movie_title"] = df["movie_title"].fillna("Unknown Movie")

        df.to_csv(PROCESSED_PATH / "articles.csv", index=False)
        return df

    def preprocess_transactions(self):
        logger.info("Processing Transactions Dataset")
        df = pd.read_csv(VALIDATION_PATH / "transactions.csv")

        df.drop_duplicates(inplace=True)
        df["rating"] = df["rating"].fillna(df["rating"].median())

        df.to_csv(PROCESSED_PATH / "transactions.csv", index=False)
        return df

    def generate_eda_plots(self, cust, art, trans):
        logger.info("Generating and saving MovieLens EDA plots.")
        try:
            sns.set_theme(style="whitegrid")

            # Plot 1: User Age Distribution
            plt.figure(figsize=(8, 5))
            sns.histplot(cust['age'], bins=20, kde=True, color='purple')
            plt.title('MovieLens User Age Distribution')
            plt.xlabel('Age')
            plt.ylabel('Count')
            plt.savefig(self.eda_report_path / "customer_age_distribution.png", bbox_inches='tight')
            plt.close()

            # Plot 2: Top 10 Most Popular Movies (Ratings Count)
            plt.figure(figsize=(10, 5))
            top_movies = trans['article_id'].value_counts().head(10).reset_index()
            top_movies.columns = ['article_id', 'interaction_count']
            top_movies = top_movies.merge(art[['article_id', 'movie_title']], on='article_id', how='left')

            sns.barplot(data=top_movies, x='interaction_count', y='movie_title', palette='magma')
            plt.title('Top 10 Most Rated Movies')
            plt.xlabel('Number of Ratings')
            plt.ylabel('Movie Title')
            plt.savefig(self.eda_report_path / "item_popularity_distribution.png", bbox_inches='tight')
            plt.close()

            # 3. Save Matrix Sparsity
            num_users = trans['customer_id'].nunique()
            num_items = trans['article_id'].nunique()
            sparsity = (1 - (len(trans) / (num_users * num_items))) * 100

            with open(self.eda_report_path / "interaction_matrix_metrics.txt", "w") as f:
                f.write(f"Unique Customers: {num_users}\nUnique Movies: {num_items}\nSparsity: {sparsity:.4f}%\n")

        except Exception as e:
            logger.error(f"Visual EDA generation failed: {str(e)}")

    def run(self):
        logger.info("=" * 70)
        logger.info("Starting Task 5 : Data Preparation & EDA")
        logger.info("=" * 70)

        cust = self.preprocess_customers()
        art = self.preprocess_articles()
        trans = self.preprocess_transactions()

        self.generate_eda_plots(cust, art, trans)

        logger.info("=" * 70)
        logger.info("Task 5 Completed Successfully")
        logger.info("=" * 70)


if __name__ == "__main__":
    DataPreparation().run()