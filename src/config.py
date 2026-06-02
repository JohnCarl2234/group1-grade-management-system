from pathlib import Path

# Project root (one level above src)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# App static folder (prefer top-level `static/`, fallback to `app/static/`)
if (PROJECT_ROOT / "static").exists():
    APP_STATIC = PROJECT_ROOT / "static"
else:
    APP_STATIC = PROJECT_ROOT / "app" / "static"

def asset_path(*parts: str) -> str:
    """Return a robust absolute path to an asset inside the project."""
    p = APP_STATIC.joinpath(*parts)
    try:
        # Prefer file:// URI which works in browsers/Streamlit frontends
        return p.resolve().as_uri()
    except Exception:
        return str(p.resolve())

# Provide a PIL Image object for use as `page_icon`
try:
    from PIL import Image

    def load_image(name: str):
        p = APP_STATIC.joinpath(name).resolve()
        return Image.open(p)

    try:
        MASCOT_IMAGE = load_image("mascot.png")
    except Exception:
        MASCOT_IMAGE = None
except Exception:
    MASCOT_IMAGE = None


# Common asset: mascot used as page icon / logo 
MASCOT_PATH = asset_path("mascot.png")

