"""Object Tracking, Decision Making, and Speech Cooldown Engine for VisionAssist.

Handles:
- Centroid/IoU tracking across continuous frames.
- Positional assignment: 'left', 'ahead' (center), 'right'.
- Proximity assessment: 'very_near', 'near', 'medium', 'far'.
- Speech cooldown and decision filter so user is not spammed every frame.
- Spatial audio panning values (-1.0 to +1.0) for 3D auditory orientation.
"""

import time
import math


class CentroidTracker:
    def __init__(self, max_disappeared: int = 5, distance_threshold: float = 0.25):
        self.next_object_id = 1
        self.objects: dict[int, dict] = {}
        self.disappeared: dict[int, int] = {}
        self.max_disappeared = max_disappeared
        self.distance_threshold = distance_threshold

    def update(self, detections: list[dict]) -> list[dict]:
        """Matches detections against existing tracks using normalized centroid distance."""
        if not detections:
            for obj_id in list(self.disappeared.keys()):
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.max_disappeared:
                    self._deregister(obj_id)
            return []

        input_centroids = []
        for det in detections:
            b = det["box"]
            cx = (b["left"] + b["right"]) / 2.0
            cy = (b["top"] + b["bottom"]) / 2.0
            input_centroids.append((cx, cy))

        if not self.objects:
            for i, det in enumerate(detections):
                self._register(input_centroids[i], det)
        else:
            object_ids = list(self.objects.keys())
            object_centroids = [self.objects[oid]["centroid"] for oid in object_ids]

            # Pairwise distance matrix
            used_objects = set()
            used_inputs = set()

            pairs = []
            for i, (icx, icy) in enumerate(input_centroids):
                for j, (ocx, ocy) in enumerate(object_centroids):
                    dist = math.hypot(icx - ocx, icy - ocy)
                    pairs.append((dist, i, object_ids[j]))

            pairs.sort(key=lambda x: x[0])

            for dist, input_idx, obj_id in pairs:
                if input_idx in used_inputs or obj_id in used_objects:
                    continue
                if dist > self.distance_threshold:
                    continue

                # Matched
                self.objects[obj_id]["centroid"] = input_centroids[input_idx]
                self.objects[obj_id]["detection"] = detections[input_idx]
                detections[input_idx]["track_id"] = obj_id
                self.disappeared[obj_id] = 0
                used_inputs.add(input_idx)
                used_objects.add(obj_id)

            # Unused detections become new tracks
            for i, det in enumerate(detections):
                if i not in used_inputs:
                    self._register(input_centroids[i], det)

            # Unused tracks increase disappearance counter
            for obj_id in object_ids:
                if obj_id not in used_objects:
                    self.disappeared[obj_id] += 1
                    if self.disappeared[obj_id] > self.max_disappeared:
                        self._deregister(obj_id)

        return detections

    def _register(self, centroid: tuple[float, float], det: dict):
        det["track_id"] = self.next_object_id
        self.objects[self.next_object_id] = {
            "centroid": centroid,
            "detection": det,
            "first_seen": time.time(),
        }
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1

    def _deregister(self, obj_id: int):
        self.objects.pop(obj_id, None)
        self.disappeared.pop(obj_id, None)


class DecisionEngine:
    def __init__(self, cooldown_seconds: float = 6.0):
        self.cooldown_seconds = cooldown_seconds
        self.last_announced: dict[str, float] = {}  # key -> timestamp

    def evaluate(self, tracked_detections: list[dict]) -> tuple[list[dict], dict | None]:
        """Evaluates tracked objects and produces an audio alert with spatial audio cues if appropriate."""
        now = time.time()
        enriched = []
        candidate_alert = None

        # Priority weights for campus safety
        priority_classes = {
            "stairs": 10,
            "door": 9,
            "lift": 9,
            "car": 8,
            "person": 7,
            "chair": 6,
            "table": 6,
            "bench": 5,
        }

        # Sort detections by proximity and priority
        def score(d):
            p = priority_classes.get(d["label"].lower(), 3)
            depth_multiplier = {"very_near": 4, "near": 3, "medium": 2, "far": 1}.get(d["depth"], 1)
            return p * depth_multiplier * d["confidence"]

        sorted_dets = sorted(tracked_detections, key=score, reverse=True)

        for d in sorted_dets:
            b = d["box"]
            cx = (b["left"] + b["right"]) / 2.0

            # Spatial Audio panning: -1.0 (left), 0.0 (center), +1.0 (right)
            # Map [0, 1] to [-1.0, 1.0] with dampening
            spatial_pan = round((cx - 0.5) * 2.0, 2)
            spatial_pan = max(-1.0, min(1.0, spatial_pan))

            if cx < 0.35:
                position = "to your left"
            elif cx > 0.65:
                position = "to your right"
            else:
                position = "ahead"

            d["position"] = position
            d["spatial_pan"] = spatial_pan
            enriched.append(d)

            # Check for candidate speech alert
            if candidate_alert is None and d["depth"] in ["very_near", "near", "medium"]:
                alert_key = f"{d.get('track_id', d['label'])}_{d['depth']}"
                last_time = self.last_announced.get(alert_key, 0.0)

                # Announce if cooldown passed or object moved to very_near
                if (now - last_time) >= self.cooldown_seconds:
                    depth_phrase = "directly in front" if d["depth"] == "very_near" else d["depth"]
                    if position == "ahead":
                        text = f"{d['label'].capitalize()} {position}, {depth_phrase}."
                    else:
                        text = f"{d['label'].capitalize()} {position}."

                    candidate_alert = {
                        "text": text,
                        "label": d["label"],
                        "depth": d["depth"],
                        "position": position,
                        "spatial_pan": spatial_pan,
                        "confidence": d["confidence"],
                        "track_id": d.get("track_id"),
                    }
                    self.last_announced[alert_key] = now

        return enriched, candidate_alert
