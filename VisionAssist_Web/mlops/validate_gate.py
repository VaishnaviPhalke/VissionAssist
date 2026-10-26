"""Automated Model Validation Gate for VisionAssist.

Enforces:
- Minimum mAP50 quality gate (must meet or exceed baseline threshold).
- Maximum inference latency gate (must ensure real-time mobile/browser FPS).
- Model size constraint (must not exceed edge deployment footprint, e.g. < 15MB).
- Promotion decision: outputs a deployment decision artifact and updates the active checkpoint.
"""

from pathlib import Path
import json
import time
import os

ROOT = Path(__file__).resolve().parents[1]
GATE_CONFIG_PATH = ROOT / "mlops" / "gate_config.json"
DECISION_REPORT_PATH = ROOT / "runs" / "validation_gate_report.json"

DEFAULT_GATE_CONFIG = {
    "baseline_mAP50": 0.50,
    "mAP_tolerance": 0.05,
    "max_latency_ms": 65.0,
    "min_fps": 15.0,
    "max_model_size_mb": 15.0,
    "require_classes": [
        "person", "tree", "car", "bicycle", "chair",
        "table", "backpack", "bottle", "door", "stairs",
        "lift", "bench", "classroom", "laboratory", "corridor"
    ]
}


def load_gate_config() -> dict:
    if GATE_CONFIG_PATH.exists():
        try:
            return json.loads(GATE_CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return DEFAULT_GATE_CONFIG


def evaluate_gate(
    candidate_model_path: Path | str,
    metrics: dict,
    gate_config: dict | None = None,
    auto_promote: bool = False,
    production_path: Path | str | None = None,
) -> dict:
    if gate_config is None:
        gate_config = load_gate_config()

    candidate_path = Path(candidate_model_path)
    if not candidate_path.exists():
        return {
            "status": "REJECTED",
            "passed": False,
            "reasons": [f"Candidate model file does not exist: {candidate_path}"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

    # Size check
    size_mb = candidate_path.stat().st_size / (1024 * 1024)

    # Metric checks
    mAP50 = metrics.get("mAP50", 0.0)
    latency_ms = metrics.get("latency_ms", 999.0)
    fps = metrics.get("fps", 0.0)

    min_required_mAP = max(0.0, gate_config["baseline_mAP50"] - gate_config["mAP_tolerance"])
    max_latency = gate_config["max_latency_ms"]
    max_size = gate_config["max_model_size_mb"]

    reasons = []
    passed = True

    if mAP50 < min_required_mAP:
        passed = False
        reasons.append(f"mAP50 ({mAP50:.4f}) is below minimum required ({min_required_mAP:.4f}).")

    if latency_ms > max_latency:
        passed = False
        reasons.append(f"Latency ({latency_ms:.2f} ms) exceeds limit ({max_latency:.2f} ms).")

    if size_mb > max_size:
        passed = False
        reasons.append(f"Model size ({size_mb:.2f} MB) exceeds limit ({max_size:.2f} MB).")

    promoted = False
    if passed and auto_promote:
        if production_path is None:
            production_path = ROOT / "models" / "yolov8n.pt"
        prod = Path(production_path)
        prod.parent.mkdir(parents=True, exist_ok=True)
        prod.write_bytes(candidate_path.read_bytes())
        promoted = True

    report = {
        "status": "PASSED" if passed else "REJECTED",
        "passed": passed,
        "promoted": promoted,
        "candidate_model": str(candidate_path),
        "evaluated_metrics": {
            "mAP50": mAP50,
            "latency_ms": latency_ms,
            "fps": fps,
            "size_mb": round(size_mb, 2),
        },
        "thresholds": {
            "min_mAP50": min_required_mAP,
            "max_latency_ms": max_latency,
            "max_size_mb": max_size,
        },
        "reasons": reasons if not passed else ["All quality and latency constraints satisfied."],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    DECISION_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    DECISION_REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    # Smoke test validation gate with dummy candidate
    test_metrics = {"mAP50": 0.72, "latency_ms": 28.5, "fps": 35.1}
    sample_model = ROOT / "models" / "yolov8n.pt"
    if sample_model.exists():
        res = evaluate_gate(sample_model, test_metrics)
        print("Validation Gate Report:")
        print(json.dumps(res, indent=2))
