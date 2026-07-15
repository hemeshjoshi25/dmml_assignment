"""
Run Complete Recommendation Pipeline (Optimized with Telemetry & Error Handling)

Author : Hemesh Joshi
Project : RecoMart Recommendation System
"""

import sys
import time
from pathlib import Path

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


class PipelineRunner:

    def __init__(self):
        # Map tasks to their execution class sequences
        self.tasks = [
            ("Task 2: Data Ingestion", DataIngestion),
            ("Task 3: Raw Data Storage", RawDataStorage),
            ("Task 4: Data Validation & Profiling", DataValidation),
            ("Task 5: Data Preparation & EDA", DataPreparation),
            ("Task 6: Feature Engineering", FeatureEngineering),
            ("Task 7: Feature Store Layer", FeatureStore),
            ("Task 8: Data Versioning (DVC)", DataVersioning),
            ("Task 9: Model Training (MLflow)", RecommendationModel),
            ("Task 10: Inference Recommendation Engine", RecommendationEngine)
        ]

    def run(self):
        logger.info("=" * 80)
        logger.info("      RECOMART STARTING MASTER PIPELINE ORCHESTRATION CYCLE      ")
        logger.info("=" * 80)

        pipeline_start_time = time.time()
        telemetry_log = []

        for task_name, TaskClass in self.tasks:
            logger.info(f"\n[ORCHESTRATOR] ---> Initializing Lifecycle Sequence: {task_name}")
            task_start = time.time()

            try:
                # Instantiates class and executes internal run method loops dynamically
                instance = TaskClass()
                instance.run()

                duration = time.time() - task_start
                telemetry_log.append((task_name, "SUCCESS", f"{duration:.2f}s"))
                logger.info(f"[ORCHESTRATOR] ---> Finished {task_name} cleanly in {duration:.2f}s.\n")

            except Exception as e:
                total_duration = time.time() - pipeline_start_time
                logger.critical("=" * 80)
                logger.critical(f"[PIPELINE BREAK] Orchestration aborted abruptly on [{task_name}]")
                logger.critical(f"Exception Message Root: {str(e)}")
                logger.critical("=" * 80)

                # Print current status summary before termination to allow fast debugging
                print(f"\n--- Execution State Prior to Failure (Total Up-time: {total_duration:.2f}s) ---")
                for completed_task, status, execution_time in telemetry_log:
                    print(f" {completed_task}: {status} ({execution_time})")
                print(f"❌ {task_name}: FAILED\n")

                sys.exit(1) # Bubble up non-zero error to terminal/orchestrators (Airflow/Bash)

        total_pipeline_time = time.time() - pipeline_start_time

        # Output clean structural performance execution tables
        logger.info("=" * 80)
        logger.info("      RECOMART PIPELINE METRICS & PERFORMANCE EXECUTION SUMMARY      ")
        logger.info("=" * 80)
        for completed_task, status, execution_time in telemetry_log:
            logger.info(f" - {completed_task:<45} | Status: {status:<8} | Time: {execution_time}")
        logger.info("-" * 80)
        logger.info(f"Total Pipeline End-to-End Elapsed Processing Execution Time: {total_pipeline_time:.2f}s")
        logger.info("=" * 80)


if __name__ == "__main__":
    runner = PipelineRunner()
    runner.run()