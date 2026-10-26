# VisionAssist Web — Project Report Outline

## Title

**VisionAssist Web: A Browser-Based AI Accessibility Assistant with Real-Time Vision, OCR, Voice Guidance and Campus Navigation**

## Problem

A visually impaired user needs a simple interface that can understand nearby objects, communicate important information through speech, read visible text and guide the user toward a campus destination. The Android version creates unnecessary deployment friction because the demo depends on Gradle, CameraX, device permissions and ONNX Runtime integration.

## Proposed Solution

VisionAssist Web moves the interaction layer to a responsive browser. Camera capture is handled with browser media APIs, the local FastAPI backend performs computer-vision inference, the UI renders accessible overlays, and browser speech APIs provide voice interaction.

## Main Modules

1. Live camera and detection
2. Context/proximity estimation
3. OCR
4. Voice input/output
5. Campus route planning
6. Accessibility UI
7. Privacy/session layer

## Innovation

- **Privacy-first processing:** image frames are posted to the local backend and are not stored by the API.
- **Explainable model status:** the interface explicitly states whether the detector is the temporary COCO checkpoint or the future campus-specific model.
- **Voice-first web interaction:** the user can use natural commands such as “what’s ahead” and “navigate to library”.
- **Campus graph navigation:** routing is separated from perception so the campus map can be updated without changing the UI.
- **Progressive Web App:** the project can behave like an installable web application without an Android APK.

## Current Model Scope

The included workflow uses standard YOLOv8n COCO-pretrained weights for the demo. This is a real detector, but it is not the final VisionAssist 15-class campus detector. The final project should train and validate the intended classes on an appropriately licensed dataset and then place that trained checkpoint behind the same API contract.

## Evaluation Plan

Measure detection precision/recall/mAP on the real 15-class campus dataset, inference latency on the target laptop/device, OCR readability on campus signs, route-planning correctness, voice command accuracy and user-task completion time.
