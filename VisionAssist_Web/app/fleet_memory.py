"""Fleet Spatial Memory & Dynamic Micro-Hazard Registry for SafePath AI.

Coordinates:
- Active crowd-sensed or camera-detected micro-hazards across the campus graph.
- Expiration time management (e.g. wet floor expires in 1-2 hours).
- Provides real-time edge blockages/penalties to the Dijkstra routing engine.
- Active-Learning MLOps logging: caches detected anomalies to trigger retraining.
"""

import time
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
FLEET_CACHE_FILE = ROOT / "runs" / "fleet_hazards_registry.json"


class FleetSpatialMemory:
    def __init__(self):
        self.hazards: dict[str, dict] = {}
        # Pre-populate with realistic demo hazards matching Web and Android mockups
        self.report_hazard(
            node_id="lib_entrance",
            hazard_type="Blocked Path",
            description="Temporary construction scaffolding blocking main ramp",
            location_name="Library Entrance",
            reported_by="Android App (BVI User)",
            ttl_seconds=7200,
            severity="HIGH",
            status="VERIFIED"
        )
        self.report_hazard(
            node_id="science_lift_2",
            hazard_type="Broken Lift",
            description="Elevator out of service on 2nd Floor, technician dispatched",
            location_name="Science Block",
            reported_by="Campus Staff",
            ttl_seconds=10800,
            severity="HIGH",
            status="IN_REVIEW"
        )
        self.report_hazard(
            node_id="main_corridor",
            hazard_type="Water Spill",
            description="Wet floor near CSE block cleaned, drying underway",
            location_name="Main Corridor",
            reported_by="Cleaning Bot Sensor",
            ttl_seconds=3600,
            severity="MEDIUM",
            status="RESOLVED"
        )

    def report_hazard(
        self,
        node_id: str,
        hazard_type: str,
        description: str,
        location_name: str | None = None,
        reported_by: str = "camera_perception",
        ttl_seconds: int = 3600,
        severity: str = "MEDIUM",
        status: str = "IN_REVIEW"
    ) -> dict:
        now = time.time()
        hazard_id = f"hz_{node_id}_{int(now)}"
        clean_loc = location_name or node_id.replace("_", " ").title()
        record = {
            "id": hazard_id,
            "node_id": node_id,
            "location_name": clean_loc,
            "hazard_type": hazard_type,
            "description": description,
            "reported_by": reported_by,
            "severity": severity,
            "status": status,  # "IN_REVIEW", "VERIFIED", "RESOLVED"
            "reported_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)),
            "expires_at": now + ttl_seconds,
            "is_active": status != "RESOLVED",
        }
        self.hazards[hazard_id] = record
        self._save_cache()
        return record

    def update_hazard_status(self, hazard_id: str, new_status: str) -> dict | None:
        self.clear_expired()
        for hid, h in self.hazards.items():
            if hid == hazard_id or h.get("id") == hazard_id:
                h["status"] = new_status
                if new_status == "RESOLVED":
                    h["is_active"] = False
                elif new_status == "VERIFIED":
                    h["is_active"] = True
                self._save_cache()
                return h
        return None

    def clear_expired(self) -> None:
        now = time.time()
        for hid in list(self.hazards.keys()):
            if self.hazards[hid]["expires_at"] < now:
                self.hazards.pop(hid, None)

    def get_active_hazards(self) -> list[dict]:
        self.clear_expired()
        return list(self.hazards.values())

    def get_blocked_nodes(self) -> set[str]:
        self.clear_expired()
        return {h["node_id"] for h in self.hazards.values() if h["severity"] in ["HIGH", "CRITICAL"]}

    def get_node_hazard(self, node_id: str) -> dict | None:
        self.clear_expired()
        for h in self.hazards.values():
            if h["node_id"] == node_id:
                return h
        return None

    def _save_cache(self) -> None:
        try:
            FLEET_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            FLEET_CACHE_FILE.write_text(json.dumps(list(self.hazards.values()), indent=2), encoding="utf-8")
        except Exception:
            pass


# Global singleton
fleet_memory = FleetSpatialMemory()
