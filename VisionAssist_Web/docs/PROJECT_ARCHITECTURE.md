# VisionAssist Web — architecture

## 1. Presentation layer

`static/` contains a responsive browser UI, camera preview, canvas overlays, accessibility controls, OCR, voice commands, navigation and a session log.

## 2. Application/API layer

FastAPI exposes small, explicit endpoints:

- `GET /api/health`
- `POST /api/detect`
- `POST /api/ocr`
- `GET /api/navigation`
- `GET /api/map`
- `GET /api/demo/status`

## 3. AI layer

`app/detector.py` loads YOLOv8n with Ultralytics and performs detection on CPU. The current checkpoint is COCO-pretrained and therefore only supports the classes learned by that checkpoint.

## 4. Context layer

The backend derives a light proximity heuristic from bounding-box area and exposes a mapping to VisionAssist target labels where a COCO label is compatible.

## 5. Navigation layer

`app/navigation.py` contains a small Dijkstra route planner over `data/campus_map.json`. Replace the demo graph with your actual campus graph.

## 6. Innovation layer

The web version adds a privacy-first processing mode, installable PWA shell, explainable model status, voice-first control and a session log that can be used during project demonstrations.

## Important distinction

The temporary YOLOv8n checkpoint is a demonstration model. The final VisionAssist project still needs a properly trained campus-specific 15-class model before claims about door/stairs/lift/classroom/laboratory/corridor detection are made.
