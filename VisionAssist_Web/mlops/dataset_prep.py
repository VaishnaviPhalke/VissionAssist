"""Dataset Preparation, Validation, and DVC Pipeline Utility for VisionAssist.

Handles:
- YOLO dataset folder verification and dataset/data.yaml generation.
- Class distribution and label integrity audits.
- Synthetic/sample data generation for pipeline smoke testing and CI/CD.
"""

from pathlib import Path
import json
import yaml
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATASET_DIR = ROOT / "dataset"
CLASSES_FILE = DATA_DIR / "classes.yaml"

TARGET_CLASSES = [
    "person", "tree", "car", "bicycle", "chair",
    "table", "backpack", "bottle", "door", "stairs",
    "lift", "bench", "classroom", "laboratory", "corridor"
]


def ensure_dataset_structure(base_dir: Path = DATASET_DIR) -> dict[str, Path]:
    paths = {
        "images_train": base_dir / "images" / "train",
        "images_val": base_dir / "images" / "val",
        "images_test": base_dir / "images" / "test",
        "labels_train": base_dir / "labels" / "train",
        "labels_val": base_dir / "labels" / "val",
        "labels_test": base_dir / "labels" / "test",
    }
    for p in paths.values():
        p.mkdir(parents=True, exist_ok=True)
    return paths


def generate_data_yaml(base_dir: Path = DATASET_DIR, output_file: Path | None = None) -> Path:
    if output_file is None:
        output_file = base_dir / "data.yaml"

    config = {
        "path": str(base_dir.resolve()).replace("\\", "/"),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "nc": len(TARGET_CLASSES),
        "names": TARGET_CLASSES,
    }
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, sort_keys=False)
    return output_file


def audit_dataset(base_dir: Path = DATASET_DIR) -> dict:
    ensure_dataset_structure(base_dir)
    stats = {}
    total_images = 0
    total_annotations = 0
    class_counts = {cls_name: 0 for cls_name in TARGET_CLASSES}

    for split in ["train", "val", "test"]:
        img_dir = base_dir / "images" / split
        lbl_dir = base_dir / "labels" / split
        images = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png"))
        labels = list(lbl_dir.glob("*.txt"))

        split_annots = 0
        for lbl_file in labels:
            try:
                lines = lbl_file.read_text(encoding="utf-8").strip().splitlines()
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 5:
                        cls_idx = int(parts[0])
                        if 0 <= cls_idx < len(TARGET_CLASSES):
                            class_counts[TARGET_CLASSES[cls_idx]] += 1
                            split_annots += 1
            except Exception:
                pass

        stats[split] = {
            "image_count": len(images),
            "label_file_count": len(labels),
            "annotations": split_annots,
        }
        total_images += len(images)
        total_annotations += split_annots

    return {
        "total_images": total_images,
        "total_annotations": total_annotations,
        "splits": stats,
        "class_distribution": class_counts,
        "classes": TARGET_CLASSES,
    }


def create_sample_dataset(base_dir: Path = DATASET_DIR, samples_per_split: int = 5) -> dict:
    """Creates a lightweight sample dataset so the MLOps pipeline and tests can run end-to-end immediately."""
    paths = ensure_dataset_structure(base_dir)
    generate_data_yaml(base_dir)

    splits = {
        "train": (paths["images_train"], paths["labels_train"], samples_per_split * 2),
        "val": (paths["images_val"], paths["labels_val"], samples_per_split),
        "test": (paths["images_test"], paths["labels_test"], samples_per_split),
    }

    colors = [(220, 50, 50), (50, 200, 50), (50, 100, 220), (220, 200, 50)]

    for split_name, (img_folder, lbl_folder, count) in splits.items():
        for i in range(count):
            img_path = img_folder / f"sample_{split_name}_{i:03d}.jpg"
            lbl_path = lbl_folder / f"sample_{split_name}_{i:03d}.txt"

            if img_path.exists() and lbl_path.exists():
                continue

            # Draw a sample campus image with geometric objects representing doors, stairs, chairs
            img = Image.new("RGB", (640, 640), color=(240, 240, 245))
            draw = ImageDraw.Draw(img)

            # Assign 1-2 bounding boxes
            annotations = []
            cls_1 = i % len(TARGET_CLASSES)
            # Box 1 (center)
            x_center, y_center, w, h = 0.5, 0.5, 0.35, 0.4
            draw.rectangle([640 * (x_center - w / 2), 640 * (y_center - h / 2),
                            640 * (x_center + w / 2), 640 * (y_center + h / 2)],
                           fill=colors[i % len(colors)], outline=(20, 20, 20), width=3)
            annotations.append(f"{cls_1} {x_center:.4f} {y_center:.4f} {w:.4f} {h:.4f}")

            if i % 2 == 1:
                cls_2 = (i + 4) % len(TARGET_CLASSES)
                x2, y2, w2, h2 = 0.8, 0.7, 0.25, 0.3
                draw.rectangle([640 * (x2 - w2 / 2), 640 * (y2 - h2 / 2),
                                640 * (x2 + w2 / 2), 640 * (y2 + h2 / 2)],
                               fill=(180, 180, 180), outline=(0, 0, 0), width=2)
                annotations.append(f"{cls_2} {x2:.4f} {y2:.4f} {w2:.4f} {h2:.4f}")

            img.save(img_path, format="JPEG", quality=85)
            lbl_path.write_text("\n".join(annotations), encoding="utf-8")

    return audit_dataset(base_dir)


if __name__ == "__main__":
    print("Preparing VisionAssist dataset structure...")
    res = create_sample_dataset()
    print("Dataset audit report:")
    print(json.dumps(res, indent=2))
