"""SafePath AI: Adaptive Surface & Hazard Profiler.

Implements:
- Ground Traversability Zone (bottom 35%): drop-offs, stairs, steps, surface irregularities.
- Overhead Clearance Zone (top 25%): hanging signs, low door frames, overhead hazards.
- Time-to-Collision (TTC) & rapid approach detection for dynamic obstacles.
- Environmental Reliability Index (ERI): combined lighting, blur, and perception safety index.
- Multi-Persona Accessibility Adaptation (BVI, Wheelchair, Elderly, Emergency).
"""

from typing import Any
import numpy as np
from PIL import Image


class SurfaceProfiler:
    def __init__(self):
        self._previous_areas: dict[int, tuple[float, float]] = {}  # track_id -> (area, timestamp)

    def analyze(
        self,
        image: Image.Image,
        detections: list[dict[str, Any]],
        persona: str = "bvi"
    ) -> dict[str, Any]:
        """Analyzes ground and overhead zones, calculates TTC, and computes Environmental Reliability Index."""
        gray = image.convert("L")
        w, h = gray.size
        arr = np.array(gray, dtype=np.float32)

        # 1. Ground Traversability Zone (Bottom 35% of frame)
        ground_top = int(h * 0.65)
        ground_roi = arr[ground_top:, :]
        ground_var = float(np.var(ground_roi))
        
        # Horizontal edge filter for step / drop-off edge detection (Sobel-like)
        if ground_roi.shape[0] > 4:
            horizontal_diff = np.abs(ground_roi[1:, :] - ground_roi[:-1, :])
            step_edge_density = float(np.mean(horizontal_diff))
        else:
            step_edge_density = 0.0

        # 2. Overhead Clearance Zone (Top 25% of frame)
        overhead_bottom = int(h * 0.25)
        overhead_roi = arr[:overhead_bottom, :]
        overhead_edge_density = float(np.std(overhead_roi))

        alerts = []
        is_step_hazard = step_edge_density > 24.0 or ground_var > 2200.0
        is_overhead_hazard = overhead_edge_density > 52.0

        # Persona-specific alerting
        if persona == "wheelchair":
            if is_step_hazard:
                alerts.append({
                    "zone": "ground",
                    "severity": "CRITICAL",
                    "message": "Caution: Curb, step, or surface transition ahead (inaccessible for wheelchair).",
                    "persona": "wheelchair"
                })
        elif persona == "bvi":
            if is_step_hazard:
                alerts.append({
                    "zone": "ground",
                    "severity": "WARNING",
                    "message": "Step or surface change detected near feet.",
                    "persona": "bvi"
                })
            if is_overhead_hazard:
                alerts.append({
                    "zone": "overhead",
                    "severity": "WARNING",
                    "message": "Low overhead clearance detected. Mind your head.",
                    "persona": "bvi"
                })
        elif persona == "elderly":
            if is_step_hazard:
                alerts.append({
                    "zone": "ground",
                    "severity": "WARNING",
                    "message": "Uneven surface ahead. Proceed with care or use railing.",
                    "persona": "elderly"
                })
        elif persona == "emergency":
            alerts.append({
                "zone": "guidance",
                "severity": "INFO",
                "message": "Emergency egress active. Heading toward nearest illuminated exit.",
                "persona": "emergency"
            })

        # 3. Calculate Time-to-Collision (TTC) for tracked obstacles
        enriched_dets = []
        approaching_threats = []

        for d in detections:
            tid = d.get("track_id")
            box = d.get("box", {})
            bw = max(0.01, box.get("right", 0) - box.get("left", 0))
            bh = max(0.01, box.get("bottom", 0) - box.get("top", 0))
            current_area = bw * bh

            is_approaching = False
            ttc_seconds = None

            if tid is not None:
                if tid in self._previous_areas:
                    prev_area, _ = self._previous_areas[tid]
                    growth_rate = (current_area - prev_area) / max(0.01, prev_area)
                    if growth_rate > 0.18 and d.get("depth") in ["near", "very_near"]:
                        is_approaching = True
                        # Approximate TTC: inverse of relative expansion rate
                        ttc_seconds = round(max(0.5, 1.0 / max(0.1, growth_rate)), 1)
                        approaching_threats.append({
                            "track_id": tid,
                            "label": d.get("label"),
                            "ttc_sec": ttc_seconds,
                            "position": d.get("position", "ahead")
                        })
                self._previous_areas[tid] = (current_area, 0)

            d_copy = dict(d)
            d_copy["approaching"] = is_approaching
            d_copy["ttc_sec"] = ttc_seconds
            enriched_dets.append(d_copy)

        # 4. Environmental Reliability Index (ERI)
        mean_luminance = float(np.mean(arr))
        sharpness = float(np.var(arr[1:, :] - arr[:-1, :])) if arr.shape[0] > 2 else 50.0

        norm_lum = max(0.0, min(1.0, mean_luminance / 160.0))
        norm_sharp = max(0.0, min(1.0, sharpness / 400.0))
        eri_score = round(0.55 * norm_lum + 0.45 * norm_sharp, 2)

        if eri_score >= 0.70:
            eri_status = "OPTIMAL"
            eri_guidance = "Clear visibility and full sensor confidence."
        elif eri_score >= 0.40:
            eri_status = "DEGRADED"
            eri_guidance = "Sub-optimal lighting or motion blur. Cautious advisory mode."
        else:
            eri_status = "UNRELIABLE"
            eri_guidance = "Severe darkness or camera obstruction. Vision guidance degraded."

        return {
            "persona": persona,
            "ground_profiler": {
                "step_edge_density": round(step_edge_density, 2),
                "surface_variance": round(ground_var, 1),
                "step_hazard": is_step_hazard,
            },
            "overhead_clearance": {
                "edge_density": round(overhead_edge_density, 2),
                "overhead_hazard": is_overhead_hazard,
            },
            "environmental_reliability": {
                "eri_score": eri_score,
                "status": eri_status,
                "guidance": eri_guidance,
            },
            "approaching_threats": approaching_threats,
            "alerts": alerts,
            "enriched_detections": enriched_dets,
        }


# Global singleton
surface_profiler = SurfaceProfiler()
