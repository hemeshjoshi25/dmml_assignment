"""
Task 3 : Raw Data Storage (MovieLens Edition)

"""

import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import SOURCE_PATH, RAW_PATH
from utils.logger import get_logger

logger = get_logger("task3_raw_storage.log")


class RawDataStorage:

    def __init__(self):
        self.date = datetime.now().strftime("%Y-%m-%d")

    def store_dataset(self, file_name):
        # We read from SOURCE_PATH (the landing zone)
        source_file_map = {
            "customers.csv": "u.user",
            "articles.csv": "u.item",
            "transactions.csv": "u.data",
            "products_api.csv": "products_api.csv"
        }

        source_name = source_file_map.get(file_name)
        source_path = SOURCE_PATH / source_name

        dataset_name = file_name.replace(".csv", "")
        partition_dir = RAW_PATH / dataset_name / self.date
        partition_dir.mkdir(parents=True, exist_ok=True)
        destination_path = partition_dir / file_name

        logger.info(f"Converting and partitioning: {source_name} -> {destination_path}")

        # Standardize delimiter logic to produce clean CSV files
        if file_name == "customers.csv":
            df = pd.read_csv(
                source_path, sep="|", header=None,
                names=['customer_id', 'age', 'gender', 'occupation', 'zip_code'],
                encoding="latin-1"
            )
        elif file_name == "articles.csv":
            # MovieLens catalog maps 19 explicit binary genres
            item_cols = ['article_id', 'movie_title', 'release_date', 'video_release_date', 'IMDb_URL'] + [f"genre_{i}" for i in range(19)]
            df = pd.read_csv(
                source_path, sep="|", header=None,
                names=item_cols, encoding="latin-1"
            )
        elif file_name == "transactions.csv":
            df = pd.read_csv(
                source_path, sep="\t", header=None,
                names=['customer_id', 'article_id', 'rating', 'timestamp'],
                encoding="latin-1"
            )
        else:
            df = pd.read_csv(source_path)

        # Write partitioned data as a standard, comma-separated CSV
        df.to_csv(destination_path, index=False)
        logger.info(f"Saved standardized CSV: {file_name}")

    def run(self):
        logger.info("=" * 70)
        logger.info("Starting Task 3 : Raw Data Storage & Delimiter Conversion")
        logger.info("=" * 70)

        files = ["customers.csv", "articles.csv", "transactions.csv", "products_api.csv"]

        for file_name in files:
            source_file_map = {
                "customers.csv": "u.user",
                "articles.csv": "u.item",
                "transactions.csv": "u.data",
                "products_api.csv": "products_api.csv"
            }
            source_path = SOURCE_PATH / source_file_map[file_name]

            if not source_path.exists():
                if file_name == "products_api.csv":
                    logger.warning("Optional products_api.csv not found. Skipping.")
                    continue
                raise FileNotFoundError(f"Required MovieLens source file missing: {source_path}")

            self.store_dataset(file_name)

        logger.info("=" * 70)
        logger.info("Task 3 Completed Successfully")
        logger.info("=" * 70)


if __name__ == "__main__":
    RawDataStorage().run()