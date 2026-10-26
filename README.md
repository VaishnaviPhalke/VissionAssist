# VisionAssist AI 2.0 👁️‍🗨️
### Real-Time Assistive Vision & Accessible Campus Navigation for Blind and Low-Vision Students

VisionAssist AI 2.0 is an intelligent, voice-first assistive Android system engineered for blind and low-vision individuals. Powered by edge-optimized computer vision (YOLOv8-Nano), multilingual text-to-speech, tactile haptic warnings, and continuous MLOps release governance (SAFE-Loop).

---

## 🌟 Key Features

- **Voice-First Multilingual Onboarding (Screen 01)**:
  - Spoken onboarding instructions upon first launch.
  - 5 Languages Supported: **English**, **Hindi (हिंदी)**, **Marathi (मराठी)**, **Spanish (Español)**, and **Tamil (தமிழ்)**.
  - Interactive speech rate calibration slider with instant audio testing.
- **Real-Time SafePath Obstacle Detection HUD (Screen 03)**:
  - Live CameraX feed with bounding box overlay and directional tracking (`ahead`, `left`, `right`).
  - Distance estimation in meters ($0.8\text{m}$ to $3.5\text{m}$).
  - **Dual-Channel Sensory Alerting**: Spoken directional alerts + heavy haptic vibration pulses for close-range danger ($< 1.4\text{m}$).
  - Interactive 6-class simulation chips (Chair, Person, Stairs, Closed Door, Laptop, Clear Path) for bench testing without live obstacles.
- **Signboard & Notice Reader (OCR - Screen 05)**:
  - Instant camera text capture and spoken readout of campus notices, library hours, and building directions.
- **Crowdsourced Campus Hazards (Screen 06)**:
  - Real-time alerts for temporary obstacles, wet floors, and construction zones with alternative accessible ramp routes.
- **Hands-Free Voice Command Assistant (Screen 07)**:
  - Natural speech triggers: *"Detect"* / *"शुरू"* / *"सुरू"*, *"Read"* / *"पढ़ो"* / *"वाचा"*, *"Emergency"* / *"मदद"*.
- **Emergency SOS Hub (Screen 12)**:
  - One-tap campus security dispatch (Ext. 0199) with automatic GPS sharing and tactile confirmation.
- **Slide-Out Navigation Drawer (`☰`)**:
  - Instant switching between all 12 accessibility screens and diagnostics.

---

## 🏛️ System Architecture

```
 VisionAssist AI 2.0
 ├── vision_assist_app/          # Native Android Flutter Mobile Application
 │   ├── lib/main.dart           # Complete 12-Screen Accessibility UI & Audio/Haptic Core
 │   ├── android/                # Native Android configuration, CameraX & Gradle
 │   └── pubspec.yaml            # TTS, Camera, and Hardware dependencies
 └── VisionAssist_Web/           # Backend MLOps, Model Storage & Audit Pipeline
     ├── app/main.py             # FastAPI service & Fleet Memory Hub
     ├── models/                 # Quantized YOLOv8-Nano weights & metadata
     └── runs/safeloop/          # SAFE-Loop continuous validation & benchmark suite
```

---

## 📱 Installation (Android APK)

1. Download the compiled release APK: `VisionAssist_AI.apk`
2. Install via ADB or file transfer:
   ```bash
   adb install VisionAssist_AI.apk
   ```
3. Open **VisionAssist AI** and follow the voice instructions to calibrate language and speech speed.

---

## 🚀 Development Setup

### Android App
```bash
cd vision_assist_app
flutter pub get
flutter run
```

### Backend & MLOps Service
```bash
cd VisionAssist_Web
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📜 License & Acknowledgments
Built with ❤️ for accessible, inclusive campus mobility.
