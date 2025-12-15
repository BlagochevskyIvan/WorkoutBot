from dotenv import load_dotenv
import os
from pathlib import Path
from config.logger import logger

load_dotenv()

CP_BASE_URL = os.getenv("CP_BASE_URL")
CP_PUBLIC_ID = os.getenv("CP_PUBLIC_ID")
CP_SECRET_KEY = os.getenv("CP_SECRET_KEY")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = BASE_DIR / "templates"


TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://your.domain/telegram
WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/telegram")
SECRET_TOKEN = os.getenv("TELEGRAM_SECRET") or os.getenv("WEBHOOK_SECRET")
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))
RELOAD: bool = os.getenv("RELOAD", "true").lower() in {"1", "true", "yes"}
DROP_PENDING: bool = os.getenv("DROP_PENDING", "false").lower() in {"1", "true", "yes"}
DATABASE_URL: str = os.getenv("DATABASE_URL")
DATABASE_ECHO: bool = True if os.getenv("DATABASE_ECHO") == "True" else False

if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN is required")
if not WEBHOOK_URL:
    raise RuntimeError("WEBHOOK_URL is required (must be full HTTPS URL incl. path)")
if not SECRET_TOKEN:
    logger.warning(
        "No SECRET_TOKEN provided. Set TELEGRAM_SECRET/WEBHOOK_SECRET to verify Telegram requests."
    )
