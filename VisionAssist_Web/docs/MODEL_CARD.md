# VisionAssist AI: Enterprise Model Card & Fairness Audit

*Generated on: 2026-10-26 18:20:33*  
*MLOps Unit V: Ethics, Interpretability, and Subgroup Auditing*

---

## 1. Model Details
- **Architecture**: Ultralytics YOLOv8-Nano (PyTorch & ONNX quantized INT8/FP16)
- **Primary Function**: Real-time object, obstacle, and campus hazard perception with sub-65ms latency.
- **Target Audience**: Visually Impaired Individuals, Wheelchair Users, and Assistive Robotics.
- **Deployment Platform**: Edge Web App (Browser WebAssembly / FastAPI Stream) & Edge IoT.

---

## 2. Intended Use & Safety Limitations
- **Intended Use**: Real-time obstacle awareness, navigation wayfinding, drop-off warnings.
- **Out-of-Scope Use**: Sole navigation reliance during rapid vehicle traffic or complete total darkness (< 1 Lux) without supplemental illumination.

---

## 3. Subgroup Performance & Fairness Matrix (Unit V)

Evaluating whether the assistive model behaves equitably across environmental variations:

| Subgroup Condition | Samples | Precision | Recall | F1-Score | mAP@0.50 | Disparate Impact | 4/5ths Rule Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Daylight Normal | 350 | 0.892 | 0.871 | 0.881 | 0.865 | 1.0 | FAIR |
| Low Light Corridor | 280 | 0.814 | 0.768 | 0.790 | 0.772 | 0.882 | FAIR |
| High Glare Outdoor | 220 | 0.795 | 0.742 | 0.768 | 0.748 | 0.852 | FAIR |

### Fairness Analysis Summary
- **Daylight vs. Low-Light Disparate Impact**: `0.882` (Passes >= 0.80 Four-Fifths threshold).
- **Daylight vs. Glare Disparate Impact**: `0.852` (Passes >= 0.80 Four-Fifths threshold).
- **Mitigation Recommendation**: In low-light environments (ERI < 0.40), the DecisionEngine activates audio notifications informing the user of degraded camera visibility, preventing false safety confidence.

---

## 4. Model Explainability & Interpretability (XAI)

Feature importance attribution for audio speech warning trigger decisions:

| Decision Factor / Feature | Importance Weight | Visual Distribution |
| :--- | :--- | :--- |
| `bounding_box_center_proximity (horizontal center alignment)` | 0.38 (38%) | ███████ |
| `estimated_distance_meters (inverse distance metric)` | 0.28 (28%) | █████ |
| `object_velocity_or_expansion_rate (Time-to-collision TTC)` | 0.16 (16%) | ███ |
| `class_semantic_severity (e.g. stair/vehicle vs bench)` | 0.12 (12%) | ██ |
| `environmental_reliability_index_ERI` | 0.06 (6%) | █ |

- **Interpretability Rationale**: Bounding box center alignment accounts for 38% of alert triggering, ensuring users are never spammed by peripheral objects outside their trajectory.

---

## 5. Quantitative Distance Bracket Audits
- **Near Field (< 1.5m)**: Recall = **92.5%**, Critical Miss Rate = **1.2%** (Meets safety-critical threshold <= 2.0%).
- **Mid Field (1.5 - 4.0m)**: Recall = **83.2%**, Critical Miss Rate = **3.8%**.
- **Far Field (> 4.0m)**: Recall = **69.0%**, Critical Miss Rate = **8.9%**.
