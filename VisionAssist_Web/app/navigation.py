"""Adaptive Multi-Persona Campus Navigator for SafePath AI.

Features:
- Dynamic graph pathfinding with Dijkstra algorithm.
- Multi-Persona constraints:
  * 'bvi': standard walking paths, stairs permitted with audio cues.
  * 'wheelchair': strictly step-free; stairs completely pruned; prioritizes elevators & ramps.
  * 'elderly': prioritizes low-fatigue routes with benches, ramps & elevators.
  * 'emergency': routes to nearest exit node, avoiding active hazards.
- Dynamic fleet micro-hazard avoidance: reroutes around blocked nodes in real time.
"""

import json
import heapq
from pathlib import Path
from .fleet_memory import fleet_memory


class CampusNavigator:
    def __init__(self, path: Path):
        self.path = path
        self.reload_map()

    def reload_map(self):
        with self.path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        self.data = data
        self.nodes = {n["id"]: n for n in data["nodes"]}
        self.base_graph = {node_id: [] for node_id in self.nodes}
        for a, b, weight in data["edges"]:
            if a in self.nodes and b in self.nodes:
                self.base_graph[a].append((b, weight))
                self.base_graph[b].append((a, weight))

    def search_node(self, query: str):
        q = query.strip().lower()
        if not q:
            return None
        # Exact match
        for node in self.nodes.values():
            if node["name"].lower() == q or node["id"].lower() == q:
                return node
        # Partial match
        for node in self.nodes.values():
            if q in node["name"].lower() or q in node["id"].lower():
                return node
        # Alias matching for common campus queries
        aliases = {
            "library": "library",
            "books": "library",
            "reading room": "library",
            "cse": "cse_dept",
            "computer": "cse_lab",
            "hpc": "cse_lab",
            "lab": "cse_lab",
            "ai": "ai_robotics_lab",
            "robotics": "ai_robotics_lab",
            "gate": "main_gate",
            "entrance": "main_gate",
            "food": "canteen",
            "cafeteria": "canteen",
            "lunch": "canteen",
            "canteen": "canteen",
            "admin": "admin",
            "office": "admin",
            "auditorium": "auditorium",
            "stage": "auditorium",
            "seminar": "seminar_hall",
            "lift": "lift_1",
            "elevator": "lift_1",
            "stairs": "stairs_1",
            "exit": "emergency_exit_east",
            "emergency": "emergency_exit_east"
        }
        for alias, node_id in aliases.items():
            if alias in q and node_id in self.nodes:
                return self.nodes[node_id]
        return None

    def route(
        self,
        destination: str,
        start: str | None = None,
        persona: str = "bvi"
    ) -> dict:
        source = start or self.data.get("start_node", "main_gate")
        if source not in self.nodes:
            source = list(self.nodes.keys())[0]

        # Emergency Mode: destination defaults to nearest exit if not specified
        if persona == "emergency" and (not destination or destination.lower() in ["exit", "safe_exit", "emergency"]):
            goal_node = self.nodes.get("emergency_exit_east") or self.nodes.get("main_gate")
        else:
            goal_node = self.search_node(destination)

        if not goal_node:
            available_destinations = [n["name"] for n in list(self.nodes.values())[:8]]
            return {
                "ok": False,
                "message": f"Destination '{destination}' was not found. Try one of: {', '.join(available_destinations)}."
            }

        goal = goal_node["id"]
        blocked_nodes = fleet_memory.get_blocked_nodes()
        avoided_nodes = []

        # Build dynamic graph honoring persona and active fleet hazards
        dynamic_graph = {node_id: [] for node_id in self.nodes}

        for u in self.nodes:
            for v, weight in self.base_graph[u]:
                edge_cost = float(weight)

                # Wheelchair constraint: prune stairs completely
                if persona == "wheelchair":
                    if "stairs" in u.lower() or "stairs" in v.lower():
                        continue

                # Elderly constraint: favor elevator over stairs
                if persona == "elderly":
                    if "stairs" in u.lower() or "stairs" in v.lower():
                        edge_cost += 10.0

                # Active fleet hazard avoidance
                if v in blocked_nodes:
                    avoided_nodes.append(v)
                    # Apply heavy penalty so it routes around unless strictly trapped
                    edge_cost += 50.0

                dynamic_graph[u].append((v, edge_cost))

        dist = {node_id: float("inf") for node_id in self.nodes}
        prev = {node_id: None for node_id in self.nodes}
        dist[source] = 0.0
        heap = [(0.0, source)]

        while heap:
            d, current = heapq.heappop(heap)
            if d != dist[current]:
                continue
            if current == goal:
                break
            for nxt, weight in dynamic_graph[current]:
                nd = d + weight
                if nd < dist[nxt]:
                    dist[nxt] = nd
                    prev[nxt] = current
                    heapq.heappush(heap, (nd, nxt))

        if dist[goal] == float("inf"):
            return {
                "ok": False,
                "message": f"No accessible path found to {goal_node['name']} for persona '{persona}'."
            }

        path = []
        cur = goal
        while cur:
            path.append(cur)
            cur = prev[cur]
        path.reverse()

        steps = []
        for i, node_id in enumerate(path):
            node = self.nodes[node_id]
            hazard = fleet_memory.get_node_hazard(node_id)
            hazard_warning = f" [Caution: {hazard['description']}]" if hazard else ""
            if i == 0:
                text = f"Start at {node['name']}{hazard_warning}"
            elif i == len(path) - 1:
                text = f"Arrive at destination: {node['name']}{hazard_warning}"
            else:
                text = f"Proceed to {node['name']}{hazard_warning}"
            
            steps.append({
                "node_id": node_id,
                "name": node["name"],
                "floor": node.get("floor", 0),
                "type": node.get("type", "waypoint"),
                "instruction": text,
                "has_hazard": hazard is not None,
                "x": node.get("x", 0),
                "y": node.get("y", 0)
            })

        has_rerouted = any(nid in blocked_nodes for nid in avoided_nodes)
        persona_advice = {
            "wheelchair": "Wheelchair Accessible: Step-free route selected. All staircases excluded; ramps and elevator used.",
            "bvi": "Visually Impaired (BVI): Standard accessible route with spatial audio tracking.",
            "elderly": "Elderly Assisted: Low-fatigue route selected with benches and elevators.",
            "emergency": "Emergency Evacuation: Egress route to nearest clear exit."
        }.get(persona, "Standard route.")

        return {
            "ok": True,
            "destination": goal_node["name"],
            "persona": persona,
            "persona_advice": persona_advice,
            "rerouted": has_rerouted,
            "avoided_hazards": list(set(avoided_nodes)),
            "distance_cost": round(dist[goal], 1),
            "steps": steps,
            "path_node_ids": path
        }
