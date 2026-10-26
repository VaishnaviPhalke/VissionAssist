from pathlib import Path
import os
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "models"
STATIC_DIR = ROOT / "static"
MODEL_PATH = Path(os.getenv("VISIONASSIST_MODEL", MODEL_DIR / "yolov8n.pt"))
CLASSES_PATH = DATA_DIR / "classes.yaml"
CAMPUS_MAP_PATH = DATA_DIR / "campus_map.json"

INPUT_SIZE = int(os.getenv("VISIONASSIST_INPUT_SIZE", "640"))
CONF_THRESHOLD = float(os.getenv("VISIONASSIST_CONF_THRESHOLD", "0.35"))
IOU_THRESHOLD = float(os.getenv("VISIONASSIST_IOU_THRESHOLD", "0.45"))
MAX_DETECTIONS = int(os.getenv("VISIONASSIST_MAX_DETECTIONS", "30"))


def load_classes() -> dict:
    with CLASSES_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
