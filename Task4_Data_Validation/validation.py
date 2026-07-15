"""
Task 4 : Data Validation (MovieLens Edition)

Author : Hemesh Joshi
"""

import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import RAW_PATH, VALIDATION_PATH, VALIDATION_REPORT_PATH
from utils.logger import get_logger

logger = get_logger("task4_validation.log")


class DataValidation:

    def __init__(self):
        VALIDATION_PATH.mkdir(parents=True, exist_ok=True)
        VALIDATION_REPORT_PATH.mkdir(parents=True, exist_ok=True)

    def get_latest_raw_file(self, dataset):
        dataset_dir = RAW_PATH / dataset
        dates = sorted([d.name for d in dataset_dir.iterdir() if d.is_dir()])
        if not dates:
            raise FileNotFoundError(f"No partitioned directories found for {dataset}")
        return dataset_dir / dates[-1] / f"{dataset}.csv"

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
                # Ratings must be integers/floats between 1 and 5
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

        # Save validated data
        df.to_csv(VALIDATION_PATH / f"{dataset}.csv", index=False)
        return report, violations

    def run(self):
        logger.info("=" * 70)
        logger.info("Starting Task 4 : Data Validation Processing")
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