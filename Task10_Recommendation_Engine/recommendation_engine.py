"""
Task 10 : Recommendation Engine Inference (MovieLens Edition)

Author : Hemesh Joshi
"""

import sys
from pathlib import Path
import pickle
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import MODEL_PATH, FEATURE_PATH, REPORT_PATH
from utils.logger import get_logger

logger = get_logger("task10_recommendation_engine.log")


class RecommendationEngine:

    def __init__(self):
        REPORT_PATH.mkdir(parents=True, exist_ok=True)

    def load_model(self):
        with open(MODEL_PATH / "recommendation_model.pkl", "rb") as f:
            return pickle.load(f)

    def load_data(self):
        transactions = pd.read_csv(FEATURE_PATH / "transaction_features.csv")
        articles = pd.read_csv(FEATURE_PATH / "article_features.csv")
        return transactions, articles

    def generate_recommendations(self, top_n=50):
        model = self.load_model()
        transactions, articles = self.load_data()

        # Generate recommendations for a subset of active users to maintain short execution runtimes
        unique_customers = transactions["customer_id"].unique()[:50]
        unique_articles = articles.to_dict(orient="records")

        logger.info(f"Generating Top-{top_n} movie recommendations for sample users.")
        recommendations = []

        for customer_id in unique_customers:
            scored_candidates = []
            for art in unique_articles:
                art_id = art["article_id"]
                prediction = model.predict(str(customer_id), str(art_id))
                scored_candidates.append({
                    "customer_id": customer_id,
                    "item_id": art_id,
                    "item_display_name": art.get("movie_title", "Unknown Movie"),
                    "predicted_rating": round(prediction.est, 4)
                })

            scored_candidates.sort(key=lambda x: x["predicted_rating"], reverse=True)
            recommendations.extend(scored_candidates[:top_n])

        return pd.DataFrame(recommendations)

    def save(self, df):
        output_file = REPORT_PATH / "recommendations.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"Recommendations exported to: {output_file}")

    def run(self):
        logger.info("=" * 70)
        logger.info("Starting Task 10 : Collaborative Filtering Inference Engine")
        logger.info("=" * 70)

        try:
            recommendations = self.generate_recommendations(top_n=10)
            self.save(recommendations)
        except Exception as e:
            logger.error(f"Inference run failed: {str(e)}")
            raise

        logger.info("=" * 70)
        logger.info("Task 10 Completed Successfully")
        logger.info("=" * 70)


if __name__ == "__main__":
    RecommendationEngine().run()