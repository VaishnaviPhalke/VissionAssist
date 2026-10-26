"""
VisionAssist AI - Unit IV Batch Inference Pipeline
Contrasting batch processing vs. real-time sub-100ms streaming inference.

This script executes offline high-throughput batch evaluation across campus
camera image dumps, produces latency distributions, flags safety-critical
hazards, and exports both structured JSON summary and tabular CSV reports.
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
import numpy as np
import cv2

# Safe PyTorch 2.6+ unpickler patch for Ultralytics
import torch
_orig_load = torch.load
def _safe_load(*args, **kwargs):
    kwargs["weights_only"] = False
    return _orig_load(*args, **kwargs)
torch.load = _safe_load

from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_MODEL = BASE_DIR / "models" / "yolov8n.pt"
RUNS_DIR = BASE_DIR / "runs"
RUNS_DIR.mkdir(parents=True, exist_ok=True)


def generate_synthetic_batch_frames(output_dir: Path, count: int = 15) -> list:
    """Creates synthetic campus test frames if no real image dump is provided."""
    output_dir.mkdir(parents=True, exist_ok=True)
    frame_paths = []
    
    # Campus scenarios: daylight hall, low-light corridor, outdoor path
    scenarios = [
        ("daylight_corridor", (210, 210, 215), True),
        ("lowlight_hall", (40, 45, 50), False),
        ("stairwell_glare", (180, 190, 230), True),
        ("cafeteria_obstacle", (120, 140, 130), True),
    ]
    
    for i in range(count):
        name, bg_color, add_hazard = scenarios[i % len(scenarios)]
        img = np.full((480, 640, 3), bg_color, dtype=np.uint8)
        
        # Add texture & simulated objects
        cv2.putText(img, f"VisionAssist Campus Feed #{i+1} [{name}]", 
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        if add_hazard:
            # Draw synthetic box simulating a person or obstacle
            cv2.rectangle(img, (200 + (i*15)%200, 150), (320 + (i*15)%200, 420), (50, 80, 200), -1)
            cv2.putText(img, "SIMULATED OBSTACLE", (210 + (i*15)%200, 140), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        file_path = output_dir / f"batch_frame_{i+1:03d}_{name}.jpg"
        cv2.imwrite(str(file_path), img)
        frame_paths.append(file_path)

    return frame_paths


def run_batch_inference(
    image_dir: Path,
    model_path: Path = DEFAULT_MODEL,
    conf_threshold: float = 0.35,
    batch_size: int = 8,
    output_summary_path: Path = None,
) -> dict:
    """
    Executes offline batch prediction over a folder of image files.
    Calculates throughput (FPS), latency percentiles (P50, P95, P99),
    and aggregates detected hazards.
    """
    if not model_path.exists():
        # Fallback to base yolov8n.pt if models/yolov8n.pt not yet populated
        if (BASE_DIR / "yolov8n.pt").exists():
            model_path = BASE_DIR / "yolov8n.pt"
        else:
            raise FileNotFoundError(f"YOLO model not found at {model_path}")

    print(f"[Batch Inference] Loading model: {model_path}")
    model = YOLO(str(model_path))

    # Collect images
    supported_exts = {".jpg", ".jpeg", ".png", ".bmp"}
    img_paths = [p for p in image_dir.glob("*") if p.suffix.lower() in supported_exts]
    
    if not img_paths:
        print(f"[Batch Inference] No images found in {image_dir}. Generating synthetic test frames...")
        img_paths = generate_synthetic_batch_frames(image_dir, count=12)

    total_images = len(img_paths)
    print(f"[Batch Inference] Processing {total_images} images with batch size {batch_size}...")

    inference_latencies = []
    hazard_events = []
    detection_counts = {}
    csv_rows = ["frame_name,num_detections,detected_labels,inference_time_ms,hazard_flag"]

    start_total_time = time.time()

    # Process in batches
    for i in range(0, total_images, batch_size):
        chunk = img_paths[i:i + batch_size]
        str_chunk = [str(p) for p in chunk]

        t0 = time.time()
        results = model.predict(source=str_chunk, conf=conf_threshold, verbose=False)
        t_batch_ms = (time.time() - t0) * 1000.0

        per_image_lat = t_batch_ms / len(chunk)

        for path, res in zip(chunk, results):
            inference_latencies.append(per_image_lat)
            detected_classes = []
            hazard_flag = False

            if res.boxes is not None and len(res.boxes) > 0:
                for box in res.boxes:
                    cls_id = int(box.cls[0].item())
                    cls_name = model.names.get(cls_id, f"class_{cls_id}")
                    detected_classes.append(cls_name)
                    detection_counts[cls_name] = detection_counts.get(cls_name, 0) + 1

                    # Identify accessibility hazards (chairs, bottles, bicycles, stairs, people in direct path)
                    if cls_name in ["person", "chair", "bicycle", "traffic light", "fire hydrant", "stairs"]:
                        hazard_flag = True

            if hazard_flag:
                hazard_events.append({
                    "frame": path.name,
                    "detections": detected_classes,
                    "per_image_ms": round(per_image_lat, 2)
                })

            csv_rows.append(f"{path.name},{len(detected_classes)},\"{';'.join(detected_classes)}\",{per_image_lat:.2f},{hazard_flag}")

    total_wall_time = time.time() - start_total_time
    fps = total_images / total_wall_time if total_wall_time > 0 else 0.0

    lat_arr = np.array(inference_latencies)
    summary = {
        "status": "SUCCESS",
        "dataset_size": total_images,
        "batch_size": batch_size,
        "total_wall_time_seconds": round(total_wall_time, 3),
        "throughput_fps": round(fps, 2),
        "latency_metrics_ms": {
            "mean": round(float(np.mean(lat_arr)), 2),
            "median_p50": round(float(np.percentile(lat_arr, 50)), 2),
            "p95": round(float(np.percentile(lat_arr, 95)), 2),
            "p99": round(float(np.percentile(lat_arr, 99)), 2),
            "min": round(float(np.min(lat_arr)), 2),
            "max": round(float(np.max(lat_arr)), 2),
        },
        "hazard_flagged_frames": len(hazard_events),
        "class_distribution": detection_counts,
        "hazards_sample": hazard_events[:5],
        "comparison_realtime_vs_batch": {
            "realtime_streaming_paradigm": "Sub-100ms single-frame sequential pipeline with speech cooldown & immediate spatial alerts.",
            "batch_inference_paradigm": "High-throughput asynchronous offline processing optimized for GPU vectorization and campus audit reports."
        }
    }

    # Save outputs
    if output_summary_path is None:
        output_summary_path = RUNS_DIR / "batch_inference_summary.json"
    
    with open(output_summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    csv_path = RUNS_DIR / "batch_inference_log.csv"
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("\n".join(csv_rows))

    print(f"[Batch Inference] Summary written to {output_summary_path}")
    print(f"[Batch Inference] CSV log written to {csv_path}")
    print(f"[Batch Inference] Throughput: {fps:.1f} FPS | P95 Latency: {summary['latency_metrics_ms']['p95']}ms")

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VisionAssist Batch Inference Pipeline (Unit IV)")
    parser.add_argument("--image_dir", type=str, default=str(RUNS_DIR / "batch_test_frames"),
                        help="Path to folder containing campus frames")
    parser.add_argument("--batch_size", type=int, default=4, help="Batch size for batch inference")
    parser.add_argument("--conf", type=float, default=0.35, help="Confidence threshold")
    args = parser.parse_args()

    run_batch_inference(
        image_dir=Path(args.image_dir),
        batch_size=args.batch_size,
        conf_threshold=args.conf
    )
