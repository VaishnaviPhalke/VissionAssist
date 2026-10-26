# VisionAssist AI: Universal Assistive Vision & MLOps Platform

[![Tests](https://img.shields.io/badge/pytest-16%20passed-brightgreen.svg)]()
[![MLOps](https://img.shields.io/badge/MLOps%20Syllabus-Units%20I--VI%20100%25-blue.svg)]()
[![License](https://img.shields.io/badge/License-MIT-teal.svg)]()
[![YOLOv8](https://img.shields.io/badge/Model-YOLOv8--Nano%20%28ONNX%29-orange.svg)]()

VisionAssist AI is a real-time accessibility platform combining computer vision, audio-spatial obstacle awareness, Ground Traversability profiling, Fleet Spatial Memory rerouting, and an enterprise end-to-end MLOps lifecycle covering Units I through VI.

---

## 🎨 System Screens & User Interface

VisionAssist AI features a bright, high-contrast, modern UI built with **Plus Jakarta Sans** and **JetBrains Mono**, featuring 5 distinct operational screens:

1. **Screen 1: Live Visual Assistant & SafePath HUD**
   - Live camera stream with sub-65ms real-time YOLOv8-Nano bounding boxes and persistent tracking IDs (`#1`, `#2`).
   - Integrated **SafePath HUD**: Ground Traversability zone (drop-off/stairs alert), Overhead Clearance bar, and Time-to-Collision (TTC) alert overlay.
   - Spatial 3D Audio stereo panner adjusting sound balance (-1.0 left to +1.0 right).

2. **Screen 2: Campus Navigation & Fleet Rerouting**
   - Dijkstra-based pathfinding across campus graph nodes (Auditorium, Library, CSE Dept, Labs).
   - Multi-Persona Accessibility Routing: **BVI**, **Wheelchair** (strictly step-free, prunes staircases), **Elderly** (low-fatigue), and **Emergency** (nearest exit).

3. **Screen 3: OCR Reader & Signboard Assistant**
   - On-demand high-accuracy text extraction from campus signage, room boards, and elevator indicators via Tesseract OCR engine.

4. **Screen 4: Fleet Spatial Memory**
   - Distributed crowd-sensed campus micro-hazard registry. Allows users or sensors to report temporary obstacles (e.g., wet floors, maintenance).
   - The campus navigation graph automatically reroutes all users around reported hazard nodes in real time.

5. **Screen 5: MLOps Telemetry & Quality Gate Center**
   - Live real-time dashboard displaying Model Checkpoint status, sub-65ms inference speed, nominal FPS, Automated Quality Gate pass/fail state, and environmental lighting/blur drift.

---

## 📚 Complete MLOps Syllabus Compliance Matrix (100% Coverage)

VisionAssist AI satisfies all 6 Units of the academic and industry MLOps curriculum:

| Unit | Syllabus Focus | VisionAssist Implementation | Status |
| :--- | :--- | :--- | :--- |
| **Unit I** | Introduction & Problem Formulation | Student Performance Prediction case study (`mlops/case_study_student_performance.py`), synthetic data pipeline, DVC data versioning (`dvc.yaml`). | **100% Verified** |
| **Unit II** | Data Engineering & Feature Store | ColumnTransformer with `StandardScaler` (continuous metrics) and `OneHotEncoder` (categorical variables). Train/val/test splits with reproducible random seeds. | **100% Verified** |
| **Unit III**| Model Training & Pipeline Orchestration | YOLOv8-Nano transfer learning, MLflow parameter & metric tracking (`mlops/train_mlflow.py`), Apache Airflow DAG (`mlops/airflow_dag.py`). | **100% Verified** |
| **Unit IV** | Model Deployment & Serving Patterns | Real-time streaming API (FastAPI + WebSocket/Blob) vs. Offline Batch Inference Pipeline (`mlops/batch_inference.py`), containerized with production `Dockerfile`. | **100% Verified** |
| **Unit V**  | Model Monitoring, Ethics & Explainability | Lighting & blur drift monitor (`mlops/drift_monitor.py`), Subgroup Fairness matrix (Four-Fifths rule), DecisionEngine attribution, and enterprise Model Card (`docs/MODEL_CARD.md`). | **100% Verified** |
| **Unit VI** | Cloud MLOps & CI/CD Retraining | Declarative AWS SageMaker Pipeline specification (`mlops/sagemaker_pipeline.py`), GitHub Actions CI/CD workflow (`.github/workflows/mlops_ci_cd.yml`). | **100% Verified** |

---

## 🚀 Quick Start (Running the Application)

### 1. Launch Web Application
```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Open **`http://127.0.0.1:8000`** in Google Chrome or Microsoft Edge.

### 2. Run Complete Test Suite
```powershell
python -m pytest tests/ -v
```
*All 16 unit, integration, and MLOps pipeline tests run and pass green.*

### 3. Run Individual MLOps Components
- **Student Performance Case Study (Unit I & II)**:
  ```powershell
  python mlops/case_study_student_performance.py
  ```
- **Batch Inference Pipeline (Unit IV)**:
  ```powershell
  python mlops/batch_inference.py --batch_size 4
  ```
- **Explainability & Subgroup Fairness Audit (Unit V)**:
  ```powershell
  python mlops/explainability_audit.py
  ```
- **AWS SageMaker Cloud Retraining DAG Spec (Unit VI)**:
  ```powershell
  python mlops/sagemaker_pipeline.py
  ```

---

## 🐳 Docker Deployment

The application includes an enterprise container configuration supporting OpenCV and OCR dependencies:

```bash
docker build -t visionassist-ai .
docker run -p 8000:8000 visionassist-ai
```
