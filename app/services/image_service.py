from __future__ import annotations

import os
import uuid


class ImageAnalysisError(Exception):
    pass


def _detect_image_type(payload: bytes) -> str | None:
    if payload.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if payload.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if payload.startswith(b"GIF87a") or payload.startswith(b"GIF89a"):
        return "gif"
    if payload.startswith(b"BM"):
        return "bmp"
    return None


def save_and_analyze_image(upload_bytes: bytes, upload_root: str, chronological_age: int) -> tuple[str, float, float]:
    image_type = _detect_image_type(upload_bytes)
    if image_type is None:
        raise ImageAnalysisError("Invalid image uploaded")

    os.makedirs(upload_root, exist_ok=True)
    image_name = f"{uuid.uuid4().hex}.{image_type}"
    image_path = os.path.join(upload_root, image_name)

    with open(image_path, "wb") as f:
        f.write(upload_bytes)

    size_kb = max(1.0, len(upload_bytes) / 1024.0)
    quality_score = max(35.0, min(95.0, 40.0 + size_kb * 3.0))

    # Placeholder estimate until full external CV model is wired.
    quality_factor = (quality_score - 50.0) / 25.0
    facial_age_estimate = float(chronological_age) - quality_factor

    return image_path, round(quality_score, 2), round(facial_age_estimate, 2)
