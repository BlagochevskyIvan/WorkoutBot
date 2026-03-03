from dotenv import load_dotenv
import os
from pathlib import Path
from config.logger import logger

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = BASE_DIR / "templates"


TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/telegram")
WEBAPP_URL = os.getenv("WEBAPP_URL")
SECRET_TOKEN = os.getenv("TELEGRAM_SECRET", '123')
DROP_PENDING: bool = os.getenv("DROP_PENDING", "false").lower() in {"1", "true", "yes"}
DATABASE_URL: str = os.getenv("DATABASE_URL")
DATABASE_ECHO: bool = True if os.getenv("DATABASE_ECHO") == "True" else False

if not TOKEN:
    raise NameError("TELEGRAM_TOKEN is required")
if not WEBHOOK_URL:
    raise NameError("WEBHOOK_URL is required (must be full HTTPS URL incl. path)")
if not SECRET_TOKEN:
    logger.warning(
        "No SECRET_TOKEN provided. Set TELEGRAM_SECRET/WEBHOOK_SECRET to verify Telegram requests."
    )
