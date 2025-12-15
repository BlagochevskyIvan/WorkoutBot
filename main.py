import asyncio
import uvicorn
from config.cp_config import HOST, PORT, RELOAD
from server.fast_api_init import init_fastapi_app

app = init_fastapi_app()

async def main() -> None:
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=RELOAD,
    )


if __name__ == "__main__":
    asyncio.run(main())
