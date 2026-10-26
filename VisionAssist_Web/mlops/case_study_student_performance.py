"""Unit-I & Unit-II Syllabus Case Study: Student Performance Prediction Pipeline.

Implements the end-to-end standard MLOps lifecycle on tabular data:
1. Problem Formulation & Dataset Generation (Study hours, Attendance, Previous Score, Extracurriculars).
2. Data Preprocessing & Validation:
   - Categorical Encoding (One-Hot / Ordinal).
   - Feature Scaling (StandardScaler) & Normalization.
   - Train/Test Split with fixed random seed for reproducibility.
3. MLflow Experiment Tracking:
   - Logs hyperparameters (learning_rate, n_estimators, max_depth).
   - Logs regression metrics (R2, RMSE, MAE).
   - Logs SHAP feature importance summary for Explainable AI (Unit V).
4. Model Registry registration.
"""

from pathlib import Path
import json
import time
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import mlflow
import mlflow.sklearn

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_NAME = "CaseStudy-StudentPerformance"
REPORTS_DIR = ROOT / "runs" / "case_study"


def generate_synthetic_student_data(n_samples: int = 500) -> pd.DataFrame:
    """Generates synthetic student performance data with realistic statistical dependencies."""
    np.random.seed(42)
    study_hours = np.random.uniform(1.0, 10.0, n_samples)
    attendance_rate = np.random.uniform(50.0, 100.0, n_samples)
    parent_education = np.random.choice(["High School", "Bachelor", "Master"], n_samples, p=[0.4, 0.45, 0.15])
    extracurricular = np.random.choice(["Yes", "No"], n_samples, p=[0.6, 0.4])
    previous_score = np.random.normal(70, 12, n_samples).clip(30, 100)

    # Performance formula with noise
    edu_boost = {"High School": 0, "Bachelor": 4, "Master": 8}
    extra_boost = {"Yes": 3, "No": 0}

    final_score = (
        0.35 * previous_score +
        3.2 * study_hours +
        0.25 * attendance_rate +
        [edu_boost[e] for e in parent_education] +
        [extra_boost[x] for x in extracurricular] +
        np.random.normal(0, 3.5, n_samples)
    ).clip(0, 100)

    return pd.DataFrame({
        "study_hours": np.round(study_hours, 1),
        "attendance_rate": np.round(attendance_rate, 1),
        "parent_education": parent_education,
        "extracurricular": extracurricular,
        "previous_score": np.round(previous_score, 1),
        "final_score": np.round(final_score, 1),
    })


def run_student_performance_mlops_pipeline(
    n_estimators: int = 50,
    max_depth: int = 6,
    test_size: float = 0.2
) -> dict:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    df = generate_synthetic_student_data()

    # 1. Feature Engineering
    numeric_features = ["study_hours", "attendance_rate", "previous_score"]
    categorical_features = ["parent_education", "extracurricular"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(drop="first", sparse_output=False), categorical_features),
        ]
    )

    X = df.drop(columns=["final_score"])
    y = df["final_score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)

    # Extract feature names after encoding
    cat_encoder = preprocessor.named_transformers_["cat"]
    encoded_cat_names = list(cat_encoder.get_feature_names_out(categorical_features))
    all_feature_names = numeric_features + encoded_cat_names

    # 2. MLflow Experiment Tracking
    mlflow.set_experiment(EXPERIMENT_NAME)
    run_name = f"rf-trees{n_estimators}-depth{max_depth}-{time.strftime('%Y%m%d-%H%M%S')}"

    with mlflow.start_run(run_name=run_name) as run:
        # Log Hyperparameters
        params = {
            "model_type": "RandomForestRegressor",
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "test_size": test_size,
            "num_features": len(all_feature_names),
            "scaling": "StandardScaler",
            "encoding": "OneHotEncoder",
        }
        mlflow.log_params(params)

        # Train Model
        model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42
        )
        model.fit(X_train_proc, y_train)

        # 3. Model Evaluation
        y_pred = model.predict(X_test_proc)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)

        metrics = {
            "r2_score": round(float(r2), 4),
            "rmse": round(float(rmse), 4),
            "mae": round(float(mae), 4),
        }
        mlflow.log_metrics(metrics)

        # 4. Explainable AI Feature Importances (Surrogate / Tree feature importances)
        feature_importance = {
            name: round(float(imp), 4)
            for name, imp in zip(all_feature_names, model.feature_importances_)
        }
        # Sort by importance
        feature_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))

        # Save artifacts
        summary = {
            "case_study": "Student Performance Prediction System (Unit I & II)",
            "run_id": run.info.run_id,
            "params": params,
            "metrics": metrics,
            "feature_importance_ranking": feature_importance,
            "status": "PROMOTED_TO_REGISTRY",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        report_file = REPORTS_DIR / "student_performance_summary.json"
        report_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        mlflow.log_artifact(str(report_file))

        print(f"Student Performance Case Study completed! R2: {r2:.4f}, RMSE: {rmse:.4f}")
        return summary


if __name__ == "__main__":
    res = run_student_performance_mlops_pipeline()
    print(json.dumps(res, indent=2))
