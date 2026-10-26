# 3-minute demo script

1. Open the browser app and start the camera.
2. Point the camera at a person, bottle, chair or backpack and show the live bounding boxes.
3. Click “What’s ahead?” to demonstrate scene narration.
4. Use “Read text in front of camera” on a clear printed page/sign. If Tesseract is not installed on Windows, explain that OCR is a local optional dependency.
5. Type `Library` and click Navigate to show the campus graph and route steps.
6. Enable voice and say `what's ahead` or `navigate to library`.
7. Explain that the current detector is the temporary COCO-pretrained checkpoint; the final 15-class model is a separate training milestone.
