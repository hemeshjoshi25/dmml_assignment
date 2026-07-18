"""
Run Complete Recommendation Pipeline (Optimized with Prefect Orchestration & Telemetry)

Project : RecoMart Recommendation System
"""

import sys
import time
from pathlib import Path
from prefect import flow, task

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import individual modular sub-tasks
from Task2_Data_Ingestion.ingestion import DataIngestion
from Task3_Raw_Data_Storage.raw_storage import RawDataStorage
from Task4_Data_Validation.validation import DataValidation
from Task5_Data_Preparation.data_preparation import DataPreparation
from Task6_Feature_Engineering.feature_engineering import FeatureEngineering
from Task7_Feature_Store.feature_store import FeatureStore
from Task8_Data_Versioning.versioning import DataVersioning
from Task9_Model_Training.model_training import RecommendationModel
from Task10_Recommendation_Engine.recommendation_engine import RecommendationEngine

from utils.logger import get_logger

logger = get_logger("pipeline_master.log")


# --- Define Prefect Tasks for each step ---

@task(name="Data Ingestion")
def run_data_ingestion():
    DataIngestion().run()


@task(name="Raw Data Storage")
def run_raw_storage():
    RawDataStorage().run()


@task(name="Data Validation")
def run_data_validation():
    DataValidation().run()


@task(name="Data Preparation & EDA", refresh_cache=True)
def run_data_preparation():
    DataPreparation().run()


@task(name="Feature Engineering")
def run_feature_engineering():
    FeatureEngineering().run()


@task(name="Feature Store Sync")
def run_feature_store():
    FeatureStore().run()


@task(name="Data Versioning")
def run_data_versioning():
    DataVersioning().run()


@task(name="Model Training")
def run_model_training():
    RecommendationModel().run()


@task(name="Recommendation Engine")
def run_recommendation_engine():
    RecommendationEngine().run()


@task(name="Automated Report Compilation")
def compile_report():
    base_path = Path(__file__).resolve().parent
    required_images = [
        base_path / "reports" / "validation" / "results_visualization.png",
        base_path / "reports" / "validation" / "evaluation_metrics.png",
        base_path / "reports" / "eda" / "customer_age_distribution.png",
        base_path / "reports" / "eda" / "item_popularity_distribution.png"
    ]

    missing_assets = [img.name for img in required_images if not img.exists()]
    if missing_assets:
        logger.warning(f"Missing visualization plots: {missing_assets}. Report will contain placeholders.")
    else:
        logger.info("All required visual plots verified on disk.")

    from generate_complete_documentation import create_final_report
    create_final_report()
    logger.info("Master Report 'Complete_Project_Documentation.pdf' compiled successfully.")


# --- Define the Master Prefect Flow Orchestrator ---

@flow(name="RecoMart Recommendation Pipeline", description="End-to-End Orchestrated ML Pipeline")
def recomart_pipeline_flow():
    logger.info("=" * 80)
    logger.info("      RECOMART STARTING ORCHESTRATED FLOW LIFECYCLE      ")
    logger.info("=" * 80)

    # Executing the sequential DAG dependency pipeline
    run_data_ingestion()
    run_raw_storage()
    run_data_validation()
    run_data_preparation()
    run_feature_engineering()
    run_feature_store()
    run_data_versioning()
    run_model_training()
    run_recommendation_engine()

    # Final Documentation Build step
    compile_report()

    logger.info("=" * 80)
    logger.info("      RECOMART ORCHESTRATED FLOW COMPLETED SUCCESSFULLY      ")
    logger.info("=" * 80)


if __name__ == "__main__":
    recomart_pipeline_flow()