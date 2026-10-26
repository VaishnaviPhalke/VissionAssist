from pathlib import Path
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

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)
MODEL_PATH = MODEL_DIR / "yolov8n.pt"

if MODEL_PATH.exists():
    print(f"Already present: {MODEL_PATH}")
else:
    print("Downloading the standard YOLOv8n COCO-pretrained checkpoint via Ultralytics...")
    model = YOLO("yolov8n.pt")
    # Ultralytics downloads to its normal cache; copy the resulting file into this project.
    source = Path(model.ckpt_path if hasattr(model, "ckpt_path") else "yolov8n.pt")
    if source.exists():
        MODEL_PATH.write_bytes(source.read_bytes())
    else:
        fallback = Path("yolov8n.pt")
        if fallback.exists():
            MODEL_PATH.write_bytes(fallback.read_bytes())
        else:
            raise FileNotFoundError("Ultralytics did not expose the downloaded checkpoint path.")
    print(f"Saved: {MODEL_PATH}")
