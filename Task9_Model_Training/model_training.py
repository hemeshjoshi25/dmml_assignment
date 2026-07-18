"""
Task 9 : Recommendation Model Training (MovieLens SVD with Retrieval Metrics & Report Charts)

Project: RecoMart Recommendation System
"""

import sys
from pathlib import Path
import json
import pickle
import pandas as pd
from collections import defaultdict

# Added visualization dependencies
import matplotlib.pyplot as plt
import seaborn as sns

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

        # Ensure validation reports path exists
        self.reports_val_path = PROJECT_ROOT / "reports" / "validation"
        self.reports_val_path.mkdir(parents=True, exist_ok=True)

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
        user_est_true = defaultdict(list)
        for uid, _, true_r, est, _ in predictions:
            user_est_true[uid].append((est, true_r))

        precisions = {}
        recalls = {}
        for uid, user_ratings in user_est_true.items():
            user_ratings.sort(key=lambda x: x[0], reverse=True)
            n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)
            n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])
            n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold)) for (est, true_r) in user_ratings[:k])

            precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k > 0 else 0
            recalls[uid] = n_rel_and_rec_k / n_rel if n_rel > 0 else 0

        mean_precision = sum(prec_val for prec_val in precisions.values()) / len(precisions)
        mean_recall = sum(rec_val for rec_val in recalls.values()) / len(recalls)

        return mean_precision, mean_recall

    def train_model(self, dataset):
        trainset, testset = train_test_split(dataset, test_size=0.2, random_state=42)

        n_factors, lr_all, reg_all = 100, 0.005, 0.02
        model = SVD(n_factors=n_factors, lr_all=lr_all, reg_all=reg_all, random_state=42)
        model.fit(trainset)

        predictions = model.test(testset)

        rmse = accuracy.rmse(predictions, verbose=False)
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

        return model, predictions, rmse, precision, recall

    def generate_training_plots(self, predictions):
        """Generates performance and curve metrics to feed the documentation engine."""
        logger.info("Generating evaluation and retrieval curve charts...")

        # 1. Calculate Precision and Recall across sliding scale of K values (1 to 15)
        k_values = list(range(1, 16))
        precisions_list = []
        recalls_list = []

        for k in k_values:
            p, r = self.calculate_precision_recall_at_k(predictions, k=k, threshold=3.5)
            precisions_list.append(p)
            recalls_list.append(r)

        # 2. Plot Retrieval Metrics Curve (Precision @ K vs Recall @ K)
        plt.figure(figsize=(8, 5))
        sns.set_theme(style="whitegrid")
        plt.plot(k_values, precisions_list, marker='o', color='#1A365D', label='Precision @ K', linewidth=2)
        plt.plot(k_values, recalls_list, marker='s', color='#2C5282', label='Recall @ K', linewidth=2)

        plt.title('Retrieval Metrics Optimization Curve (SVD)', fontsize=14, fontweight='bold', pad=12)
        plt.xlabel('Number of Recommended Items (K)', fontsize=11)
        plt.ylabel('Score Range', fontsize=11)
        plt.xticks(k_values)
        plt.legend(frameon=True)
        plt.tight_layout()

        curve_chart_path = self.reports_val_path / "evaluation_metrics.png"
        plt.savefig(curve_chart_path, dpi=300)
        plt.close()
        logger.info(f"Saved retrieval curve to: {curve_chart_path}")

        # 3. Plot Actual vs Predicted Distribution density mapping
        plt.figure(figsize=(8, 5))

        # EXTRACTED: Clean, structured unpacking using explicit named tuple attributes
        actuals = [pred.r_ui for pred in predictions]
        estimates = [pred.est for pred in predictions]

        sns.kdeplot(actuals, fill=True, color="#718096", label="Actual Test Ratings", alpha=0.4)
        sns.kdeplot(estimates, fill=True, color="#1A365D", label="SVD Predicted Estimations", alpha=0.6)

        plt.title('Distribution Deviation: Actual vs. SVD Predicted Scores', fontsize=14, fontweight='bold', pad=12)
        plt.xlabel('Rating Scale', fontsize=11)
        plt.ylabel('Density Distribution', fontsize=11)
        plt.legend()
        plt.tight_layout()

        dist_chart_path = self.reports_val_path / "results_visualization.png"
        plt.savefig(dist_chart_path, dpi=300)
        plt.close()
        logger.info(f"Saved actual vs predicted distribution graph to: {dist_chart_path}")

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
        model, predictions, rmse, precision, recall = self.train_model(dataset)

        # Generate structural output charts for report compilation
        self.generate_training_plots(predictions)

        self.save_model(model)
        self.save_metrics(rmse, precision, recall)

        logger.info("=" * 70)
        logger.info("Task 9 Completed Successfully")
        logger.info("=" * 70)


if __name__ == "__main__":
    RecommendationModel().run()