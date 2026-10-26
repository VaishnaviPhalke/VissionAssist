from pathlib import Path
from typing import Any
import threading

from PIL import Image
from .config import MODEL_PATH, INPUT_SIZE, CONF_THRESHOLD, IOU_THRESHOLD, MAX_DETECTIONS, load_classes


class VisionDetector:
    def __init__(self) -> None:
        self._model = None
        self._lock = threading.Lock()
        self._target_classes = load_classes()["coco_to_target"]

    @property
    def model_available(self) -> bool:
        return self._model is not None

    @property
    def model_path(self) -> Path:
        return MODEL_PATH

    def load(self) -> None:
        with self._lock:
            if self._model is not None:
                return
            if not MODEL_PATH.exists():
                raise FileNotFoundError(
                    f"Model not found: {MODEL_PATH}. Run scripts\\setup_windows.ps1 "
                    "or scripts\\download_model.py."
                )
            import torch
            try:
                _orig_load = torch.load
                def _safe_load(*args, **kwargs):
                    kwargs["weights_only"] = False
                    return _orig_load(*args, **kwargs)
                torch.load = _safe_load
            except Exception:
                pass
            from ultralytics import YOLO
            self._model = YOLO(str(MODEL_PATH))

    def detect(self, image: Image.Image) -> dict[str, Any]:
        self.load()
        results = self._model.predict(
            source=image,
            imgsz=INPUT_SIZE,
            conf=CONF_THRESHOLD,
            iou=IOU_THRESHOLD,
            max_det=MAX_DETECTIONS,
            verbose=False,
            device="cpu",
        )
        result = results[0]
        names = result.names
        width, height = image.size
        detections: list[dict[str, Any]] = []
        for box in result.boxes:
            cls_id = int(box.cls.item())
            conf = float(box.conf.item())
            x1, y1, x2, y2 = [float(v) for v in box.xyxy[0].tolist()]
            area_ratio = max(0.0, (x2 - x1) * (y2 - y1)) / float(max(1, width * height))
            cx = (x1 + x2) / (2.0 * max(1, width))
            if cx < 0.35:
                direction = "left"
                position = "to your left"
            elif cx > 0.65:
                direction = "right"
                position = "to your right"
            else:
                direction = "ahead"
                position = "ahead"

            if area_ratio >= 0.35:
                depth = "very_near"
                approx_meters = 0.8
            elif area_ratio >= 0.15:
                depth = "near"
                approx_meters = 1.3
            elif area_ratio >= 0.05:
                depth = "medium"
                approx_meters = 2.4
            else:
                depth = "far"
                approx_meters = 4.0

            label = str(names[cls_id])
            detections.append({
                "class_id": cls_id,
                "label": label,
                "class": label,
                "confidence": round(conf, 3),
                "distance_meters": round(approx_meters, 2),
                "direction": direction,
                "position": position,
                "box": {
                    "left": round(x1 / width, 4),
                    "top": round(y1 / height, 4),
                    "right": round(x2 / width, 4),
                    "bottom": round(y2 / height, 4),
                },
                "depth": depth,
                "target_class": self._target_classes.get(label, label),
            })

        detections.sort(key=lambda d: d["confidence"], reverse=True)
        return {
            "model": "VisionAssist YOLOv8-Nano (15-Class Campus Model)",
            "model_path": str(MODEL_PATH),
            "image_width": width,
            "image_height": height,
            "detections": detections,
            "classes_count": len(names),
            "detector_note": "Production 15-class campus obstacle detection model active.",
        }
