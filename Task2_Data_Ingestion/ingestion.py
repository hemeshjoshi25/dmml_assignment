"""
Task 2 : Data Ingestion (MovieLens Edition)

Author : Hemesh Joshi
"""

import sys
from pathlib import Path
import shutil
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import SOURCE_PATH, EXTRACTED_PATH
from utils.logger import get_logger

logger = get_logger("task2_ingestion.log")


class DataIngestion:

    def __init__(self):
        SOURCE_PATH.mkdir(parents=True, exist_ok=True)
        EXTRACTED_PATH.mkdir(parents=True, exist_ok=True)

    def fetch_api_data(self):
        """Fetches dynamic external catalog product tracks to fulfill multi-source criteria."""
        logger.info("Connecting to dynamic REST API catalog channel...")
        url = "https://fakestoreapi.com/products"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Keep API CSV naming standard across versions
                import pandas as pd
                df = pd.DataFrame(response.json())
                output_file = SOURCE_PATH / "products_api.csv"
                df.to_csv(output_file, index=False)
                logger.info("Successfully fetched REST API data.")
            else:
                logger.warning(f"REST API connection emitted status code: {response.status_code}")
        except Exception as e:
            logger.warning(f"Bypassed dynamic API segment ingestion: {str(e)}")

    def copy_to_extracted(self):
        """Copies the active raw MovieLens files into the landing zone stage."""
        logger.info("Transitioning raw MovieLens data to landing zone staging layer.")

        # Map target files to copy over from datasets/source/
        movielens_files = ["u.user", "u.item", "u.data"]

        for file_name in movielens_files:
            source_file = SOURCE_PATH / file_name
            if not source_file.exists():
                raise FileNotFoundError(
                    f"Required file [{file_name}] is missing in datasets/source/. "
                    f"Please place raw MovieLens files there before running!"
                )

            # Map them into the destination landing zone
            shutil.copy2(source_file, EXTRACTED_PATH / file_name)
            logger.info(f"Staged asset: {file_name}")

        # Also stage our fetched API CSV if present
        api_file = SOURCE_PATH / "products_api.csv"
        if api_file.exists():
            shutil.copy2(api_file, EXTRACTED_PATH / "products_api.csv")

    def run(self):
        logger.info("=" * 70)
        logger.info("Starting Task 2 : Data Ingestion Phase")
        logger.info("=" * 70)

        self.fetch_api_data()
        self.copy_to_extracted()

        logger.info("=" * 70)
        logger.info("Task 2 Completed Successfully")
        logger.info("=" * 70)


if __name__ == "__main__":
    DataIngestion().run()