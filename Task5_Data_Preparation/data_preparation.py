"""
Task 5 : Data Preparation & Visual EDA (MovieLens Edition)

Project: RecoMart Recommendation System
"""
import os
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

        # Enforce absolute project workspace paths
        self.workspace_root = Path(__file__).resolve().parents[1]
        self.eda_report_path = self.workspace_root / "reports" / "eda"
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

    def build_and_save_interaction_matrix(self, trans_df):
        """Generates the User-Item Interaction Matrix and metadata summary."""
        logger.info("Building User-Item Interaction Matrix...")

        # Compute exact profile metrics
        unique_customers = trans_df['customer_id'].nunique()
        unique_movies = trans_df['article_id'].nunique()

        total_possible_interactions = unique_customers * unique_movies
        actual_interactions = trans_df.groupby(['customer_id', 'article_id']).size().shape[0]
        sparsity = (1 - (actual_interactions / total_possible_interactions)) * 100

        # Log metrics to console and logfile
        logger.info(f"Unique Customers: {unique_customers}")
        logger.info(f"Unique Movies: {unique_movies}")
        logger.info(f"Sparsity: {sparsity:.4f}%")

        # Build the sparse matrix pivot structure
        interaction_matrix = trans_df.groupby(['customer_id', 'article_id'])['rating'].max().unstack(fill_value=0)

        matrix_path = PROCESSED_PATH / "interaction_matrix_movies.txt"

        # Write metadata headers at the top of the file followed by the matrix matrix entries
        with open(matrix_path, "w", encoding="utf-8") as f:
            f.write(f"# Interaction Matrix Profile metadata\n")
            f.write(f"# Unique Customers: {unique_customers}\n")
            f.write(f"# Unique Movies: {unique_movies}\n")
            f.write(f"# Sparsity: {sparsity:.4f}%\n\n")

        interaction_matrix.to_csv(matrix_path, sep='\t', mode='a')
        logger.info(f"✅ Interaction matrix profile successfully saved to: {matrix_path}")

    def generate_eda_plots(self, cust_df, art_df, trans_df):
        """Generates explicit distribution metrics and saves plots for the document engine."""
        logger.info("Generating Visual EDA Artifacts...")
        self.eda_report_path.mkdir(parents=True, exist_ok=True)

        # Chart 1: User Age Distribution
        plt.figure(figsize=(7, 4))
        sns.set_theme(style="whitegrid")
        sns.histplot(cust_df['age'], bins=30, kde=True, color='#2C5282')
        plt.title("MovieLens User Age Distribution", fontsize=12, fontweight='bold', pad=10)
        plt.xlabel("Age", fontsize=10)
        plt.ylabel("Count", fontsize=10)
        plt.tight_layout()

        age_plot_path = self.eda_report_path / "customer_age_distribution.png"
        if age_plot_path.exists():
            try: os.remove(age_plot_path)
            except Exception: pass
        plt.savefig(str(age_plot_path), dpi=150)
        plt.close()

        # Chart 2: Item Popularity Distribution
        plt.figure(figsize=(7, 4))
        movie_counts = trans_df['article_id'].value_counts()
        sns.histplot(movie_counts, bins=30, kde=True, color='#1A365D')
        plt.title("Movie Item Popularity Distribution", fontsize=12, fontweight='bold', pad=10)
        plt.xlabel("Number of Ratings per Movie", fontsize=10)
        plt.ylabel("Count of Movies", fontsize=10)
        plt.tight_layout()

        pop_plot_path = self.eda_report_path / "item_popularity_distribution.png"
        if pop_plot_path.exists():
            try: os.remove(pop_plot_path)
            except Exception: pass
        plt.savefig(str(pop_plot_path), dpi=150)
        plt.close()

        logger.info(f"✅ Both EDA plots successfully saved to: {self.eda_report_path}")

    def run(self):
        logger.info("=" * 70)
        logger.info("Starting Task 5 : Data Preparation & EDA")
        logger.info("=" * 70)

        cust = self.preprocess_customers()
        art = self.preprocess_articles()
        trans = self.preprocess_transactions()

        self.build_and_save_interaction_matrix(trans)
        self.generate_eda_plots(cust, art, trans)

        logger.info("=" * 70)
        logger.info("Task 5 Completed Successfully")
        logger.info("=" * 70)


if __name__ == "__main__":
    DataPreparation().run()