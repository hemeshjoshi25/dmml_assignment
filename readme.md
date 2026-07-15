# RecoMart End-to-End Data Management Pipeline

An industry-aligned, production-ready Data Management and Machine Learning pipeline designed for **RecoMart**, an e-commerce platform. This project ingests tracking assets from both static H&M datasets and dynamic REST APIs, processes data through storage layers, tracks transformations via an architectural Feature Store, versions code/data with DVC, and manages models via MLflow experiment logs.

---

## 🛠️ System Architecture & Folder Layout

```text
recomart_pipeline/
│
├── configs/
│   └── config.py               # Centralized workspace folder path setups
│
├── utils/
│   └── logger.py               # Global formatted logger configuration engine
│
├── Task2_Data_Ingestion/
│   └── ingestion.py            # Extracts CSVs and queries Fake Store REST API
│
├── Task3_Raw_Data_Storage/
│   └── raw_storage.py          # Partitions raw tracks into chronological data lakes
│
├── Task4_Data_Validation/
│   └── validation.py           # Validates data profiles & automated range filters
│
├── Task5_Data_Preparation/
│   └── data_preparation.py     # Performs imputation & generates visual EDA reports
│
├── Task6_Feature_Engineering/
│   └── feature_engineering.py   # Extracts user engagement and temporal features
│
├── Task7_Feature_Store/
│   └── feature_store.py        # Central feature registry with batch lookup capabilities
│
├── Task8_Data_Versioning/
│   └── versioning.py           # Creates data snapshots integrated with DVC
│
├── Task9_Model_Training/
│   └── model_training.py       # Optimizes SVD matrices logged with MLflow tracking
│
├── Task10_Recommendation_Engine/
│   └── recommendation_engine.py# Computes personalized Top-N inference targets
│
├── pipeline_runner.py          # Master Orchestrator with telemetry timings
├── requirements.txt            # Project platform code dependencies
└── README.md                   # Documentation guide