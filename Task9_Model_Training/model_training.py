"""
Task 9 : Recommendation Model Training (MovieLens SVD)

Author : Hemesh Joshi
"""

import sys
from pathlib import Path
import json
import pickle
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy

try:
    import mlflow
except ImportError:
    mlflow = None

from configs.config import FEATURE_PATH, MODEL_PATH
from utils.logger import get_logger

logger = get_logger("task9_model_training.log")


class RecommendationModel:

    def __init__(self):
        MODEL_PATH.mkdir(parents=True, exist_ok=True)
        if mlflow is not None:
            mlflow.set_tracking_uri(f"file:///{MODEL_PATH / 'mlruns'}")
            mlflow.set_experiment("MovieLens_Recommendation_System")

    def load_data(self):
        return pd.read_csv(FEATURE_PATH / "transaction_features.csv")

    def prepare_dataset(self, df):
        # MovieLens explicit ratings span from 1 to 5
        reader = Reader(rating_scale=(1, 5))
        dataset = Dataset.load_from_df(df[["customer_id", "article_id", "rating"]], reader)
        return dataset

    def train_model(self, dataset):
        trainset, testset = train_test_split(dataset, test_size=0.2, random_state=42)

        n_factors, lr_all, reg_all = 100, 0.005, 0.02
        model = SVD(n_factors=n_factors, lr_all=lr_all, reg_all=reg_all, random_state=42)
        model.fit(trainset)

        predictions = model.test(testset)
        rmse = accuracy.rmse(predictions, verbose=False)
        logger.info(f"SVD Training Complete | Calculated RMSE: {rmse:.4f}")

        if mlflow is not None:
            try:
                with mlflow.start_run(run_name="MovieLens_SVD"):
                    mlflow.log_param("algorithm", "SVD")
                    mlflow.log_param("n_factors", n_factors)
                    mlflow.log_metric("RMSE", rmse)
            except Exception as e:
                logger.warning(f"MLflow log failed: {e}")

        return model, rmse

    def save_model(self, model):
        with open(MODEL_PATH / "recommendation_model.pkl", "wb") as f:
            pickle.dump(model, f)

    def save_metrics(self, rmse):
        metrics = {"Algorithm": "SVD", "RMSE": float(rmse)}
        with open(MODEL_PATH / "model_metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)

    def run(self):
        logger.info("=" * 70)
        logger.info("Starting Task 9 : SVD Model Training")
        logger.info("=" * 70)

        df = self.load_data()
        dataset = self.prepare_dataset(df)
        model, rmse = self.train_model(dataset)

        self.save_model(model)
        self.save_metrics(rmse)

        logger.info("=" * 70)
        logger.info("Task 9 Completed Successfully")
        logger.info("=" * 70)


if __name__ == "__main__":
    RecommendationModel().run()