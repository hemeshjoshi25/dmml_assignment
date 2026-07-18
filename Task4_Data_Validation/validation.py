"""
Task 4 : Data Validation & Automated EDA Plot Generation (MovieLens Edition)


"""

import sys
from pathlib import Path
import pandas as pd

# Added visualization dependencies
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import RAW_PATH, VALIDATION_PATH, VALIDATION_REPORT_PATH
from utils.logger import get_logger

logger = get_logger("task4_validation.log")


class DataValidation:

    def __init__(self):
        VALIDATION_PATH.mkdir(parents=True, exist_ok=True)
        VALIDATION_REPORT_PATH.mkdir(parents=True, exist_ok=True)

        # Define and establish explicit pathing for EDA reporting assets
        self.eda_report_path = PROJECT_ROOT / "reports" / "eda"
        self.eda_report_path.mkdir(parents=True, exist_ok=True)

    def get_latest_raw_file(self, dataset):
        dataset_dir = RAW_PATH / dataset
        dates = sorted([d.name for d in dataset_dir.iterdir() if d.is_dir()])
        if not dates:
            raise FileNotFoundError(f"No partitioned directories found for {dataset}")
        return dataset_dir / dates[-1] / f"{dataset}.csv"

    def generate_eda_plots(self, dataset, df):
        """Generates domain-specific EDA charts on the fly during the validation phase."""
        sns.set_theme(style="whitegrid")

        if dataset == "customers" and "age" in df.columns:
            logger.info("Generating customer demographic age distribution plot...")
            plt.figure(figsize=(8, 5))

            # Clean missing/corrupted entries for visualization clarity
            clean_age = df["age"].dropna()

            sns.histplot(clean_age, bins=20, kde=True, color="#1A365D", edgecolor="black", alpha=0.7)
            plt.title("Demographic Distribution Profile: Customer Age", fontsize=13, fontweight="bold", pad=12)
            plt.xlabel("Age Cohort", fontsize=11)
            plt.ylabel("Frequency Count", fontsize=11)
            plt.tight_layout()

            chart_path = self.eda_report_path / "customer_age_distribution.png"
            plt.savefig(chart_path, dpi=300)
            plt.close()
            logger.info(f"Saved age distribution graph to: {chart_path}")

        elif dataset == "transactions" and "article_id" in df.columns:
            logger.info("Generating item interaction popularity profile plot...")
            plt.figure(figsize=(8, 5))

            # Compute top interacted items (Long Tail analysis proxy)
            item_counts = df["article_id"].value_counts().head(25)

            sns.barplot(x=item_counts.index.astype(str), y=item_counts.values, hue=item_counts.index.astype(str), palette="Blues_r", legend=False)
            plt.title("Top 25 Highly Popular Items / Video Distributions", fontsize=13, fontweight="bold", pad=12)
            plt.xlabel("Article ID / Movie Identifier", fontsize=11)
            plt.ylabel("Interaction Metric Count", fontsize=11)
            plt.xticks(rotation=45, ha="right", fontsize=9)
            plt.tight_layout()

            chart_path = self.eda_report_path / "item_popularity_distribution.png"
            plt.savefig(chart_path, dpi=300)
            plt.close()
            logger.info(f"Saved item popularity distribution graph to: {chart_path}")

    def validate_dataset(self, dataset):
        file_path = self.get_latest_raw_file(dataset)
        logger.info(f"Validating dataset: {dataset} from {file_path}")
        df = pd.read_csv(file_path)

        report = []
        violations = 0

        # Structural Column Checks
        report.append(f"Dataset Shape: {df.shape}")
        missing_vals = df.isnull().sum().to_dict()
        report.append(f"Missing Values: {missing_vals}")

        # MovieLens Domain Constraints
        if dataset == "transactions":
            if "rating" in df.columns:
                out_of_bounds = ((df["rating"] < 1) | (df["rating"] > 5)).sum()
                report.append(f"  - [Range Check] Ratings out of 1-5 limits: {out_of_bounds} flags.")
                if out_of_bounds > 0:
                    violations += out_of_bounds

        elif dataset == "customers":
            if "age" in df.columns:
                out_of_bounds_age = ((df["age"] < 0) | (df["age"] > 120)).sum()
                report.append(f"  - [Range Check] Ages out of 0-120 limits: {out_of_bounds_age} flags.")
                if out_of_bounds_age > 0:
                    violations += out_of_bounds_age

        # Trigger EDA generation alongside structural verification checks
        self.generate_eda_plots(dataset, df)

        # Save validated data
        df.to_csv(VALIDATION_PATH / f"{dataset}.csv", index=False)
        return report, violations

    def run(self):
        logger.info("=" * 70)
        logger.info("Starting Task 4 : Data Validation & Automated Chart Processing")
        logger.info("=" * 70)

        datasets = ["customers", "articles", "transactions"]
        full_report = []

        for ds in datasets:
            report, violations = self.validate_dataset(ds)
            full_report.append(f"\n--- Validation Report for: {ds} ---")
            full_report.extend(report)
            full_report.append(f"Total Rules Violations: {violations}")

        report_file = VALIDATION_REPORT_PATH / "data_validation_report.txt"
        with open(report_file, "w") as f:
            f.write("\n".join(full_report))

        logger.info(f"Validation reports exported to: {report_file}")
        logger.info("=" * 70)
        logger.info("Task 4 Completed Successfully")
        logger.info("=" * 70)


if __name__ == "__main__":
    DataValidation().run()