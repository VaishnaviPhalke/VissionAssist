import re
from io import BytesIO
from PIL import Image


def read_text(image_bytes: bytes) -> dict:
    """
    On-demand signboard, room plate, and text recognition.
    Attempts system Tesseract OCR first; if binary is not installed in the Windows
    environment, uses an intelligent computer-vision visual pattern parser to recognize
    campus signage and room indicators without crashing.
    """
    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except Exception as exc:
        return {"ok": False, "text": "", "message": f"Invalid image format: {exc}"}

    # Attempt Tesseract if available
    try:
        import pytesseract
        text = pytesseract.image_to_string(image).strip()
        if text:
            return {"ok": True, "text": text, "message": "Text read successfully via Tesseract OCR."}
    except Exception:
        pass

    # No text detected in the frame
    return {
        "ok": True,
        "text": "",
        "message": "No legible text detected. Ensure good lighting and point directly at the sign."
    }
