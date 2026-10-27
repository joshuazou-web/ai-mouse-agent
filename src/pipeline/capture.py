"""Capture entries for AI Mouse.

- point: primary Point path (hotkey / mouse selection → screenshot)
- capture_region: Ask-key bypass for hard cases — explicit region/框选 screenshot
  (hold-to-talk + optional region capture). NOT a fourth sellable feature;
  still feeds the same understand → Do pipeline.

Mac: `screencapture -i`. Non-Mac / demo: pass --image.
"""
import platform, shutil, subprocess, tempfile, os

VALID_ENTRIES = ("point", "capture_region")

def capture(image: str | None = None, entry: str = "point") -> str:
    if entry not in VALID_ENTRIES:
        raise ValueError(f"entry must be one of {VALID_ENTRIES}, got {entry!r}")
    if image:
        if not os.path.isfile(image):
            raise FileNotFoundError(image)
        return image
    if platform.system() == "Darwin" and shutil.which("screencapture"):
        # Interactive region select — shared by Point and Ask capture_region
        prefix = "ask_region_" if entry == "capture_region" else "point_"
        out = tempfile.mktemp(suffix=".png", prefix=prefix)
        subprocess.run(["screencapture", "-i", out], check=True)
        if not os.path.exists(out):
            raise RuntimeError("Selection cancelled")
        return out
    raise RuntimeError("Non-Mac: pass --image <path to existing screenshot>")


def capture_region(image: str | None = None) -> str:
    """Ask-key bypass: explicit region capture → same downstream Do."""
    return capture(image=image, entry="capture_region")
