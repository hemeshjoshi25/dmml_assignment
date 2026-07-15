from pathlib import Path

# =====================================================
# Project Root
# =====================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# =====================================================
# Dataset Paths
# =====================================================
DATASET_PATH = PROJECT_ROOT / "datasets"
SOURCE_PATH = DATASET_PATH / "source"
RAW_PATH = DATASET_PATH / "raw"

EXTRACTED_PATH = DATASET_PATH / "extracted"

PROCESSED_PATH = DATASET_PATH / "processed"

FEATURE_PATH = DATASET_PATH / "features"

VALIDATION_PATH = DATASET_PATH / "validated"

VERSION_PATH = DATASET_PATH / "versions"

REPORT_PATH = PROJECT_ROOT / "reports"

VALIDATION_REPORT_PATH = REPORT_PATH / "validation"

FEATURE_STORE_PATH = DATASET_PATH / "feature_store"

# =====================================================
# Project Directories
# =====================================================
MODEL_PATH = PROJECT_ROOT / "models"

REPORT_PATH = PROJECT_ROOT / "reports"

LOG_PATH = PROJECT_ROOT / "logs"