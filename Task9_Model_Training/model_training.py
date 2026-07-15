"""
Task 9 : Recommendation Model Training (MovieLens SVD with Retrieval Metrics)

Author : Hemesh Joshi
"""

import sys
from pathlib import Path
import json
import pickle
import pandas as pd
from collections import defaultdict

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
        reader = Reader(rating_scale=(1, 5))
        dataset = Dataset.load_from_df(df[["customer_id", "article_id", "rating"]], reader)
        return dataset

    def calculate_precision_recall_at_k(self, predictions, k=10, threshold=3.5):
        """Calculates Precision@K and Recall@K metrics for explicit ratings."""
        # First map predictions to each user
        user_est_true = defaultdict(list)
        for uid, _, true_r, est, _ in predictions:
            user_est_true[uid].append((est, true_r))

        precisions = {}
        recalls = {}
        for uid, user_ratings in user_est_true.items():
            # Sort ratings by estimated value
            user_ratings.sort(key=lambda x: x[0], reverse=True)

            # Number of relevant items (actual rating >= threshold)
            n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)

            # Number of recommended items in top K (predicted rating >= threshold)
            n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])

            # Number of relevant and recommended items in top K
            n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold)) for (est, true_r) in user_ratings[:k])

            # Precision@K: Proportion of recommended items that are relevant
            precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k > 0 else 0

            # Recall@K: Proportion of relevant items that are recommended
            recalls[uid] = n_rel_and_rec_k / n_rel if n_rel > 0 else 0

        # Mean precision and recall across all active test users
        mean_precision = sum(prec_val for prec_val in precisions.values()) / len(precisions)
        mean_recall = sum(rec_val for rec_val in recalls.values()) / len(recalls)

        return mean_precision, mean_recall

    def train_model(self, dataset):
        trainset, testset = train_test_split(dataset, test_size=0.2, random_state=42)

        n_factors, lr_all, reg_all = 100, 0.005, 0.02
        model = SVD(n_factors=n_factors, lr_all=lr_all, reg_all=reg_all, random_state=42)
        model.fit(trainset)

        predictions = model.test(testset)

        # Calculate standard prediction error (RMSE)
        rmse = accuracy.rmse(predictions, verbose=False)

        # Calculate ranking and retrieval metrics
        precision, recall = self.calculate_precision_recall_at_k(predictions, k=10, threshold=3.5)

        logger.info(f"SVD Metrics Summary:")
        logger.info(f" -> Offline Evaluation RMSE : {rmse:.4f}")
        logger.info(f" -> Retrieval Precision@10  : {precision:.4f}")
        logger.info(f" -> Retrieval Recall@10     : {recall:.4f}")

        if mlflow is not None:
            try:
                with mlflow.start_run(run_name="MovieLens_SVD"):
                    mlflow.log_param("algorithm", "SVD")
                    mlflow.log_param("n_factors", n_factors)
                    mlflow.log_metric("RMSE", rmse)
                    mlflow.log_metric("Precision_at_10", precision)
                    mlflow.log_metric("Recall_at_10", recall)
            except Exception as e:
                logger.warning(f"MLflow metrics log bypassed: {e}")

        return model, rmse, precision, recall

    def save_model(self, model):
        with open(MODEL_PATH / "recommendation_model.pkl", "wb") as f:
            pickle.dump(model, f)

    def save_metrics(self, rmse, precision, recall):
        metrics = {
            "Algorithm": "SVD",
            "RMSE": float(rmse),
            "Precision_at_10": float(precision),
            "Recall_at_10": float(recall)
        }
        with open(MODEL_PATH / "model_metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)

    def run(self):
        logger.info("=" * 70)
        logger.info("Starting Task 9 : SVD Model Training & Retrieval Metric Valuation")
        logger.info("=" * 70)

        df = self.load_data()
        dataset = self.prepare_dataset(df)
        model, rmse, precision, recall = self.train_model(dataset)

        self.save_model(model)
        self.save_metrics(rmse, precision, recall)

        logger.info("=" * 70)
        logger.info("Task 9 Completed Successfully")
        logger.info("=" * 70)


if __name__ == "__main__":
    RecommendationModel().run()