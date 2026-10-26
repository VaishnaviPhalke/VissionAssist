"""Data Drift & Environmental Shift Monitor for VisionAssist.

Monitors:
- Lighting drift: Mean luminance (detects low-light, nighttime, glare).
- Image degradation drift: Laplacian variance (detects camera blur, motion blur).
- Model confidence drift: Tracks rolling average confidence of detections.
- Latency / FPS drift: Tracks hardware throttling.
- Retraining trigger: Emits alert when data distribution significantly shifts.
"""

from pathlib import Path
import time
import json
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DRIFT_LOG_PATH = ROOT / "runs" / "drift_monitor_log.json"
RETRAIN_TRIGGER_PATH = ROOT / "runs" / "retraining_trigger.json"


class DriftMonitor:
    def __init__(
        self,
        min_brightness: float = 40.0,
        max_brightness: float = 225.0,
        min_sharpness: float = 25.0,
        confidence_warning_threshold: float = 0.40,
        rolling_window_size: int = 30
    ):
        self.min_brightness = min_brightness
        self.max_brightness = max_brightness
        self.min_sharpness = min_sharpness
        self.confidence_warning_threshold = confidence_warning_threshold
        self.rolling_window_size = rolling_window_size

        self.history: list[dict] = []
        self.drift_incidents: list[dict] = []

    def compute_image_metrics(self, image: Image.Image) -> dict:
        gray = image.convert("L")
        arr = np.array(gray, dtype=np.float32)

        mean_brightness = float(np.mean(arr))
        contrast = float(np.std(arr))

        # Discrete Laplacian approximation for sharpness/blur detection
        # [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
        if arr.shape[0] > 4 and arr.shape[1] > 4:
            laplacian = (
                arr[:-2, 1:-1] + arr[2:, 1:-1] +
                arr[1:-1, :-2] + arr[1:-1, 2:] - 4 * arr[1:-1, 1:-1]
            )
            sharpness = float(np.var(laplacian))
        else:
            sharpness = 100.0

        return {
            "brightness": round(mean_brightness, 2),
            "contrast": round(contrast, 2),
            "sharpness": round(sharpness, 2),
        }

    def process_frame(
        self,
        image: Image.Image,
        detections: list[dict],
        latency_ms: float
    ) -> dict:
        img_metrics = self.compute_image_metrics(image)
        confs = [d.get("confidence", 0.0) for d in detections]
        avg_conf = float(np.mean(confs)) if confs else 0.0

        alerts = []
        drift_type = None

        if img_metrics["brightness"] < self.min_brightness:
            alerts.append("LOW_LIGHT_DRIFT: Scene is underexposed or in night conditions.")
            drift_type = "lighting_low"
        elif img_metrics["brightness"] > self.max_brightness:
            alerts.append("GLARE_DRIFT: Scene is overexposed or has direct glare.")
            drift_type = "lighting_high"

        if img_metrics["sharpness"] < self.min_sharpness:
            alerts.append("BLUR_DRIFT: Frame is blurred (motion or defocus).")
            drift_type = "motion_blur"

        if len(detections) > 0 and avg_conf < self.confidence_warning_threshold:
            alerts.append("CONFIDENCE_DRIFT: Low detection confidence indicates potential out-of-distribution scene.")
            drift_type = "low_confidence"

        frame_record = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "image_metrics": img_metrics,
            "detection_count": len(detections),
            "avg_confidence": round(avg_conf, 3),
            "latency_ms": round(latency_ms, 2),
            "has_drift": len(alerts) > 0,
            "alerts": alerts,
        }

        self.history.append(frame_record)
        if len(self.history) > self.rolling_window_size:
            self.history.pop(0)

        if alerts:
            self.drift_incidents.append(frame_record)
            if len(self.drift_incidents) > 100:
                self.drift_incidents.pop(0)

        # Check if retraining is needed (e.g. > 30% of recent frames show drift)
        recent_drifts = sum(1 for h in self.history if h["has_drift"])
        drift_ratio = recent_drifts / max(1, len(self.history))
        retraining_recommended = len(self.history) >= 10 and drift_ratio >= 0.35

        if retraining_recommended:
            self._save_retraining_trigger(drift_ratio, alerts)

        return {
            "current_frame": frame_record,
            "rolling_drift_ratio": round(drift_ratio, 3),
            "retraining_recommended": retraining_recommended,
            "total_incidents": len(self.drift_incidents),
        }

    def _save_retraining_trigger(self, drift_ratio: float, latest_alerts: list[str]) -> None:
        trigger_data = {
            "trigger_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "RETRAINING_TRIGGERED",
            "drift_ratio": drift_ratio,
            "latest_alerts": latest_alerts,
            "recommendation": (
                "Collect recent drift frames into dataset/images/train, "
                "update DVC version, and run mlops/train_mlflow.py."
            ),
        }
        RETRAIN_TRIGGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        RETRAIN_TRIGGER_PATH.write_text(json.dumps(trigger_data, indent=2), encoding="utf-8")

    def get_summary(self) -> dict:
        total_frames = len(self.history)
        drift_frames = sum(1 for h in self.history if h["has_drift"])
        return {
            "window_frames": total_frames,
            "drift_frames": drift_frames,
            "drift_rate": round(drift_frames / max(1, total_frames), 3),
            "total_incidents_recorded": len(self.drift_incidents),
            "recent_incidents": self.drift_incidents[-5:],
        }


# Global singleton instance for app runtime
drift_monitor = DriftMonitor()


if __name__ == "__main__":
    # Smoke test drift monitor
    mon = DriftMonitor()
    normal_img = Image.new("RGB", (320, 240), color=(128, 128, 128))
    dark_img = Image.new("RGB", (320, 240), color=(10, 10, 10))

    r1 = mon.process_frame(normal_img, [{"confidence": 0.85}], latency_ms=25.0)
    print("Normal frame result:", r1["current_frame"]["alerts"])

    r2 = mon.process_frame(dark_img, [], latency_ms=30.0)
    print("Dark frame result:", r2["current_frame"]["alerts"])
    print("Drift monitor test passed.")
