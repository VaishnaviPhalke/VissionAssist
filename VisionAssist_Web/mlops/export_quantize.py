"""Model Optimization, Quantization, and Export for VisionAssist Edge Deployment.

Exports:
- ONNX format (for cross-platform runtime / WebAssembly / ONNX Runtime).
- TFLite format (FP16 / INT8) for Android and edge acceleration.
- Benchmarks model size and computes compression ratio.
"""

from pathlib import Path
import json
import time
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
DEFAULT_MODEL = ROOT / "models" / "yolov8n.pt"
EXPORT_DIR = ROOT / "models" / "exported"


def export_model(
    model_path: Path | str = DEFAULT_MODEL,
    formats: list[str] | None = None,
    imgsz: int = 640,
    half: bool = True
) -> dict:
    if formats is None:
        formats = ["onnx"]

    src = Path(model_path)
    if not src.exists():
        raise FileNotFoundError(f"Model checkpoint not found: {src}")

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    orig_size_mb = src.stat().st_size / (1024 * 1024)

    model = YOLO(str(src))
    results = {}

    for fmt in formats:
        t0 = time.perf_counter()
        try:
            print(f"Exporting {src.name} to {fmt.upper()} (half={half})...")
            exported_path = model.export(
                format=fmt,
                imgsz=imgsz,
                half=half if fmt in ["onnx", "engine"] else False,
                dynamic=False,
                simplify=True,
            )
            elapsed = time.perf_counter() - t0
            p = Path(exported_path)
            export_size_mb = p.stat().st_size / (1024 * 1024) if p.exists() else 0.0

            results[fmt] = {
                "status": "SUCCESS",
                "path": str(p),
                "size_mb": round(export_size_mb, 2),
                "compression_ratio": round(orig_size_mb / max(0.01, export_size_mb), 2),
                "export_time_sec": round(elapsed, 2),
            }
        except Exception as exc:
            results[fmt] = {
                "status": "FAILED",
                "error": str(exc),
                "export_time_sec": round(time.perf_counter() - t0, 2),
            }

    summary = {
        "source_model": str(src),
        "source_size_mb": round(orig_size_mb, 2),
        "exports": results,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    report_path = ROOT / "runs" / "export_optimization_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    if DEFAULT_MODEL.exists():
        print(f"Optimizing {DEFAULT_MODEL}...")
        report = export_model(formats=["onnx"])
        print(json.dumps(report, indent=2))
