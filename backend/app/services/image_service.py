"""
Image compression service using Pillow.
Compresses images before storing in GridFS.
"""
import io
from PIL import Image


def compress_image(image_bytes: bytes, max_size: tuple = (1920, 1080), quality: int = 80, fmt: str = "JPEG") -> bytes:
    """Compress an image and return the resulting bytes.

    Args:
        image_bytes: Raw image file bytes.
        max_size: Maximum (width, height) – image is resized proportionally if larger.
        quality: JPEG quality (1-100).
        fmt: Output format (JPEG / PNG / WEBP).

    Returns:
        Compressed image bytes.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))

        # Convert RGBA to RGB for JPEG
        if fmt.upper() == "JPEG" and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Proportional resize
        img.thumbnail(max_size, Image.LANCZOS)

        buf = io.BytesIO()
        save_kwargs = {"format": fmt, "optimize": True}
        if fmt.upper() in ("JPEG", "WEBP"):
            save_kwargs["quality"] = quality
        img.save(buf, **save_kwargs)
        return buf.getvalue()
    except Exception:
        # If compression fails, return the original bytes
        return image_bytes


def get_image_dimensions(image_bytes: bytes) -> tuple:
    """Return (width, height) of an image."""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        return img.size
    except Exception:
        return (0, 0)


def is_valid_image(image_bytes: bytes) -> bool:
    """Check if bytes represent a valid image."""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()
        return True
    except Exception:
        return False
