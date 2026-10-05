import os

os.environ.setdefault("TELEGRAM_TOKEN", "test_token")
os.environ.setdefault("WEBHOOK_URL", "https://example.com/webhook")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5435/test_db")